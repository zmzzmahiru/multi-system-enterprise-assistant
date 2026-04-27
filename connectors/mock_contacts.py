import json
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "contacts.json"


def get_contacts() -> dict[str, dict[str, str]]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))
