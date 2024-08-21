# Aind.Behavior.VideoEncodingBenchmarks

A repository with code for benchmarking online video acquisition/encoding pipelines


## Getting started

The easiest way to get started is to clone this repository and run the `deploy.cmd` script. This script will install the necessary dependencies. If you use any python-dependent scripts (e.g. generate valid schema json files or use the launcher script), make sure to run them from an activated environment (`./.venv` directory in the root of the repo).

To run the benchmark workflow you will need a valid set of schemas. Examples of how to generate these can be found in the `./examples/examples.py` file. For the most part, you will only need to generate the rig schema, as the others can be automatically generated using the `Launcher.cmd` script. In summary:

1. Generate the rig schema by adapting the script in `./examples/examples.py`. You should make a copy of the example and modify it outside the repository directory, otherwise any untracked changes / new files in the local repository will flag it as "dirty" and the benchmarks will not be allowed to run.
2. Once the rig schema is defined in the `.py` file, run the script to generate a valid `.json` file that will be the input to the benchmark workflow.
3. Copy and Paste the generated schema (i.e. the `.json` file) to the target config folder (by default `\\allen\aind\scratch\AindBehavior.db\AindVideoEncodingBenchmarks\Rig\<COMPUTERNAME>\<RIG_FILE>.json`)
4. Run the `./scripts/Launcher.cmd`, from the root of the repository, and follow the prompt.
5. Once Bonsai is running, double-click the `UserInterface` operator to open the GUI
6. Click Start (Stop) to start (stop) the benchmark workflow.
7. Once the workflow stops, if a `remote_data_dir` was specified in the `Launcher` a RoboCopy routine will be executed to copy the data to the specified location.

Alternatively, you can run the `main.bonsai` script directly using the following command from the root of the repository:

```cmd
"./bonsai/bonsai.exe" "./src/main.bonsai" -p TaskLogicPath="<PATH_TO_TASK_LOGIC.json>" -p RigPath="<PATH_TO_RIG.json>" -p SessionPath="<PATH_TO_SESSION.json>"
```

where `<PATH_TO_TASK_LOGIC.json>`, `<PATH_TO_RIG.json>`, and `<PATH_TO_SESSION.json>` are the paths to the task logic, rig, and session schemas, respectively.



---

## General instructions

This repository follows the project structure laid out in the [Aind.Behavior.Services repository](https://github.com/AllenNeuralDynamics/Aind.Behavior.Services).

---

## Deployment

Deployment instructions can be found [here](https://github.com/AllenNeuralDynamics/Aind.Behavior.Services?tab=readme-ov-file#deployment).

Specifically, Ffmpeg and CUDA support must be installed on the computer.

---

## Prerequisites

Pre-requisites for running the project can be found [here](https://github.com/AllenNeuralDynamics/Aind.Behavior.Services?tab=readme-ov-file#prerequisites).

---

## Regenerating schemas

Instructions for regenerating schemas can be found [here](https://github.com/AllenNeuralDynamics/Aind.Behavior.Services?tab=readme-ov-file#regenerating-schemas).
