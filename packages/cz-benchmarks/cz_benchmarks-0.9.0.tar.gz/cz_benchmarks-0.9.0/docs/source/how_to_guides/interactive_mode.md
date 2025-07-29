# Running a Docker Container in Interactive Mode

This guide explains how to launch an interactive docker container with cz-benchmarks and run benchmarks for a model.

## Command Line Flags

The script `scripts/run_docker.sh` is used to launch the container and accepts the following command line flags:

- `-m, --model-name MODEL_NAME`: (Required) Set the model name (Geneformer, scGenePT, scGPT, scVI, UCE). Model names are case-insensitive and will be converted to lowercase internally. This also determines which docker image to use.
- `-h, --help`: Display usage information and exit.

Example:
```bash
bash scripts/run_docker.sh -m MODEL_NAME
```

## User Defined Configuration

The script also includes user-configurable variables at the top of the file:

### Mount Paths
- `DATASETS_CACHE_PATH`: Path to the cache directory containing datasets. Default: `${HOME}/.cz-benchmarks/datasets`
- `MODEL_WEIGHTS_CACHE_PATH`: Path to the cache directory for model weights. Default: `${HOME}/.cz-benchmarks/weights`
- `DEVELOPMENT_CODE_PATH`: Path to the workstation development code. Default: `$(pwd)`. 
- `EXAMPLES_CODE_PATH`: Path to the examples directory. Default: `$(pwd)/examples`
- `MOUNT_FRAMEWORK_CODE`: Whether to mount the framework code. Note: the examples directory is always mounted in interactive mode, while mounting the code directory is optional. Options: `true` or `false`.

### Container Execution Settings
- `BUILD_DEV_CONTAINER`: true to use prebuilt container from AWS ECR, false to build a container with development code.
- `EVAL_CMD`: Command to execute when the container starts (e.g. `bash`, `python3 -u examples/example_interactive.py`, etc.). See inline comments in `run_docker.sh` for more examples.
- `RUN_AS_ROOT`: Whether to run the container as root. Options: `false` (default) or `true`

## Running the Interactive Example

The repository includes two example scripts (`examples/example_interactive.py` and `examples/example_interactive_perturb.py`, for perturbation tasks) that demonstrate how to run various tasks on a dataset with the user-selected model. To use this example:

1. Launch the container with the appropriate model:
   ```bash
   bash scripts/run_docker.sh -m MODEL_NAME
   ```

2. Inside the container, run the example script with one of the following commands:
   
   For perturbation tasks with scGenePT:

   ```bash
   python3 examples/example_interactive_perturb.py
   ```

   For UCE:

   ```bash
   /opt/conda/envs/uce/bin/python -u /app/examples/example_interactive.py
   ```

   Or all other models: 
   
   ```bash
   python3 examples/example_interactive.py
   ```

The example script will:

- Download the specified dataset(s)
- Evaluate the dataset(s) with the model
- Execute tasks
- Print the results of each task

## Additional Notes

- The container has GPU support enabled by default and is configured with appropriate memory settings
- The script validates that all required directories exist before starting the container and that a valid model is provided
- The script will automatically ensure the appropriate container is downloaded and current
- When using AWS ECR images, the script automatically handles image pulling

## Limitations

- Each model is provided in a separate Docker container, thus limiting this method to a single model per container
- Running multiple models can be accomplished by launching the docker run script for each model
