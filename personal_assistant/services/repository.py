import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from personal_assistant.models import RecordingSession


class SessionRepository:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    status TEXT NOT NULL,
                    audio_path TEXT NOT NULL,
                    transcript TEXT,
                    created_at TEXT NOT NULL,
                    stopped_at TEXT
                )
                """
            )

    def create_session(self, title: str, audio_path: str) -> int:
        now = datetime.utcnow().isoformat()
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO sessions (title, status, audio_path, created_at) VALUES (?, ?, ?, ?)",
                (title, "recording", audio_path, now),
            )
            return int(cur.lastrowid)

    def stop_session(self, session_id: int) -> None:
        now = datetime.utcnow().isoformat()
        with self._connect() as conn:
            conn.execute(
                "UPDATE sessions SET status = ?, stopped_at = ? WHERE id = ?",
                ("recorded", now, session_id),
            )

    def save_transcript(self, session_id: int, transcript: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE sessions SET transcript = ?, status = ? WHERE id = ?",
                (transcript, "transcribed", session_id),
            )

    def get_session(self, session_id: int) -> Optional[RecordingSession]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
        if not row:
            return None
        return self._to_model(row)

    def list_sessions(self) -> list[RecordingSession]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM sessions ORDER BY id DESC").fetchall()
        return [self._to_model(r) for r in rows]

    @staticmethod
    def _to_model(row: sqlite3.Row) -> RecordingSession:
        return RecordingSession(
            id=row["id"],
            title=row["title"],
            status=row["status"],
            audio_path=row["audio_path"],
            transcript=row["transcript"],
            created_at=datetime.fromisoformat(row["created_at"]),
            stopped_at=datetime.fromisoformat(row["stopped_at"]) if row["stopped_at"] else None,
        )
