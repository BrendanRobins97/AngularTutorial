# Personal Assistant (AI)

A clean, extensible local web app that can:
- record long-running desktop audio sessions
- save recordings persistently
- transcribe recordings using OpenAI

## Architecture (future-friendly)
- `personal_assistant/server.py` — FastAPI API + static app host
- `personal_assistant/services/repository.py` — persistence layer (SQLite)
- `personal_assistant/services/recorder.py` — recording adapter (FFmpeg)
- `personal_assistant/services/transcriber.py` — OpenAI transcription adapter
- `personal_assistant/static/` — clean UI (HTML/CSS/JS)

This separation makes it straightforward to add future features like summaries, memory search, reminders, and plugins.

## Requirements
- Python 3.10+
- FFmpeg installed and available on your PATH
- OpenAI API key (`OPENAI_API_KEY`)

> **Desktop + mic capture note:** true dual-source capture (system output + microphone) is OS/device specific. This app provides FFmpeg adapters and persistent architecture; for best results configure your OS audio routing (e.g., loopback/virtual device) so both streams are available to FFmpeg.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
export OPENAI_API_KEY=your_key_here
personal-assistant
```
Then open: `http://127.0.0.1:8000`

## Tests
```bash
python -m pytest
```
