from aana_summarize_video.endpoints.summarize_video import SummarizeVideoEndpoint
from aana_summarize_video.endpoints.summarize_video_stream import (
    SummarizeVideoStreamEndpoint,
)
from aana_summarize_video.endpoints.transcribe_video import TranscribeVideoEndpoint

endpoints: list[dict] = [
    {
        "name": "transcribe_video",
        "path": "/video/transcribe",
        "summary": "Transcribe a video",
        "endpoint_cls": TranscribeVideoEndpoint,
    },
    {
        "name": "summarize_video",
        "path": "/video/summarize",
        "summary": "Summarize a video",
        "endpoint_cls": SummarizeVideoEndpoint,
    },
    {
        "name": "summarize_video_stream",
        "path": "/video/summarize_stream",
        "summary": "Summarize a video with streaming output",
        "endpoint_cls": SummarizeVideoStreamEndpoint,
    },
]
