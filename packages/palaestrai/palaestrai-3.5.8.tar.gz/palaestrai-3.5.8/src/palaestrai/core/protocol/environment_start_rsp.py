from __future__ import annotations
from typing import TYPE_CHECKING, Any, List

from dataclasses import dataclass, field
from datetime import datetime

from palaestrai.types.simtime import SimTime

if TYPE_CHECKING:
    from palaestrai.agent import SensorInformation, ActuatorInformation


@dataclass
class EnvironmentStartResponse:
    """Notifies a ::`SimulationController` that an ::`Environment` has started.

    * Sender: A :class:`Environment` after starting
    * Receiver: The :class:`SimulationController`

    sender_environment : str
        The ID of the answering :class:`Environment` (or derived a class)
    receiver_simulation_controller : str
        The ID of the requesting :class:`SimulationController` (or a derived
        class)
    experiment_run_id : str
        ID of the current experiment run this environment participates in
    experiment_run_instance_id : str
        ID of the ::`ExperimentRun` object instance
    experiment_run_phase : int
        Current phase number of the experiment run
    sensors: List[SensorInformation]
        A list of available sensors with initial readings
    actuators: List[ActuatorInformation]
        A list of all actuators available from the sending environment
    static_model : Any, default: None
        The static model of the environment (if given); see
        :py:class:`EnvironmentBaseline` for details.
    simtime : SimTime (default: SimTime(simtime_ticks=1))
        Environment in-simulation starting time
    walltime : datetime (default: `datetime.now()`)
        The time the message was created
    """

    sender_environment: str
    receiver_simulation_controller: str
    experiment_run_id: str
    experiment_run_instance_id: str
    experiment_run_phase: int
    sensors: List[SensorInformation]
    actuators: List[ActuatorInformation]
    static_model: Any = None
    simtime: SimTime = field(
        default_factory=lambda: SimTime(
            simtime_ticks=1, simtime_timestamp=None
        )
    )
    walltime: datetime = field(default_factory=datetime.now)

    @property
    def sender(self):
        return self.sender_environment

    @property
    def receiver(self):
        return self.receiver_simulation_controller
