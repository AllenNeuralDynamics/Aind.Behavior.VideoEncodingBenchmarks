# Aind.Behavior.VideoEncodingBenchmarks

A repository with code for benchmarking online video acquisition/encoding pipelines


## Getting started

The easiest way to get started is to clone this repository and run the `deploy.cmd` script. This script will install the necessary dependencies.

To run the benchmark workflow you will need a valid set of schemas. Examples of how to generate these can be found in the `./examples/examples.py` file. For the most part, you will only need to generate the rig schema, as the others can be automatically generated using the `Launcher.cmd` script. In summary:

1. Generate the rig schema by adapting the script in `./examples/examples.py`.
2. Copy and Paste the generated schema to the target config folder (by default `\\allen\aind\scratch\AindBehavior.db\AindVideoEncodingBenchmarks\Rig\<COMPUTERNAME>\<RIG_FILE>.json`)
3. Run the `Launcher.cmd` and follow the prompt.
4. Once Bonsai is running, double-click the `ExperimentalControlUI` operator to open the GUI
5. Click Start (Stop) to start (stop) the benchmark workflow.
6. Once the workflow stops, if a `remote_data_dir` was specified in the `Launcher` a Robocopy routing will be executed to copy the data to the specified location.



---

## General instructions

This repository follows the project structure laid out in the [Aind.Behavior.Services repository](https://github.com/AllenNeuralDynamics/Aind.Behavior.Services).

---

## Deployment

Deployment instructions can be found [here](https://github.com/AllenNeuralDynamics/Aind.Behavior.Services?tab=readme-ov-file#deployment).

---

## Prerequisites

Pre-requisites for running the project can be found [here](https://github.com/AllenNeuralDynamics/Aind.Behavior.Services?tab=readme-ov-file#prerequisites).

---

## Regenerating schemas

Instructions for regenerating schemas can be found [here](https://github.com/AllenNeuralDynamics/Aind.Behavior.Services?tab=readme-ov-file#regenerating-schemas).