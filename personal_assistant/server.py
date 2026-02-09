from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from personal_assistant.config import settings
from personal_assistant.services.recorder import FFmpegRecorder, RecorderError
from personal_assistant.services.repository import SessionRepository
from personal_assistant.services.transcriber import OpenAITranscriber, TranscriberError

settings.ensure_dirs()
repo = SessionRepository(settings.db_path)
recorder = FFmpegRecorder()
transcriber = OpenAITranscriber(settings.openai_api_key, settings.openai_model)

app = FastAPI(title="Personal Assistant")
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")


class SessionCreate(BaseModel):
    title: str


@app.get("/")
def index() -> FileResponse:
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.get("/api/sessions")
def list_sessions() -> list[dict]:
    return [
        {
            "id": s.id,
            "title": s.title,
            "status": s.status,
            "audio_path": s.audio_path,
            "transcript": s.transcript,
            "created_at": s.created_at.isoformat(),
            "stopped_at": s.stopped_at.isoformat() if s.stopped_at else None,
        }
        for s in repo.list_sessions()
    ]


@app.post("/api/sessions/start")
def start_session(payload: SessionCreate) -> dict:
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe_title = payload.title.strip().replace(" ", "_")[:40] or "session"
    audio_path = settings.recordings_dir / f"{timestamp}_{safe_title}.wav"
    session_id = repo.create_session(payload.title, str(audio_path))
    try:
        recorder.start(session_id, audio_path)
    except RecorderError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return {"session_id": session_id, "audio_path": str(audio_path)}


@app.post("/api/sessions/{session_id}/stop")
def stop_session(session_id: int) -> dict:
    if not repo.get_session(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    try:
        recorder.stop(session_id)
        repo.stop_session(session_id)
    except RecorderError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"status": "recorded"}


@app.post("/api/sessions/{session_id}/transcribe")
def transcribe_session(session_id: int) -> dict:
    session = repo.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    try:
        text = transcriber.transcribe(Path(session.audio_path))
        repo.save_transcript(session_id, text)
    except TranscriberError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"transcript": text}
