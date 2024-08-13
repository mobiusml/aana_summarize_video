# Use NVIDIA CUDA as base image
FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

# Set working directory
WORKDIR /app

# Set environment variables to non-interactive (this prevents some prompts)
ENV DEBIAN_FRONTEND=non-interactive

# Install required libraries, tools, and Python3
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 ffmpeg curl git python3.10 python3-pip nvidia-cuda-toolkit
ENV LD_LIBRARY_PATH=/usr/local/cuda/compat:$LD_LIBRARY_PATH

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Update PATH
RUN echo 'export PATH="/root/.local/bin:$PATH"' >> /root/.bashrc
ENV PATH="/root/.local/bin:$PATH"

# Copy project files into the container
COPY . /app

# Install the package with poetry
RUN poetry install

# Install flash attention
RUN poetry run pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
RUN poetry run pip install flash-attn --no-build-isolation

# Disable buffering for stdout and stderr to get the logs in real time
ENV PYTHONUNBUFFERED=1

# Expose the desired port
EXPOSE 8000

# Run the app
CMD ["poetry", "run", "aana", "deploy", "aana_summarize_video.app:aana_app", "--host", "0.0.0.0"]
