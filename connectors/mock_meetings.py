import json
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "meeting_notes.json"


def get_meeting_notes() -> list[dict]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))
