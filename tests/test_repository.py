from pathlib import Path

from personal_assistant.services.repository import SessionRepository


def test_session_lifecycle(tmp_path: Path) -> None:
    repo = SessionRepository(tmp_path / "assistant.db")
    sid = repo.create_session("Daily sync", "/tmp/audio.wav")
    session = repo.get_session(sid)
    assert session is not None
    assert session.status == "recording"

    repo.stop_session(sid)
    session = repo.get_session(sid)
    assert session is not None
    assert session.status == "recorded"

    repo.save_transcript(sid, "hello world")
    session = repo.get_session(sid)
    assert session is not None
    assert session.status == "transcribed"
    assert session.transcript == "hello world"
