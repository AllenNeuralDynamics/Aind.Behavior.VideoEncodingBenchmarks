# Import core types
from __future__ import annotations

# Import core types
from typing import Literal, Optional

import aind_behavior_services.rig as rig
from aind_behavior_services.rig import AindBehaviorRigModel
from pydantic import Field

__version__ = "0.1.0"


class AindVideoEncodingBenchmarksRig(AindBehaviorRigModel):
    version: Literal[__version__] = __version__
    triggered_camera_controller_1: rig.CameraController[rig.SpinnakerCamera] = Field(
        ..., description="Required camera controller to triggered cameras. Will use Camera0 register as a trigger."
    )
    triggered_camera_controller_2: Optional[rig.CameraController[rig.SpinnakerCamera]] = Field(
        default=None,
        description="Optional camera controller to triggered cameras. Will use Camera1 register as a trigger.",
    )
    harp_behavior: rig.HarpBehavior = Field(
        ..., description="Harp behavior board. Will be the source of triggers for the two camera controllers."
    )
    harp_clock_generator: rig.HarpClockGenerator = Field(..., description="Harp clock generator.")
