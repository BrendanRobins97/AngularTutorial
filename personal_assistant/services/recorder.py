import platform
import subprocess
from pathlib import Path


class RecorderError(RuntimeError):
    pass


class FFmpegRecorder:
    def __init__(self) -> None:
        self._processes: dict[int, subprocess.Popen] = {}

    def build_command(self, output_path: Path) -> list[str]:
        system = platform.system().lower()
        if "linux" in system:
            return [
                "ffmpeg", "-y",
                "-f", "pulse", "-i", "default",
                str(output_path),
            ]
        if "darwin" in system:
            return [
                "ffmpeg", "-y",
                "-f", "avfoundation", "-i", ":0",
                str(output_path),
            ]
        if "windows" in system:
            return [
                "ffmpeg", "-y",
                "-f", "dshow", "-i", "audio=Microphone",
                str(output_path),
            ]
        raise RecorderError(f"Unsupported platform: {system}")

    def start(self, session_id: int, output_path: Path) -> None:
        cmd = self.build_command(output_path)
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError as exc:
            raise RecorderError("FFmpeg is not installed or not on PATH") from exc
        self._processes[session_id] = process

    def stop(self, session_id: int) -> None:
        process = self._processes.get(session_id)
        if not process:
            raise RecorderError(f"No active recorder for session {session_id}")
        process.terminate()
        process.wait(timeout=5)
        del self._processes[session_id]
