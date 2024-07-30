from aana.api.api_generation import Endpoint
from aana.core.models.video import VideoInput
from aana.deployments.aana_deployment_handle import AanaDeploymentHandle
from aana.deployments.whisper_deployment import WhisperOutput
from aana.integrations.external.yt_dlp import download_video
from aana.processors.remote import run_remote
from aana.processors.video import extract_audio


class TranscribeVideoEndpoint(Endpoint):
    """Transcribe video endpoint."""

    async def initialize(self):
        """Initialize the endpoint."""
        await super().initialize()
        self.asr_handle = await AanaDeploymentHandle.create("asr_deployment")

    async def run(self, video: VideoInput) -> WhisperOutput:
        """Transcribe video."""
        video_obj = await run_remote(download_video)(video_input=video)
        audio = extract_audio(video=video_obj)
        transcription = await self.asr_handle.transcribe(audio=audio)
        return transcription
