from connectors.mock_contacts import get_contacts
from connectors.mock_docs import search_onboarding_docs


def run_onboarding_agent(query: str):
    matches = search_onboarding_docs(query)
    contacts = get_contacts()

    if matches:
        answer_parts = [
            "Here is what I found for your onboarding question:",
            "",
        ]
        for item in matches[:3]:
            answer_parts.append(f"- {item['title']}: {item['content']}")
    else:
        answer_parts = [
            "I could not find a direct policy match, but these first-week contacts can help:",
        ]

    answer_parts.extend(
        [
            "",
            "Useful contacts:",
            f"- HR: {contacts['hr']['name']} ({contacts['hr']['email']})",
            f"- IT Helpdesk: {contacts['it']['name']} ({contacts['it']['email']})",
            f"- Facilities: {contacts['facilities']['name']} ({contacts['facilities']['email']})",
        ]
    )

    return {
        "workflow": "onboarding",
        "answer": "\n".join(answer_parts),
        "sources": [item["source"] for item in matches[:3]] or ["data/contacts.json"],
        "metadata": {"matches": len(matches)},
    }
