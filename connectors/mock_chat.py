import json
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "chat_logs.json"


def get_chat_logs() -> list[dict[str, str]]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))
