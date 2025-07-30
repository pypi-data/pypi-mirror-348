from __future__ import annotations

import typing
from typing import Union, List

from palaestrai.agent import (
    SensorInformation,
    ActuatorInformation,
    RewardInformation,
)
from palaestrai.environment import (
    Environment,
    EnvironmentBaseline,
    EnvironmentState,
)
from palaestrai.types import SimTime, Discrete


class CrashingEnvironment(Environment):
    def start_environment(
        self,
    ) -> Union[
        EnvironmentBaseline,
        typing.Tuple[List[SensorInformation], List[ActuatorInformation]],
    ]:
        return EnvironmentBaseline(
            sensors_available=[
                SensorInformation(uid="S1", space=Discrete(1), value=0)
            ],
            actuators_available=[
                ActuatorInformation(uid="A1", space=Discrete(1), value=0)
            ],
            simtime=SimTime(simtime_ticks=0),
            static_world_model=None,
        )

    def update(self, actuators: List[ActuatorInformation]) -> Union[
        EnvironmentState,
        typing.Tuple[List[SensorInformation], List[RewardInformation], bool],
    ]:
        raise RuntimeError("Mwaaaahhhrgh!!")
