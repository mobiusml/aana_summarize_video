from typing import Annotated, TypedDict

from aana.api.api_generation import Endpoint
from aana.core.models.chat import ChatDialog, ChatMessage
from aana.core.models.video import VideoInput
from aana.deployments.aana_deployment_handle import AanaDeploymentHandle
from aana.integrations.external.yt_dlp import download_video
from aana.processors.remote import run_remote
from aana.processors.video import extract_audio
from pydantic import Field


class SummarizeVideoEndpointOutput(TypedDict):
    """Summarize video endpoint output."""

    summary: Annotated[str, Field(description="The summary of the video.")]


class SummarizeVideoEndpoint(Endpoint):
    """Summarize video endpoint."""

    async def initialize(self):
        """Initialize the endpoint."""
        await super().initialize()
        self.asr_handle = await AanaDeploymentHandle.create("asr_deployment")
        self.llm_handle = await AanaDeploymentHandle.create("llm_deployment")

    async def run(self, video: VideoInput) -> SummarizeVideoEndpointOutput:
        """Summarize video."""
        video_obj = await run_remote(download_video)(video_input=video)
        audio = extract_audio(video=video_obj)
        transcription = await self.asr_handle.transcribe(audio=audio)
        transcription_text = transcription["transcription"].text
        dialog = ChatDialog(
            messages=[
                ChatMessage(
                    role="system",
                    content="You are a helpful assistant that can summarize audio transcripts.",
                ),
                ChatMessage(
                    role="user",
                    content=f"Summarize the following video transcript into a list of bullet points: {transcription_text}",
                ),
            ]
        )
        summary_response = await self.llm_handle.chat(dialog=dialog)
        summary_message: ChatMessage = summary_response["message"]
        summary = summary_message.content
        return {"summary": summary}
