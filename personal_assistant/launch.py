import uvicorn

from personal_assistant.config import settings


def main() -> None:
    uvicorn.run("personal_assistant.server:app", host=settings.host, port=settings.port, reload=False)


if __name__ == "__main__":
    main()
