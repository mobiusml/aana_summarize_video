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

See [tutorial](https://mobiusml.github.io/aana_sdk/pages/tutorial/) for more information.

## Running within Docker

To execute the project using Docker, you will find both a Dockerfile and a Docker Compose configuration file in the repository. These resources allow you to run the project seamlessly. You have the option to launch it using Docker Compose for a more streamlined approach, or you can opt to use Docker directly. Here’s how you can do both:

### Deploying via docker-compose

```bash
CUDA_VISIBLE_DEVICES=0 docker-compose up
```

The application requires one GPU to operate, so you'll need to set `CUDA_VISIBLE_DEVICES` in the command.
The docker-compose configuration will deploy a PostgreSQL instance alongside the application and establish a connection between them. If you already have a database set up elsewhere, you can modify the docker-compose configuration by removing PostgreSQL and specifying the PostgreSQL address using environment variables. The application will be accessible at `http://localhost:8000` in the host server and the PostgreSQL will be accessible via port 15430.
You can check the [docker-compose config](./docker-compose.yaml) to see all available variables you can set for running the application.

### Deploying via docker

To deploy the application by docker directly follow these steps:

1. Build the docker image by running:

```bash
docker build --no-cache -t aana_summarize_video:latest .
```

2. Run the the image:
```bash
export DB_CONFIG='{"datastore_type":"postgresql","datastore_config":{"host":<PG_HOST>,"port":<PG_PORT>,"user":<PGUSER>,"password":<PG_PASSWORD>,"database":<PG_DB>}}'
docker run --rm -it -v ~/.cache:/root/.cache -e CUDA_VISIBLE_DEVICES=0 -e DB_CONFIG=$DB_CONFIG -p 8000:8000 aana_summarize_video:latest
```

The Dockerfile is currently configured to utilize the base image `nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04`. This particular image integrates CUDA and cuDNN, making it well-suited for applications that require GPU acceleration and deep learning functionalities. However, if you're planning to deploy the container on a server where the installed NVIDIA driver is incompatible with this specific image, you may need to modify the base image. It's essential to choose a version that aligns with the capabilities of the existing driver on your server to ensure optimal performance and functionality. Always verify the compatibility of the CUDA version with your server’s GPU driver to avoid any issues during deployment.
