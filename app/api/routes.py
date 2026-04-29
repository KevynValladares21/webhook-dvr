from time import perf_counter

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_api_key
from app.core.config import settings
from app.db.models import Event

router = APIRouter()


@router.get("/healthz")
def healthz():
    return {"ok": True}


def build_replay_headers(headers: dict) -> dict:
    excluded_headers = {
        "host",
        "content-length",
        "connection",
        "accept-encoding",
    }

    return {
        key: value
        for key, value in headers.items()
        if key.lower() not in excluded_headers
    }


@router.post("/ingest/{source}")
async def ingest(
    source: str,
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(require_api_key),
):
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


@router.get("/events")
def list_events(
    db: Session = Depends(get_db),
    _: None = Depends(require_api_key),
):
    events = db.query(Event).order_by(Event.received_at.desc()).limit(10).all()

    return [
        {
            "id": event.id,
            "source": event.source,
            "received_at": event.received_at,
        }
        for event in events
    ]


@router.get("/events/{event_id}")
def get_event(
    event_id: str,
    db: Session = Depends(get_db),
    _: None = Depends(require_api_key),
):
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


@router.post("/events/{event_id}/replay")
async def replay_event(
    event_id: str,
    db: Session = Depends(get_db),
    _: None = Depends(require_api_key),
):
    event = db.get(Event, event_id)

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    start = perf_counter()

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.replay_target_url,
                content=event.body,
                headers=build_replay_headers(event.headers),
                timeout=10.0,
            )

        duration = perf_counter() - start

        return {
            "target_url": settings.replay_target_url,
            "status_code": response.status_code,
            "duration_ms": round(duration * 1000, 2),
            "response_body": response.text[:200],
        }

    except httpx.HTTPError as exc:
        duration = perf_counter() - start

        return {
            "target_url": settings.replay_target_url,
            "duration_ms": round(duration * 1000, 2),
            "error": str(exc),
        }
