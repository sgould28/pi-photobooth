
from pathlib import Path
from datetime import datetime
import subprocess

BASE_DIR = Path(__file__).resolve().parent
PHOTO_DIR = BASE_DIR / "photos"
LOG_FILE = BASE_DIR / "camera_error.log"


def take_photo():
    PHOTO_DIR.mkdir(parents=True, exist_ok=True)

    filename = datetime.now().strftime(
        "photo_%Y%m%d_%H%M%S_%f.jpg"
    )

    photo_path = PHOTO_DIR / filename

    command = [
        "rpicam-still",
        "--nopreview",
        "--timeout", "1000",
        "--output", str(photo_path)
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30
        )

    except subprocess.TimeoutExpired as error:
        raise RuntimeError(
            "Camera timed out after 30 seconds."
        ) from error

    except FileNotFoundError as error:
        raise RuntimeError(
            "rpicam-still was not found. Check camera software."
        ) from error

    if result.returncode != 0:
        details = (
            result.stderr.strip()
            or result.stdout.strip()
            or "No camera error details were returned."
        )

        LOG_FILE.write_text(details, encoding="utf-8")

        raise RuntimeError(
            f"Camera command failed:\n{details[-500:]}"
        )

    if not photo_path.is_file():
        raise RuntimeError(
            "Camera command finished, but no picture was saved."
        )

    return photo_path
