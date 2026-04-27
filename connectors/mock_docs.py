import json
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "onboarding_docs.json"


def get_onboarding_docs() -> list[dict[str, str]]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def search_onboarding_docs(query: str) -> list[dict[str, str]]:
    terms = {term.strip(".,?!").lower() for term in query.split() if len(term) > 2}
    docs = get_onboarding_docs()

    scored = []
    for doc in docs:
        haystack = f"{doc['title']} {doc['content']} {' '.join(doc['tags'])}".lower()
        score = sum(term in haystack for term in terms)
        if score:
            scored.append((score, doc))

    return [doc for _, doc in sorted(scored, key=lambda item: item[0], reverse=True)]
