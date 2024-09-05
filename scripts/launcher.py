import logging
import re

from aind_behavior_services.launcher import Launcher
from aind_behavior_services.session import AindBehaviorSessionModel
from aind_behavior_video_encoding_benchmarks.rig import AindVideoEncodingBenchmarksRig
from aind_behavior_video_encoding_benchmarks.task_logic import (
    AindVideoEncodingBenchmarksTaskLogic,
)


class CustomLauncher(Launcher):
    def _get_experimenter(self) -> list[str]:
        experimenters_input = str(input("Enter experimenter(s):"))
        split = re.split(
            r"[,\s]+", experimenters_input.strip()
        )  # Split using commas, spaces, and control characters as separators
        return split if split != [""] else []

    def run_ui(self):
        try:
            self._print_header()
            self._validate_dependencies()
            subject = "Null"
            self._session_schema = self.session_schema_model(
                experiment="",  # Will be set later
                root_path=str(self.data_dir.resolve())
                if not self.group_by_subject_log
                else str(self.data_dir.resolve() / subject),
                remote_path=self.remote_data_dir,
                subject=subject,
                notes=None,  # Will be set later
                commit_hash=self.repository.head.commit.hexsha,
                allow_dirty_repo=self._debug_mode or self.allow_dirty,
                skip_hardware_validation=self.skip_hardware_validation,
                experiment_version="",  # Will be set later
                experimenter=[],
            )
            self._session_schema.notes = self.prompt_get_notes()
            self._session_schema.experimenter = self._get_experimenter()

            self._task_logic_schema = self._prompt_task_logic_input()
            self._rig_schema = self._prompt_rig_input()
            self._bonsai_visualizer_layout = self._prompt_visualizer_layout_input()

            # Handle some cross-schema references
            self._session_schema.experiment = self._task_logic_schema.name
            self._session_schema.experiment_version = self._task_logic_schema.version

            input("Press enter to start or Control+C to exit...")
            self.pre_run_hook()
            self.run_hook()
            self.post_run_hook()

            for handler in self.logger.handlers:
                if isinstance(handler, logging.FileHandler):
                    self.logger.info("File handler found in logger. Closing and copying to session directory.")
                    handler.close()

            if self.session_directory is not None:
                self._copy_tmp_folder(self.session_directory / "Behavior" / "Logs")

            self.logger.info("All hooks finished. Launcher closing.")
            self._exit(0)

        except KeyboardInterrupt:
            print("Exiting!")
            return


if __name__ == "__main__":
    launcher_cli = CustomLauncher(
        rig_schema_model=AindVideoEncodingBenchmarksRig,
        session_schema_model=AindBehaviorSessionModel,
        task_logic_schema_model=AindVideoEncodingBenchmarksTaskLogic,
        data_dir=r"C:/Data",
        config_library_dir=r"C:\Users\bruno.cruz\OneDrive - Allen Institute\Desktop\AindBehavior.db\AindVideoEncodingBenchmarks",
        bonsai_workflow=r"./src/main.bonsai",
    )
    launcher_cli.run()
