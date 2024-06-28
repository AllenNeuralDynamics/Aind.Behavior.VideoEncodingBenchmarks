import datetime
import os

import aind_behavior_services.rig as rig
from aind_behavior_services.session import AindBehaviorSessionModel
from aind_behavior_video_encoding_benchmarks.rig import AindVideoEncodingBenchmarksRig
from aind_behavior_video_encoding_benchmarks.task_logic import (
    AindVideoEncodingBenchmarksTaskLogic,
    AindVideoEncodingBenchmarksTaskParameters,
)


def main(path_seed: str = "./local/{schema}.json"):

    this_session = AindBehaviorSessionModel(
        date=datetime.datetime.now(tz=datetime.timezone.utc),
        experiment="AindVideoEncodingBenchmarks",
        root_path="c://",
        remote_path=None,  # change to a remote valid path to trigger robocopy at the end of the session
        subject="Test",
        notes="test session",
        experiment_version="0.0.0",
        allow_dirty_repo=False,
        skip_hardware_validation=False,
        experimenter=["Foo", "Bar"],
    )

    this_task = AindVideoEncodingBenchmarksTaskLogic(task_parameters=AindVideoEncodingBenchmarksTaskParameters())

    video_writer = rig.VideoWriterFfmpeg(
        frame_rate=120,
        container_extension="mp4",
        output_arguments="-c:v hevc_nvenc -pix_fmt x2rgb10le -color_range full -tune hq -preset p3 -rc vbr -cq 16 -rc-lookahead 56 -temporal-aq 1 -qmin 0 -qmax 10", # noqa: E501
    )

    this_rig = AindVideoEncodingBenchmarksRig(
        rig_name="this_rig",
        triggered_camera_controller_0=rig.CameraController[rig.SpinnakerCamera](
            frame_rate=120,
            cameras={
                "FaceCamera": rig.SpinnakerCamera(
                    serial_number="SerialNumber", binning=1, exposure=5000, gain=0, video_writer=video_writer
                ),
                "SideCamera": rig.SpinnakerCamera(
                    serial_number="SerialNumber", binning=1, exposure=5000, gain=0, video_writer=video_writer
                ),
            },
        ),
        triggered_camera_controller_1=None,
        harp_behavior=rig.HarpBehavior(port_name="COM3"),
        harp_clock_generator=rig.HarpClockGenerator(port_name="COM6"),
    )

    os.makedirs(os.path.dirname(path_seed), exist_ok=True)

    models = [this_session, this_rig, this_task]

    for model in models:
        with open(path_seed.format(schema=model.__class__.__name__), "w", encoding="utf-8") as f:
            f.write(model.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
