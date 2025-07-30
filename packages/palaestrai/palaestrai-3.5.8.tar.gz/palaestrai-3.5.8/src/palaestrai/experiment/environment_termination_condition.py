from __future__ import annotations
from typing import Optional, Union, Any, Tuple

from palaestrai.core.protocol import (
    EnvironmentUpdateResponse,
    SimulationControllerTerminationRequest,
)
from palaestrai.experiment import TerminationCondition, RunGovernor
from palaestrai.types import SimulationFlowControl


class EnvironmentTerminationCondition(TerminationCondition):
    """Terminates the current phase when an ::`~Environment` terminates

    This :class:`~TerminationCondition` examines updates from an
    :class:`~Environment` and checks whether the environment itself signals
    termination. When an environment termination signal is received this
    :class:`~TerminationCondition` the current **episode**.

    Example
    -------

    The following snipped is a shortened example from palaestrAI’s experiment
    definition in which an episode is ended when the environment terminates::

        definitions:
          # (Definitions of environment, agents and phase_config
          are omitted.)
          simulation:
            vanilla:
                name: palaestrai.simulation:Vanilla
                conditions:
                  - name: palaestrai.simulation:EnvironmentTerminationCondition
                    params: {}
        # (Definition of the run configuration is also omitted.)
    """

    def phase_flow_control(
        self,
        run_governor: RunGovernor,
        message: Optional[Union[SimulationControllerTerminationRequest]],
    ) -> Tuple[SimulationFlowControl, Any]:
        if not isinstance(message, SimulationControllerTerminationRequest):
            return SimulationFlowControl.CONTINUE, None
        return (message.flow_control_data[self.__class__.__name__][0]), None

    def check_termination(self, message, component=None):
        """
        Checks for environment termination.

        Parameters
        ----------
        message : Any
            Examines :class:`~EnvironmentUpdateResponse` messages for
            ::`~EnvironmentUpdateResponse.is_teminal`.
        component : Any
            unused

        Returns
        -------
        bool
            ``True`` if ``message.is_terminal``.
        """
        return isinstance(message, EnvironmentUpdateResponse) and message.done
