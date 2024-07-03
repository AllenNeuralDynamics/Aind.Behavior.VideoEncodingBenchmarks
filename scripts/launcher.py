import os
import re
from typing import Optional, Type

from aind_behavior_services.launcher import Launcher, LauncherCli, open_bonsai_process
from aind_behavior_services.session import AindBehaviorSessionModel
from aind_behavior_video_encoding_benchmarks.rig import AindVideoEncodingBenchmarksRig
from aind_behavior_video_encoding_benchmarks.task_logic import (
    AindVideoEncodingBenchmarksTaskLogic,
    AindVideoEncodingBenchmarksTaskParameters,
)
from typing_extensions import override


class CustomLauncherCli(LauncherCli):

    @override
    def __init__(
        self,
        rig_schema: Type[AindVideoEncodingBenchmarksRig],
        session_schema: Type[AindBehaviorSessionModel],
        task_logic_schema: Type[AindVideoEncodingBenchmarksTaskLogic],
        data_dir: os.PathLike | str,
        config_library_dir: os.PathLike | str,
        workflow: os.PathLike | str,
        remote_data_dir: Optional[os.PathLike | str] = None,
        repository_dir: Optional[os.PathLike | str] = None,
        **launcher_kwargs,
    ) -> None:

        parser = self._get_default_arg_parser()
        args, _ = parser.parse_known_args()

        # optional parameters that override the defaults
        data_dir = args.data_dir if args.data_dir is not None else data_dir
        workflow = args.workflow if args.workflow is not None else workflow
        remote_data_dir = args.remote_data_dir if args.remote_data_dir is not None else remote_data_dir
        repository_dir = args.repository_dir if args.repository_dir is not None else repository_dir
        config_library_dir = args.config_library_dir if args.config_library_dir is not None else config_library_dir

        # flag-like parameter
        force_create_directories = args.force_create_directories
        dev_mode = args.dev_mode
        bonsai_is_editor_mode = args.bonsai_is_editor_mode
        bonsai_is_start_flag = args.bonsai_is_start_flag
        allow_dirty_repo = args.allow_dirty_repo
        skip_hardware_validation = args.skip_hardware_validation

        self.launcher = CustomLauncher(
            rig_schema=rig_schema,
            session_schema=session_schema,
            task_logic_schema=task_logic_schema,
            data_dir=data_dir,
            remote_data_dir=remote_data_dir,
            repository_dir=repository_dir,
            config_library_dir=config_library_dir,
            workflow=workflow,
            dev_mode=dev_mode,
            bonsai_is_editor_mode=bonsai_is_editor_mode,
            bonsai_is_start_flag=bonsai_is_start_flag,
            allow_dirty_repo=allow_dirty_repo,
            skip_hardware_validation=skip_hardware_validation,
            **launcher_kwargs,
        )

        if force_create_directories:
            self.make_folder_structure()


class CustomLauncher(Launcher):

    def _get_experimenter(self) -> list[str]:
        experimenters_input = str(input("Enter notes:"))
        split = re.split(
            r"[,\s]+", experimenters_input.strip()
        )  # Split using commas, spaces, and control characters as separators
        return split if split != [""] else []

    def run(self):
        try:
            self._print_header()
            self._validate_dependencies()
            session = AindBehaviorSessionModel(
                experiment="",  # Will be set later
                root_path=self.data_dir,
                remote_path=self.remote_data_dir,
                subject="Null",
                notes=None,  # Will be set later
                commit_hash=self.repository.head.commit.hexsha,
                allow_dirty_repo=self._dev_mode or self.allow_dirty_repo,
                skip_hardware_validation=self.skip_hardware_validation,
                experiment_version="",  # Will be set later
                experimenter=[],
            )
            session.notes = self._get_notes()
            session.experimenter = self._get_experimenter()

            task_logic = AindVideoEncodingBenchmarksTaskLogic(task_parameters=AindVideoEncodingBenchmarksTaskParameters)
            rig = self.prompt_rig_input()
            bonsai_visualizer_layout = None

            # Handle some cross-schema references
            session.experiment = task_logic.name
            session.experiment_version = task_logic.version

            input("Press enter to launch Bonsai or Control+C to exit...")

            additional_properties = {
                "TaskLogicPath": os.path.abspath(self.save_temp_model(model=task_logic, folder=self.temp_dir)),
                "SessionPath": os.path.abspath(self.save_temp_model(model=session, folder=self.temp_dir)),
                "RigPath": os.path.abspath(self.save_temp_model(model=rig, folder=self.temp_dir)),
            }

            proc = open_bonsai_process(
                bonsai_exe=self.bonsai_executable,
                workflow_file=self.default_workflow,
                additional_properties=additional_properties,
                layout=bonsai_visualizer_layout,
                log_file_name=os.path.join(
                    session.root_path, session.subject, f"{session.subject}_{session.date.strftime('%Y%m%dT%H%M%S')}"
                ),
                is_editor_mode=self.bonsai_is_editor_mode,
                is_start_flag=self.bonsai_is_start_flag,
                cwd=self._cwd,
                print_cmd=self._dev_mode,
            )
            print("Bonsai process running...")
            ret = proc.wait()
            print(f"Bonsai process finished with return code {ret}.")

        except KeyboardInterrupt:
            print("Exiting!")
            return


if __name__ == "__main__":
    launcher_cli = CustomLauncherCli(
        rig_schema=AindVideoEncodingBenchmarksRig,
        session_schema=AindBehaviorSessionModel,
        task_logic_schema=AindVideoEncodingBenchmarksTaskLogic,
        data_dir=r"C:/Data",
        remote_data_dir=r"\\allen\aind\scratch\video-encoding-benchmarks\data",
        config_library_dir=r"\\allen\aind\scratch\AindBehavior.db\AindVideoEncodingBenchmarks",
        workflow=r"./src/main.bonsai",
    )
    launcher_cli.run()
