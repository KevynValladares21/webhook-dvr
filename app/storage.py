from typing import Dict, Any
from uuid import uuid4
from datetime import datetime

# super simple in-memory store
EVENTS: Dict[str, Dict[str, Any]] = {}


def save_event(data: Dict[str, Any]) -> str:
    event_id = str(uuid4())
    EVENTS[event_id] = {
        "id": event_id,
        "received_at": datetime.utcnow().isoformat(),
        **data,
    }
    return event_id


def get_event(event_id: str) -> Dict[str, Any] | None:
    return EVENTS.get(event_id)

