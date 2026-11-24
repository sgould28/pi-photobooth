
from pathlib import Path
from datetime import datetime
import subprocess

PHOTO_DIR = Path(__file__).parent / "photos"


def take_photo():
    PHOTO_DIR.mkdir(exist_ok=True)

    filename = datetime.now().strftime("photo_%Y%m%d_%H%M%S.jpg")
    photo_path = PHOTO_DIR / filename

    subprocess.run(
        [
            "rpicam-still",
            "-n",
            "-t", "1000",
            "-o", str(photo_path)
        ],
        check=True,
        timeout=30
    )

    return photo_path
