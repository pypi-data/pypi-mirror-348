"""Defines the initial state (baseline) of an  initialized ::`Environment`."""

from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING, Any, List

from palaestrai.types import SimTime

if TYPE_CHECKING:
    from palaestrai.agent import SensorInformation, ActuatorInformation


@dataclasses.dataclass
class EnvironmentBaseline:
    """An :class:`~Environment`'s baseline after initializing

    This data class contains data about an environment after it has been
    started, but no actor has acted yet. It contains the sensors/actuator
    available, initial values for sensors, as well as the starting time in
    the environment.

    Attributes
    ----------
    sensors_available : List[SensorInformation]
        Sensors available in the environment, along with initial readings
    actuators_available : List[ActuatorInformation]
        Actuators available
    simtime : palaestrai.types.SimTime (default: SimTime(simtime_ticks=1))
        Environment starting time
    static_world_model : Any
        Any piece of static model the world can publish. The world model
        should be complete in the sense that any further update of the
        environment can be used to also update palaestrAI's world view through
        this model. Supplying the model is optional, but helpful.
    """

    sensors_available: List[SensorInformation]
    actuators_available: List[ActuatorInformation]
    simtime: SimTime = dataclasses.field(
        default_factory=lambda: SimTime(
            simtime_ticks=1, simtime_timestamp=None
        )
    )
    static_world_model: Any = None
