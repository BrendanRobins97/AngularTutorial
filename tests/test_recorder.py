from pathlib import Path

from personal_assistant.services.recorder import FFmpegRecorder


def test_build_command_contains_ffmpeg(monkeypatch) -> None:
    recorder = FFmpegRecorder()
    monkeypatch.setattr("platform.system", lambda: "Linux")
    cmd = recorder.build_command(Path("out.wav"))
    assert cmd[0] == "ffmpeg"
    assert "out.wav" in cmd
