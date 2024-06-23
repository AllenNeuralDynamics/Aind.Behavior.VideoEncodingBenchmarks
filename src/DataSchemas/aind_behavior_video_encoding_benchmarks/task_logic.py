from __future__ import annotations

from typing import Literal

from aind_behavior_services.task_logic import AindBehaviorTaskLogicModel, TaskParameters
from pydantic import Field

__version__ = "0.1.0"


class AindVideoEncodingBenchmarksTaskParameters(TaskParameters):
    pass


class AindVideoEncodingBenchmarksTaskLogic(AindBehaviorTaskLogicModel):
    version: Literal[__version__] = __version__
    name: str = Field(default="AindVideoEncodingBenchmarks", description="Name of the task logic", frozen=True)
    task_parameters: AindVideoEncodingBenchmarksTaskParameters = Field(..., description="Parameters of the task logic")
