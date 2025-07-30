from __future__ import annotations

import asyncio
import asyncio.exceptions
import dataclasses
import enum
import logging
import multiprocessing
import os
import signal
import uuid
from collections import deque
from datetime import datetime
from typing import Dict, List, Optional, Union, Sequence, TYPE_CHECKING

import aiomultiprocess
import setproctitle
import zmq.error

from .run_governor import RunGovernor
from palaestrai.version import __version__
from palaestrai.core.protocol import (
    ExperimentRunShutdownRequest,
    ExperimentRunShutdownResponse,
    ExperimentRunStartRequest,
    ExperimentRunStartResponse,
)
from palaestrai.util import LogServer, spawn_wrapper
from palaestrai.core import MajorDomoBroker, MajorDomoClient, RuntimeConfig

if TYPE_CHECKING:
    import palaestrai.experiment

LOG = logging.getLogger(__name__)


class ExecutorState(enum.Enum):
    PRISTINE = 0
    INITIALIZED = 1
    RUNNING = 2
    SHUTDOWN = 3
    EXITED = 4
    SIGINT = 5
    SIGABRT = 6
    SIGTERM = 7


@dataclasses.dataclass
class _RunGovernorPCB:
    """Simple Process Control Block for RunGovernor control."""

    run_governor_id: str
    started_at: datetime
    run_governor_process: aiomultiprocess.Process
    experiment_run: palaestrai.experiment.ExperimentRun
    experiment_run_id: Optional[str] = None


@dataclasses.dataclass
class ExperimentRunRuntimeInformation:
    """Accumulated information about the one experiment run

    This structure contains information about one experiment run.
    It stores on which :py:class:`RunGovernor` it is executed, when it
    was started, which run is being executed and what ID the
    experiment run has.
    """

    experiment_run: palaestrai.experiment.ExperimentRun
    started_at: Union[datetime, None] = None
    run_governor_id: Union[str, None] = None
    experiment_run_id: Union[str, None] = None

    @property
    def is_running(self):
        return self.experiment_run_id is not None


class ExperimentRunStartError(RuntimeError):
    def __init__(self, experiment_run_id, run_governor_id, message):
        super().__init__(message)
        self.experiment_run_id = experiment_run_id
        self.run_governor_id = run_governor_id
        self.message = message


class DeadMajorDomoBrokerError(RuntimeError):
    def __init__(self):
        super().__init__()


class InterruptSignal(RuntimeError):
    def __init__(self):
        super().__init__()


async def _execute_run_governor(uid: str):
    """Executes the ::`RunGovernor` main loop, catching errors

    This is a wrapper function around that creates a ::`RunGovernor` and
    handles ::`RunGovernor.run`. It takes care of clearing signal handlers,
    setting the proctitle, and generally catching errors in a meaningful in
    order to report it to the Executor without simply dying.

    This method belongs to the ::`Executor` logically, but is not part of the
    class in order to avoid serialization/deserialization of the whole Executor
    each time a new ::`RunGovernor` process is spawned.

    Parameters
    ----------
    uid : str
        UID of the new ::`RunGovernor`
    broker_uri : str
        URI of the ::`MajorDomoBroker` instance to connect to for further
        communication

    Return
    ------
    Nothing.
    """
    pid = os.getpid()
    os.setpgrp()
    try:
        run_gov = RunGovernor(
            uid=uid,
        )
        await run_gov.run()  # type: ignore
    except Exception as e:
        LOG.critical("Execution of RunGovernor(uid=%s) failed: %s.", uid, e)
        LOG.debug("Execution of RunGovernor(uid=%s) failed:", exc_info=e)
        os.killpg(pid, signal.SIGKILL)
        raise e


