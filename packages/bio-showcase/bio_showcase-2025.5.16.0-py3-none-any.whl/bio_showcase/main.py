import uvicorn
from sodatools import CD
from pathlib import Path


def main():
    cr = Path(__file__).resolve().parent
    with CD(cr):
        try:
            uvicorn.run("bio_showcase.asgi:application", port=8000, log_level="info")
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
