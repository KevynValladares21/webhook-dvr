from fastapi import APIRouter, Request

from app.db.session import SessionLocal
from app.db.models import Event
from app.storage import save_event, get_event

router = APIRouter()


@router.get("/healthz")
def healthz():
    return {"ok": True}


@router.post("/ingest/{source}")
async def ingest(source: str, request: Request):
    body = await request.body()
    headers = dict(request.headers)
    query_params = dict(request.query_params)

    db = SessionLocal()

    event = Event(
        source=source,
        body=body.decode(errors="replace"),
        headers=headers,
        query_params=query_params,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    db.close()

    return {"event_id": event.id}

@router.get("/events/{event_id}")
def get_event_api(event_id: str):
    event = get_event(event_id)
    if not event:
        return {"error": "not found"}
    return event

