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

## Running with Docker

We provide a docker-compose configuration to run the application in a Docker container.

Requirements:

- Docker Engine >= 26.1.0
- Docker Compose >= 1.29.2
- NVIDIA Driver >= 525.60.13

To run the application, simply run the following command:

```bash
docker-compose up
```

The application will be accessible at `http://localhost:8000` on the host server.


> **⚠️ Warning**
>
> The applications require 1 GPUs to run.
>
> The applications will detect the available GPU automatically but you need to make sure that `CUDA_VISIBLE_DEVICES` is set correctly.
> 
> Sometimes `CUDA_VISIBLE_DEVICES` is set to an empty string and the application will not be able to detect the GPU. Use `unset CUDA_VISIBLE_DEVICES` to unset the variable.
> 
> You can also set the `CUDA_VISIBLE_DEVICES` environment variable to the GPU index you want to use: `CUDA_VISIBLE_DEVICES=0 docker-compose up`.


> **💡Tip**
>
> Some models use Flash Attention for better performance. You can set the build argument `INSTALL_FLASH_ATTENTION` to `true` to install Flash Attention. 
>
> ```bash
> INSTALL_FLASH_ATTENTION=true docker-compose build
> ```
>
> After building the image, you can use `docker-compose up` command to run the application.
>
> You can also set the `INSTALL_FLASH_ATTENTION` environment variable to `true` in the `docker-compose.yaml` file.
