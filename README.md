# Summarize Video App

**Summarize Video App** is an Aana application that summarizes a video by extracting transcription from the audio and generating a summary using a Language Model (LLM). This application is a part of the [tutorial](https://mobiusml.github.io/aana_sdk/pages/tutorial/) on how to build multimodal applications with [Aana SDK](https://github.com/mobiusml/aana_sdk).

## Installation

To install the project, follow these steps:

1. Clone the repository.

2. Install the package with Poetry.

The project is managed with [Poetry](https://python-poetry.org/docs/). See the [Poetry installation instructions](https://python-poetry.org/docs/#installation) on how to install it on your system.

It will install the package and all dependencies in a virtual environment.

```bash
poetry install
```

3. Install additional libraries.

For optimal performance, you should also install [PyTorch](https://pytorch.org/get-started/locally/) version >=2.1 appropriate for your system. You can continue directly to the next step, but it will install a default version that may not make optimal use of your system's resources, for example, a GPU or even some SIMD operations. Therefore we recommend choosing your PyTorch package carefully and installing it manually.

Some models use Flash Attention. Install Flash Attention library for better performance. See [flash attention installation instructions](https://github.com/Dao-AILab/flash-attention?tab=readme-ov-file#installation-and-features) for more details and supported GPUs.


4. Activate the Poetry environment.

To activate the Poetry environment, run the following command:

```bash
poetry shell
```

Alternatively, you can run commands in the Poetry environment by prefixing them with `poetry run`. For example:

```bash
poetry run aana deploy aana_summarize_video.app:aana_app
```

5. Run the app.

```bash
aana deploy aana_summarize_video.app:aana_app
```

## Usage

To use the project, follow these steps:

1. Run the app as described in the installation section.

```bash
aana deploy aana_summarize_video.app:aana_app
```

Once the application is running, you will see the message `Deployed successfully.` in the logs. It will also show the URL for the API documentation.

> **⚠️ Warning**
>
> The applications require 1 GPUs to run.
>
> The applications will detect the available GPU automatically but you need to make sure that `CUDA_VISIBLE_DEVICES` is set correctly.
> 
> Sometimes `CUDA_VISIBLE_DEVICES` is set to an empty string and the application will not be able to detect the GPU. Use `unset CUDA_VISIBLE_DEVICES` to unset the variable.
> 
> You can also set the `CUDA_VISIBLE_DEVICES` environment variable to the GPU index you want to use: `export CUDA_VISIBLE_DEVICES=0`.

2. Send a POST request to the app.

```bash
curl -X POST http://127.0.0.1:8000/video/summarize -Fbody='{"video":{"url":"https://www.youtube.com/watch?v=VhJFyyukAzA"}}'
```

See [Tutorial](https://mobiusml.github.io/aana_sdk/pages/tutorial/) for more information.

## Running within Docker
To run the application in a Docker container, we offer a Dockerfile and a docker-compose configuration in the repository. The Aana SDK requires a database for storage and supports both SQLite and PostgreSQL. If you prefer SQLite, you can use just the Dockerfile. For better performance, you can use the docker-compose file, which will automatically set up a PostgreSQL instance alongside the application. 

### Deploying via docker
To successfully run the application within a Docker container, please follow the steps outlined below:

1. Build the Docker Image
Begin by building the Docker image for the application. You can accomplish this by executing the following command in your terminal:

```bash
docker build -t aana_summarize_video:latest --build-arg INSTALL_FLASH_ATTEN=false .
```

This command creates a new Docker image tagged as `aana_summarize_video:latest`, with an optional build argument to skip the installation of Flash Attention.

2. Execute the Docker Container
Once the image is built, you can run the application inside a Docker container using the following command:

```bash
export DB_CONFIG='{"datastore_type": "sqlite", "datastore_config": {"path": "/tmp/db/aana_db.sqlite"}}'
docker run \
    --name aana_summarize_video_app \
    -v ~/aana/tmp:/tmp/aana_data \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    -v ~/aana/db:/tmp/db \
    -e CUDA_VISIBLE_DEVICES=0 \
    -e HF_DATASETS_CACHE=/root/.cache/huggingface \
    -e TMP_DATA_DIR=/tmp/aana_data \
    -e DB_CONFIG=$DB_CONFIG \
    -p 8000:8000 \
    aana_summarize_video:latest
```

**Configuration Details:**

In the above command:

- `--name aana_summarize_video_app`: Assigns a name for the running container for easy reference.

- **Volume Mounts (-v):** Specify directories to share files between your host and the container. 

  - `~/aana/tmp` is mapped to /tmp/aana_data in the container.
  - `~/.cache/huggingface` is used to store Hugging Face model data, ensuring that the cache is preserved between container runs.
  - `~/aana/db` is linked to the SQLite database file.

- **Environment Variables (-e):**

  - `CUDA_VISIBLE_DEVICES=0`: Indicates which GPU device to use, if available.
  - `HF_DATASETS_CACHE`: Specifies the path for caching Hugging Face datasets.
  - `TMP_DATA_DIR`: Sets the temporary data directory for the application.
  - `DB_CONFIG`: Contains the configuration for the database, which by default is set to use SQLite. This configuration can be customized as needed.

### Deploying via docker-compose
This Docker Compose configuration automatically builds the Docker image for your application. If you want to include the flash-atten feature, set INSTALL_FLASH_ATTEN to true during the build process. To deploy the app with PostgreSQL using Docker Compose, follow these steps: 

1. Build the images by running:

```bash
INSTALL_FLASH_ATTEN=false docker-compose build
```

2. Run the containers with:

```bash
CUDA_VISIBLE_DEVICES=0 docker-compose up
```

The application requires one GPU to operate, so you'll need to set `CUDA_VISIBLE_DEVICES` in the command.
The application will be accessible at `http://localhost:8000` in the host server and the PostgreSQL will be accessible via port 15430.
You can check the [docker-compose config](./docker-compose.yaml) to see all available variables you can set for running the application.

**Base Image**
The Dockerfile utilizes the image `nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04`, which includes CUDA and cuDNN necessary for deployment operations. If you plan to run this container on a server that does not have a supported NVIDIA driver, you may need to modify the base image to ensure it functions correctly. Aana requires CUDA version 12.1, cuDNN version 8, and an NVIDIA driver version 525.60.13 or newer.
