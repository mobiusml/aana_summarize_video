from transformers import BitsAndBytesConfig
from aana.deployments.hf_text_generation_deployment import (
    HfTextGenerationConfig,
    HfTextGenerationDeployment,
)
from aana.deployments.whisper_deployment import (
    WhisperComputeType,
    WhisperConfig,
    WhisperDeployment,
    WhisperModelSize,
)

asr_deployment = WhisperDeployment.options(
    num_replicas=1,
    ray_actor_options={"num_gpus": 0.25},
    user_config=WhisperConfig(
        model_size=WhisperModelSize.MEDIUM,
        compute_type=WhisperComputeType.FLOAT16,
    ).model_dump(mode="json"),
)

llm_deployment = HfTextGenerationDeployment.options(
    num_replicas=1,
    ray_actor_options={"num_gpus": 0.25},
    user_config=HfTextGenerationConfig(
        model_id="microsoft/Phi-3-mini-4k-instruct",
        model_kwargs={
            "trust_remote_code": True,
            "quantization_config": BitsAndBytesConfig(
                load_in_8bit=False, load_in_4bit=True
            ),
        },
    ).model_dump(mode="json"),
)


deployments: list[dict] = [
    {"name": "asr_deployment", "instance": asr_deployment},
    {"name": "llm_deployment", "instance": llm_deployment},
]
