from pathlib import Path
from typing import Optional

from aind_behavior_services.launcher import Launcher, TSession, app_service, resource_monitor_service, services
from aind_behavior_services.session import AindBehaviorSessionModel
from aind_behavior_video_encoding_benchmarks.rig import AindVideoEncodingBenchmarksRig
from aind_behavior_video_encoding_benchmarks.task_logic import (
    AindVideoEncodingBenchmarksTaskLogic,
)


class CustomLauncher(Launcher):
    def _prompt_session_input(self, directory: Optional[str] = None) -> TSession:
        subject = input("Enter subject name:")
        if subject == "":
            subject = "00000"
        notes = self._ui_helper.prompt_get_notes()

        return self.session_schema_model(
            experiment="",  # Will be set later
            root_path=str(self.data_dir.resolve())
            if not self.group_by_subject_log
            else str(self.data_dir.resolve() / subject),
            remote_path=str(self.remote_data_dir.resolve()) if self.remote_data_dir is not None else None,
            subject=subject,
            notes=notes,
            commit_hash=self.repository.head.commit.hexsha,
            allow_dirty_repo=self._debug_mode or self.allow_dirty,
            skip_hardware_validation=self.skip_hardware_validation,
            experiment_version="",  # Will be set later
        )


if __name__ == "__main__":
    data_dir = Path(r"C:/Data")

    _services = services.Services(
        resource_monitor=resource_monitor_service.ResourceMonitor(
            logger=None,
            constrains=[resource_monitor_service.available_storage_constraint_factory(drive="C:/", min_bytes=2e9)],
        ),
        app=app_service.BonsaiApp(r"./src/main.bonsai"),
    )

    launcher = CustomLauncher(
        rig_schema_model=AindVideoEncodingBenchmarksRig,
        session_schema_model=AindBehaviorSessionModel,
        task_logic_schema_model=AindVideoEncodingBenchmarksTaskLogic,
        data_dir=data_dir,
        config_library_dir=Path(r"\\allen\aind\scratch\AindBehavior.db\AindVideoEncodingBenchmarks"),
        skip_hardware_validation=True,
        allow_dirty=True,
        group_by_subject_log=True,
        services=_services,
    )
    launcher()
