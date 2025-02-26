from pathlib import Path
from typing import Optional

import aind_behavior_experiment_launcher.launcher.behavior_launcher as behavior_launcher
from aind_behavior_experiment_launcher.apps import BonsaiApp
from aind_behavior_experiment_launcher.resource_monitor import (
    ResourceMonitor,
    available_storage_constraint_factory,
    remote_dir_exists_constraint_factory,
)
from aind_behavior_experiment_launcher.ui_helper import prompt_field_from_input
from aind_behavior_services.session import AindBehaviorSessionModel
from pydantic import ValidationError
from typing_extensions import override

from aind_behavior_video_encoding_benchmarks.rig import AindVideoEncodingBenchmarksRig
from aind_behavior_video_encoding_benchmarks.task_logic import (
    AindVideoEncodingBenchmarksTaskLogic,
    AindVideoEncodingBenchmarksTaskParameters,
)


class AindVideoEncodingBenchmarksLauncher(
    behavior_launcher.BehaviorLauncher[
        AindVideoEncodingBenchmarksRig, AindBehaviorSessionModel, AindVideoEncodingBenchmarksTaskLogic
    ]
):
    @override
    def _prompt_session_input(self, directory: Optional[str] = None) -> AindBehaviorSessionModel:
        experimenter = self._ui_helper.prompt_experimenter(strict=True)
        subject = input("Enter subject name: [defaults to 00000]")
        if subject == "":
            subject = "00000"
        notes = self._ui_helper.prompt_get_notes()

        return self.session_schema_model(
            experiment="",  # Will be set later
            root_path=str(self.data_dir.resolve())
            if not self.group_by_subject_log
            else str(self.data_dir.resolve() / subject),
            subject=subject,
            notes=notes,
            experimenter=experimenter if experimenter is not None else [],
            commit_hash=self.repository.head.commit.hexsha,
            allow_dirty_repo=self._debug_mode or self.allow_dirty,
            skip_hardware_validation=self.skip_hardware_validation,
            experiment_version="",  # Will be set later
        )

    @override
    def _prompt_task_logic_input(self, *args, **kwargs) -> AindVideoEncodingBenchmarksTaskLogic:
        save_raw = None
        while save_raw is None:
            try:
                save_raw = prompt_field_from_input(
                    AindVideoEncodingBenchmarksTaskParameters, "save_raw_video", default=False
                )
            except ValidationError as e:
                self._logger.error("Failed to parse input: %s", e)
            else:
                self._logger.info("save_raw_video set to: %s", save_raw)
        return AindVideoEncodingBenchmarksTaskLogic(
            task_parameters=AindVideoEncodingBenchmarksTaskParameters(save_raw_video=save_raw)
        )


def make_launcher() -> AindVideoEncodingBenchmarksLauncher:
    data_dir = r"C:/Data"
    remote_dir = Path(r"\\allen\aind\scratch\video-encoding-benchmarks\data")
    srv = behavior_launcher.BehaviorServicesFactoryManager()
    srv.attach_bonsai_app(BonsaiApp(r"./src/main.bonsai"))
    srv.attach_data_transfer(behavior_launcher.robocopy_data_transfer_factory(Path(remote_dir)))
    srv.attach_resource_monitor(
        ResourceMonitor(
            constrains=[
                available_storage_constraint_factory(data_dir, 2e11),
                remote_dir_exists_constraint_factory(Path(remote_dir)),
            ]
        )
    )

    return AindVideoEncodingBenchmarksLauncher(
        rig_schema_model=AindVideoEncodingBenchmarksRig,
        session_schema_model=AindBehaviorSessionModel,
        task_logic_schema_model=AindVideoEncodingBenchmarksTaskLogic,
        data_dir=data_dir,
        config_library_dir=r"\\allen\aind\scratch\AindBehavior.db\AindVideoEncodingBenchmarks",
        temp_dir=r"./local/.temp",
        allow_dirty=False,
        skip_hardware_validation=False,
        debug_mode=False,
        group_by_subject_log=True,
        services=srv,
        validate_init=True,
    )


def main():
    launcher = make_launcher()
    launcher.main()
    return None


if __name__ == "__main__":
    main()
