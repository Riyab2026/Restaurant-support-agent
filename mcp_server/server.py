import uuid
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mock_api_server", host="127.0.0.1", port=8001)

DOCS_PATH = Path(__file__).resolve().parent.parent / "docs" / "docs.md"

_issues: list[dict] = []
_feedback: list[dict] = []

_STORE_HOURS = {
    "new york": "6:00 AM - 11:00 PM daily, with select drive-thru locations open 24 hours.",
    "chicago": "6:00 AM - 12:00 AM daily, with select drive-thru locations open 24 hours.",
    "london": "7:00 AM - 11:00 PM daily, with select drive-thru locations open 24 hours.",
    "los angeles": "5:30 AM - 1:00 AM daily, with select drive-thru locations open 24 hours.",
}


@mcp.tool()
def log_issue(description: str, order_reference: str = "") -> dict:
    """Log a customer's order or restaurant visit issue and get a case ID."""
    case_id = uuid.uuid4().hex[:8].upper()
    _issues.append(
        {
            "case_id": case_id,
            "description": description,
            "order_reference": order_reference,
        }
    )
    return {"case_id": case_id, "status": "logged"}


@mcp.tool()
def submit_feedback(sentiment: str, comment: str = "") -> dict:
    """Record customer feedback about their order or restaurant visit."""
    _feedback.append({"sentiment": sentiment, "comment": comment})
    return {"status": "recorded"}


@mcp.tool()
def get_store_hours(location: str) -> str:
    """Look up restaurant opening hours for a specific city or location."""
    hours = _STORE_HOURS.get(location.strip().lower())
    if hours:
        return f"Hours for {location}: {hours}"
    return (
        f"We don't have specific hours on file for {location}. Most restaurants are "
        "open 6:00 AM - 11:00 PM, though this varies by location. Check the McDonald's "
        "app or the restaurant locator on our website for the exact hours of your "
        "nearest restaurant."
    )


@mcp.tool()
def search_faqs(query: str) -> str:
    """Look up an answer to a customer's question in the restaurant's FAQ knowledge base."""
    return DOCS_PATH.read_text(encoding="utf-8")


@mcp.tool()
def escalate_to_human(summary: str) -> dict:
    """Transfer the customer to a human Customer Support Specialist with a summary of the conversation."""
    ticket_id = uuid.uuid4().hex[:8].upper()
    return {"status": "transferred", "ticket_id": ticket_id}


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
