from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class RecordingSession:
    id: int
    title: str
    status: str
    audio_path: str
    transcript: Optional[str]
    created_at: datetime
    stopped_at: Optional[datetime]