class Executor:
    """The executor is the entrypoint for every run execution.

    The role of the executor is to receive new experiment runs and
    distribute them to existing :class:`RunGovernor` instances. If
    palaestrAI is used in local run mode, the executor will initialize
    a :class:`RunGovernor`.

    Furthermore, the Executor can stop running experiment runs.

    Notes
    -----
        At some point, when the core protocol has progressed far enough,
        we will be able to run several experiments at once from an
        executor. But, until we're sure we can, the public API accepts
        only one experiment.

    """

    def __init__(self):
        # (At some point, when the core protocol has progressed far enough,
        # we will be able to run several experiments at once from an executor.
        # But, until we're sure we can, the public API accepts only one
        # experiment.)

        self._state: ExecutorState = ExecutorState.PRISTINE
        self._broker: Union[None, MajorDomoBroker] = None
        self._client: Union[None, MajorDomoClient] = None
        self._broker_process: Union[None, aiomultiprocess.Process] = None
        self._broker_ctrl = multiprocessing.Pipe()
        self._run_governors: Dict[str, _RunGovernorPCB] = {}
        self._runs_scheduled = deque()
        self._log_server = LogServer("127.0.0.1", RuntimeConfig().logger_port)
        aiomultiprocess.set_start_method(
            RuntimeConfig().fork_method
        )  # Set best default for this OS.

    def _handle_signal_interrupt(self, signum):
        """Handle interrupting signals by notifying of the state change."""
        LOG.info(
            "palaestrAI executor has received signal %s, shutting down", signum
        )
        if self._state in {
            ExecutorState.SIGINT,
            ExecutorState.SIGABRT,
            ExecutorState.SIGTERM,
        }:
            # We already received a signal to interrupt and are probably
            # waiting for another process, but the user wants to exit in any
            # case. Well, let's do it, then.
            LOG.debug(
                "%s kills MajorDomoBroker process (PID: %s)",
                self,
                self._broker_process.pid,
            )
            self._broker_process.kill()
            try:
                _ = asyncio.get_running_loop().create_task(
                    self._broker_process.join(5)
                )
            except TimeoutError:
                LOG.error(
                    "%s could not kill MajorDomoBroker(pid=%s); "
                    "see if you have to kill it yourself. "
                    "Here is my spear: -->",
                    self,
                    self._broker_process.pid,
                )
        else:
            if signum not in {signal.SIGABRT, signal.SIGINT, signal.SIGTERM}:
                return
            old_state = self._state
            self._state = {
                signal.SIGINT.value: ExecutorState.SIGINT,
                signal.SIGABRT.value: ExecutorState.SIGABRT,
                signal.SIGTERM.value: ExecutorState.SIGTERM,
            }[signum]
            LOG.info(
                "%s changed state from %s to %s.", self, old_state, self._state
            )

    def _init_signal_handler(self):
        """Sets handlers for interrupting signals in the event loop."""
        signals = {signal.SIGINT, signal.SIGABRT, signal.SIGTERM}
        LOG.debug(
            "Executor(id=0x%x) registering signal handlers for signals %s.",
            id(self),
            signals,
        )
        loop = asyncio.get_running_loop()
        for signum in signals:
            loop.add_signal_handler(
                signum, self._handle_signal_interrupt, signum
            )

    async def _init_logging(self):
        """Starts the log server and configures log filters"""
        await self._log_server.start()

        def filter_record_above_debug(record: logging.LogRecord):
            if record.levelname != "DEBUG":
                return False
            return True

        for h in [h for h in logging.root.handlers if "debug" in h.name]:
            h.addFilter(filter_record_above_debug)

    def _init_communication(self):
        """Initialization of all core components"""
        LOG.info("Starting Major Domo Broker...")
        self._broker = MajorDomoBroker(uri=None, ctrl=self._broker_ctrl[1])
        self._broker_process = aiomultiprocess.Process(
            daemon=True,
            target=spawn_wrapper,
            args=(
                "MajorDomoBroker",
                RuntimeConfig().to_dict(),
                self._broker.mediate,
            ),
            name="Executor-MajorDomoBroker",
        )
        self._broker_process.start()
        broker_uri = self._broker_ctrl[0].recv()
        RuntimeConfig().broker_uri = broker_uri
        LOG.info(
            "Major Domo Broker is bound to %s.",
            RuntimeConfig().broker_uri,
        )
        self._client = MajorDomoClient(RuntimeConfig().broker_uri)
        LOG.debug(
            "Executor(id=0x%x) started MajorDomoClient(id=0x%x, uri=%s).",
            id(self),
            id(self._client),
            RuntimeConfig().broker_uri,
        )

    @staticmethod
    def _join_process(process: aiomultiprocess.Process):
        while process.is_alive():
            try:
                process.join(3)
            except TimeoutError:
                pass

    def experiment_runs(self) -> List[ExperimentRunRuntimeInformation]:
        runs = list()
        for run in self._runs_scheduled:
            runs.append(ExperimentRunRuntimeInformation(experiment_run=run))

        for pcb in self._run_governors.values():
            runs.append(
                ExperimentRunRuntimeInformation(
                    experiment_run=pcb.experiment_run,
                    started_at=pcb.started_at,
                    experiment_run_id=pcb.experiment_run_id,
                )
            )
        return runs

    async def _launch_run_governor(
        self, experiment_run: palaestrai.experiment.ExperimentRun
    ) -> _RunGovernorPCB:
        """Launches a new :py:class:`RunGovernor` process

        This method creates a new `aiomultiprocess.Process` and launches it,
        returning the appropriate PCB object.

        :rtype: _RunGovernorPCB
        """
        run_gov_uid = str(uuid.uuid4())
        run_gov_process = aiomultiprocess.Process(
            target=spawn_wrapper,
            args=(
                f"palaestrAI[RunGovernor-{run_gov_uid[-6:]}",
                RuntimeConfig().to_dict(),
                _execute_run_governor,
                [run_gov_uid],
            ),
        )
        run_gov_process.start()
        pcb = _RunGovernorPCB(
            experiment_run=experiment_run,
            started_at=datetime.now(),
            run_governor_id=run_gov_uid,
            run_governor_process=run_gov_process,
        )
        LOG.debug(
            "Launched new RunGovernor %s",
        )
        return pcb

    async def _deploy_experiment_run(
        self, experiment_run: palaestrai.experiment.ExperimentRun
    ):
        """Creates a :py:class:`RunGovernor` for a given experiment
        run.

        This method creates a new :py:class:`RunGovernor` and deploys
        the provided :py:class:`ExperimentRun` to it, pending start.

        The new :py:class:`RunGovernor` is started as a "python-
        parallel" process. All information about the running process is
        saved in the `self._run_governors` list, where we can also take
        care to stop all run governors should we need to.

        Parameters
        ----------
        experiment_run: ExperimentRun
            The experiment that should be executed.

        Returns
        -------
        str
            An opaque :py:class:`RunGovernor` identification string.
        """

        pcb = await self._launch_run_governor(experiment_run)
        self._run_governors[pcb.run_governor_id] = pcb
        return pcb.run_governor_id

    async def _start_experiment_run(self, run_governor_id):
        """Starts a previously deployed experiment run.

        When the experiment run is deployed via
        :py:meth:`_deploy_experiment_run`, the :py:class:`RunGovernor`
        is ready, but does not yet start it. This is done through this
        method, which sends the appropriate messages over the executor
        communications bus.

        Parameters
        ----------
        run_governor_id: str
            ID of the :class:`RunGovernor` that shall commence the
            experiment run.
        """
        pcb = self._run_governors[run_governor_id]
        experiment_run_id = pcb.experiment_run.uid
        msg = ExperimentRunStartRequest(
            sender_executor_id=str(id(self)),
            receiver_run_governor_id=run_governor_id,
            experiment_run_id=experiment_run_id,
            experiment_run=pcb.experiment_run,
        )
        LOG.info(
            'Starting experiment run "%s". Our business is life itself',
            experiment_run_id,
        )
        response = await self._client.send(run_governor_id, msg)

        if isinstance(response, ExperimentRunStartResponse):
            if response.successful is True:
                pcb.experiment_run_id = experiment_run_id
                LOG.debug(
                    "Executor(id=0x%x) received ExperimentRunStart"
                    "Response from RunGovernor(uid=%s) for "
                    "ExperimentRun(run_id=%s).",
                    id(self),
                    run_governor_id,
                    experiment_run_id,
                )
            else:
                LOG.error("Could not start experiment run: %s", response.error)
                raise ExperimentRunStartError(
                    experiment_run_id=experiment_run_id,
                    run_governor_id=run_governor_id,
                    message=response.error,
                )
        else:
            LOG.error(
                "Executor expected ExperimentRunStartResponse, but got "
                "'%s' instead",
                response,
            )
            raise TypeError
        LOG.debug(
            "Executor(id=0x%x) started experiment run (experiment_run_id=%s), "
            "got ExperimentStartResponse(successful=%s).",
            id(self),
            experiment_run_id,
            response.successful,
        )
        return experiment_run_id

    async def cancel(self, experiment_run_id):
        """Shuts an experiment run down prematurely.

        This method sends a :py:class:`ExperimentShutdownRequest` to
        the :py:class:`RunGovernor` responsible for executing the
        associated experiment run. This allows for a graceful, yet
        premature shutdown of a running experiment run. Normally,
        experiment runs terminate when their termination condition is
        met, so this method provides a way for an external user to
        interfere with a running experiment.

        Parameters
        ----------
        experiment_run_id: str
            UID of the experiment run to shut down.
        """
        rg_dict_item = next(
            filter(
                lambda i: i[1].experiment_run_id == experiment_run_id,
                self._run_governors.items(),
            ),
            None,
        )
        run_governor_id = rg_dict_item[0]

        if run_governor_id is None:
            LOG.error(
                "Executor (id=0x%x) cannot terminate ExperimentRun("
                "run_id=%s): Cannot find RunGovernor",
                id(self),
                experiment_run_id,
            )
            return

        LOG.debug(
            "Executor (id=0x%x) sending ExperimentRunShutdownRequest for "
            "ExperimentRun(run_id=%s).",
            id(self),
            experiment_run_id,
        )
        msg = ExperimentRunShutdownRequest(
            sender_executor_id=str(id(self)),
            receiver_run_governor_id=run_governor_id,
            experiment_run_id=experiment_run_id,
        )
        response = await self._client.send(run_governor_id, msg)
        LOG.debug("Executor(id=0x%x) received %s", id(self), response)
        if not isinstance(response, ExperimentRunShutdownResponse):
            return
        if not response.successful:
            # This may lead to an error when performed during an
            # iteration over the run_governors:
            # self._run_governors.pop(run_governor_uid, None)
            raise RuntimeError(response.error)

    def schedule(
        self,
        experiment_run: Union[
            palaestrai.experiment.ExperimentRun,
            Sequence[palaestrai.experiment.ExperimentRun],
        ],
    ):
        """Schedules an experiment run to be executed.

        This method schedules experiment runs, i.e., puts them in the
        waiting queue. The main loop (started by ::`execute`) picks up
        experiment run objects and executes them.

        Parameters
        ----------
        experiment_run : Union[palaestrai.experiment.ExperimentRun,
        Sequence[palaestrai.experiment.ExperimentRun]]
            One or many :class:`palaestrai.experiment.ExperimentRun` objects,
            which are added to the queue.
        """
        if isinstance(experiment_run, list):
            self._runs_scheduled.extend(experiment_run)
        else:
            self._runs_scheduled.append(experiment_run)

    def shutdown(self):
        """Performs an oderly shutdown"""
        # We need to discriminate via state. If we're currently running, but
        # receive a call to "shutdown", then its coming from outside and we
        # need to change the flag to have an orderly shutdown on the main loop
        # in .run().
        # Otherwise, we do the actual shutdown and cleanup.

        if self._state.value > ExecutorState.RUNNING.value:
            LOG.warning(
                "Executor(id=0x%x) is already shuttdown down.", id(self)
            )
            return  # We're already shutting down.
        LOG.info("palaestrAI executor received command to shut down.")
        self._runs_scheduled.clear()
        self._state = ExecutorState.SHUTDOWN

    async def _monitor_state(self):
        known_state = self._state
        while known_state.value == self._state.value:
            try:
                await asyncio.sleep(0.2)
            except asyncio.CancelledError:
                break
        LOG.debug(
            "Executor(id=0x%x) state changed from %s to %s",
            id(self),
            known_state,
            self._state,
        )

    async def _check_major_domo_broker_state(self):
        if (
            self._state != ExecutorState.RUNNING
            or self._broker_process.is_alive()
        ):
            return
        n_broker_checks = 0
        if n_broker_checks == 3:
            LOG.fatal(
                "Executor(id=%s) lost the MajorDomoBroker, "
                "committing seppuku.",
                id(self),
            )
            raise DeadMajorDomoBrokerError()
        else:
            wait_time = 1 + n_broker_checks
            LOG.debug(
                "MajorDomoBroker is not yet online, waiting for" "%s seconds",
                wait_time,
            )
            n_broker_checks += 1
            await asyncio.sleep(wait_time)

    async def _try_start_next_scheduled_experiment(self):
        """Starts all experiments that are scheduled, monitoring the start

        All experiments that are currently scheduled via
        ::`Executor.schedule` are started. This method initializes a new
        ::`RunGovernor`, deploys the experiment to it, signals the
        ::`RunGovernor` to start the experiment and waits for positive
        response to this ::`ExperimentStartRequest`. If no such response
        arrives, the ::`RunGovernor` is killed and the experiment run
        cancelled.

        The method returns when all scheduled experiments have successfully
        started. It does not keep track of the overall experimentation
        process.
        """
        LOG.debug(
            "Executor(id=0x%x) checks whether to start new experiments.",
            id(self),
        )
        if len(self._run_governors) > 0 or len(self._runs_scheduled) == 0:
            return
        experiment = self._runs_scheduled.pop()
        try:
            run_governor_id = await self._deploy_experiment_run(experiment)
            start_experiment_run_task = asyncio.create_task(
                self._start_experiment_run(run_governor_id)
            )
            process_monitor_task = asyncio.create_task(
                self._run_governors[
                    run_governor_id
                ].run_governor_process.join()
            )
            tasks_done, _ = await asyncio.wait(
                {
                    start_experiment_run_task,
                    process_monitor_task,
                },
                return_when=asyncio.FIRST_COMPLETED,
            )
            if (
                start_experiment_run_task in tasks_done
                and start_experiment_run_task.exception()
            ):
                raise start_experiment_run_task.exception()
            if process_monitor_task in tasks_done:
                raise ExperimentRunStartError(
                    self._run_governors[run_governor_id].experiment_run_id,
                    run_governor_id,
                    "No ExperimentStartResponse received",
                )
        except (ExperimentRunStartError, asyncio.CancelledError) as e:
            LOG.fatal(
                "Executor(id=%s) "
                "could not launch ExperimentRun(experiment_id=%s): "
                "%s; killing associated RunGovernor(uid=%s).",
                id(self),
                experiment.uid,
                e,
                e.run_governor_id,
            )
            pcb = self._run_governors[e.run_governor_id]
            pcb.run_governor_process.terminate()
            try:
                await pcb.run_governor_process.join(3)
            except (asyncio.TimeoutError, asyncio.CancelledError):
                if pcb.run_governor_process.is_alive():
                    pcb.run_governor_process.kill()
                    await pcb.run_governor_process.join(3)

    async def execute(self):
        """Executes an experiment run.

        This method starts the whole experiment run execution process.
        It initializes the :class:`RunGovernor` for the experiment run
        and sets up communication. This method returns only if:

        1. The experiment run has terminated successfully;
        2. an error has occurred, in which case an exception is raised;
        3. the user has terminated the process (e.g., by hitting ^C).

        Returns
        -------
        ExecutorState
            The state the executor is now in, either "SHUTDOWN" if
            everything exited normally, or one of the SIG* states if a
            signal was received.
        """
        self._init_signal_handler()
        setproctitle.setproctitle("palaestrAI[Executor]")
        await self._init_logging()
        LOG.info("This is palaestrAI, version %s", __version__)
        self._init_communication()
        self._state = ExecutorState.INITIALIZED

        LOG.debug("Executor(id=0x%x) starting main execution loop", id(self))
        self._state = ExecutorState.RUNNING
        state_change_monitor_task = asyncio.create_task(self._monitor_state())
        while self._state == ExecutorState.RUNNING:
            try:
                await self._check_major_domo_broker_state()
            except DeadMajorDomoBrokerError:
                self._state = ExecutorState.SHUTDOWN
                continue
            start_experiment_task = asyncio.create_task(
                self._try_start_next_scheduled_experiment()
            )
            tasks_done, tasks_pending = await asyncio.wait(
                {state_change_monitor_task, start_experiment_task},
                return_when=asyncio.FIRST_COMPLETED,
            )
            if (
                state_change_monitor_task in tasks_done
                and start_experiment_task in tasks_pending
            ):
                start_experiment_task.cancel()

            LOG.debug(
                "Executor(id=0x%x) checks for finished RunGovernors",
                id(self),
            )
            for pcb in self._run_governors.values():
                try:
                    await pcb.run_governor_process.join(0.1)
                except TimeoutError:
                    pass  # This is actually expected in most cases.
                if pcb.run_governor_process.is_alive():
                    continue
                if pcb.run_governor_process.exitcode != 0:
                    LOG.error("RunGovernor process %s died.", pcb)
            self._run_governors = {
                uid: pcb
                for uid, pcb in self._run_governors.items()
                if pcb.run_governor_process.is_alive()
            }
            LOG.debug(
                "Executor(id=0x%x) has %d active run governors and %d "
                "experiment runs scheduled.",
                id(self),
                len(self._run_governors),
                len(self._runs_scheduled),
            )
            await asyncio.sleep(0.2)
            if (
                self._state == ExecutorState.RUNNING
                and len(self._run_governors) + len(self._runs_scheduled) == 0
            ):
                self._state = ExecutorState.SHUTDOWN
        state_change_monitor_task.cancel()
        await self._shutdown()
        return self._state

    async def _shutdown_all_run_governors(self):
        """Shuts all ::`RunGovernor` instances down, cleaning up

        This method terminates all running ::`RunGovernor` instances. They
        get a nice message first, but are forcefully terminated if they don't
        react. Also, the internal data structures of the ::`Executor` are
        cleaned up.
        """
        for run_gov_uid in self._run_governors:
            pcb = self._run_governors[run_gov_uid]
            if not pcb.run_governor_process.is_alive():
                continue
            LOG.debug(
                "Executor(id=%s) "
                "signalling RunGovernor(uid=%s, run_id=%s) "
                "to shut down.",
                id(self),
                run_gov_uid,
                pcb.experiment_run_id,
            )
            if pcb.experiment_run_id:
                try:
                    await asyncio.wait_for(
                        self.cancel(pcb.experiment_run_id), timeout=15
                    )
                    continue
                except asyncio.TimeoutError:
                    LOG.debug(
                        "Executor(id=%s) has encountered a "
                        "RunGovernor(uid=%s, run_id=%s) "
                        "that seems to be still active, trying to abort. "
                        "Did you hit ^C? Oh, you bad boy...",
                        id(self),
                        pcb.run_governor_id,
                        pcb.experiment_run_id,
                    )
            LOG.warning(
                "Executor(id=0x%x) "
                "could not shut down "
                "RunGovernor(uid=%s, run_id=%s) "
                "orderly.",
                id(self),
                run_gov_uid,
                pcb.experiment_run_id,
            )
            run_governor_pgid = os.getpgid(pcb.run_governor_process.pid)
            pcb.run_governor_process.terminate()
            try:
                await pcb.run_governor_process.join(3)
            except asyncio.TimeoutError:
                pcb.run_governor_process.kill()
            try:
                # Zombies will be shot:
                os.killpg(run_governor_pgid, signal.SIGKILL)
            except ProcessLookupError:
                pass  # Just a shot in the dark.

    async def _shutdown(self):
        LOG.info("palaestrAI executor initiating shutdown procedure")
        await self._shutdown_all_run_governors()
        try:
            pass
            # await self._client.destroy()
        except zmq.error.ZMQError:
            # This can happen on ^C. It's actually not that bad, so we just
            # do a debug log entry here.
            LOG.debug(
                "%s could not send destroy message via MajorDomoClient to "
                "MajorDomoBroker(uri=%s); ignoring that anyways and dragging "
                "on.",
                self,
                self._broker_uri,
            )
        self._broker_process.terminate()
        while self._broker_process.is_alive():
            try:
                await self._broker_process.join(1)
            except asyncio.exceptions.TimeoutError:
                pass  # Give asyncio some time to process other stuff.
        if self._state == ExecutorState.SHUTDOWN:
            self._state = ExecutorState.EXITED
        await self._log_server.stop()

    def __str__(self):
        return "Executor(id=%s)" % id(self)
