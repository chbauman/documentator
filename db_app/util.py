from pathlib import Path

PROJECT_DIR = Path(__file__).parent
FILES_DIR = PROJECT_DIR / "images"


def get_file_path(user_id: int, file_name: str):
    user_file_dir = FILES_DIR / f"user_{user_id}"
    user_file_dir.mkdir(exist_ok=True, parents=True)
    file_path = user_file_dir / file_name.replace(" ", "-")
    return file_path
