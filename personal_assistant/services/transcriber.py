from pathlib import Path


class TranscriberError(RuntimeError):
    pass


class OpenAITranscriber:
    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model

    def transcribe(self, audio_path: Path) -> str:
        if not self.api_key:
            raise TranscriberError("OPENAI_API_KEY is not configured")
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise TranscriberError("openai package is not installed") from exc

        client = OpenAI(api_key=self.api_key)
        with audio_path.open("rb") as audio_file:
            transcript = client.audio.transcriptions.create(model=self.model, file=audio_file)
        if not getattr(transcript, "text", ""):
            raise TranscriberError("Transcription failed or returned empty text")
        return transcript.text
