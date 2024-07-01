from aind_behavior_services.launcher import LauncherCli
from aind_behavior_services.session import AindBehaviorSessionModel
from aind_behavior_video_encoding_benchmarks.rig import AindVideoEncodingBenchmarksRig
from aind_behavior_video_encoding_benchmarks.task_logic import AindVideoEncodingBenchmarksTaskLogic

if __name__ == "__main__":
    launcher_cli = LauncherCli(
        rig_schema=AindVideoEncodingBenchmarksRig,
        session_schema=AindBehaviorSessionModel,
        task_logic_schema=AindVideoEncodingBenchmarksTaskLogic,
        data_dir=r"C:/Data",
        remote_data_dir=r"\\allen\aind\scratch\video-encoding-benchmarks\data",
        config_library_dir=r"\\allen\aind\scratch\AindBehavior.db\AindVideoEncodingBenchmarks",
        workflow=r"./src/main.bonsai",
    )
    launcher_cli.run()
