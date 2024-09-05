from __future__ import annotations

from typing import Literal

from aind_behavior_services.task_logic import AindBehaviorTaskLogicModel, TaskParameters
from pydantic import Field

__version__ = "0.1.1"


class AindVideoEncodingBenchmarksTaskParameters(TaskParameters):
    save_raw_video: bool = Field(
        default=False,
        description="For each video-writer object, will also save the RAW encoded video to disk. Use at your own risk.",
    )


class AindVideoEncodingBenchmarksTaskLogic(AindBehaviorTaskLogicModel):
    version: Literal[__version__] = __version__
    name: str = Field(
        default="AindVideoEncodingBenchmarks",
        description="Name of the task logic",
        frozen=True,
    )
    task_parameters: AindVideoEncodingBenchmarksTaskParameters = Field(..., description="Parameters of the task logic")
