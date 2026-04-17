from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models import Event

router = APIRouter()


@router.get("/healthz")
def healthz():
    return {"ok": True}


@router.post("/ingest/{source}")
async def ingest(source: str, request: Request, db: Session = Depends(get_db)):
    body = await request.body()
    headers = dict(request.headers)
    query_params = dict(request.query_params)

    event = Event(
        source=source,
        body=body.decode(errors="replace"),
        headers=headers,
        query_params=query_params,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return {"event_id": event.id}


@router.get("/events/{event_id}")
def get_event(event_id: str, db: Session = Depends(get_db)):
    event = db.get(Event, event_id)

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return {
        "id": event.id,
        "source": event.source,
        "body": event.body,
        "headers": event.headers,
        "query_params": event.query_params,
        "received_at": event.received_at,
    }


@router.get("/events")
def list_events(db: Session = Depends(get_db)):
    events = (
        db.query(Event)
        .order_by(Event.received_at.desc())
        .limit(10)
        .all()
    )

    return [
        {
            "id": e.id,
            "source": e.source,
            "received_at": e.received_at,
        }
        for e in events
    ]
