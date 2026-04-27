import json
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "task_updates.json"


def get_task_updates() -> list[dict[str, str]]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))
