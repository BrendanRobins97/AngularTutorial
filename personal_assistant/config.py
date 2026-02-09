from pathlib import Path
import os


class Settings:
    def __init__(self) -> None:
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini-transcribe")
        self.host = os.getenv("PA_HOST", "127.0.0.1")
        self.port = int(os.getenv("PA_PORT", "8000"))
        self.data_dir = Path(os.getenv("PA_DATA_DIR", str(Path.home() / ".personal_assistant")))
        self.recordings_dir = self.data_dir / "recordings"
        self.db_path = self.data_dir / "assistant.db"

    def ensure_dirs(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.recordings_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
