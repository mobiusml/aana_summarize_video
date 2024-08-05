from collections.abc import AsyncGenerator
from typing import Annotated, TypedDict

from aana.api.api_generation import Endpoint
from aana.core.models.chat import ChatDialog, ChatMessage
from aana.core.models.video import VideoInput
from aana.deployments.aana_deployment_handle import AanaDeploymentHandle
from aana.integrations.external.yt_dlp import download_video
from aana.processors.remote import run_remote
from aana.processors.video import extract_audio
from pydantic import Field


class SummarizeVideoStreamEndpointOutput(TypedDict):
    """Summarize video endpoint output."""

    text: Annotated[str, Field(description="The text chunk.")]


class SummarizeVideoStreamEndpoint(Endpoint):
    """Summarize video endpoint with streaming output."""

    async def initialize(self):
        """Initialize the endpoint."""
        await super().initialize()
        self.asr_handle = await AanaDeploymentHandle.create("asr_deployment")
        self.llm_handle = await AanaDeploymentHandle.create("llm_deployment")

    async def run(
        self, video: VideoInput
    ) -> AsyncGenerator[SummarizeVideoStreamEndpointOutput, None]:
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
        async for chunk in self.llm_handle.chat_stream(dialog=dialog):
            chunk_text = chunk["text"]
            yield {"text": chunk_text}
