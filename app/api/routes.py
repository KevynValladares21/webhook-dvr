from fastapi import APIRouter, Request

from app.storage import save_event, get_event

router = APIRouter()


@router.get("/healthz")
def healthz():
    return {"ok": True}


@router.post("/ingest/{source}")
async def ingest(source: str, request: Request):
    # 1. extract raw body
    body = await request.body()

    # 2. extract headers and query params
    headers = dict(request.headers)
    query_params = dict(request.query_params)

    # 3. build event payload
    event_data = {
        "source": source,
        "body": body.decode(errors="replace"),
        "headers": headers,
        "query_params": query_params,
    }

    # 4. save event
    event_id = save_event(event_data)

    # 5. return event ID
    return {"event_id": event_id}

@router.get("/events/{event_id}")
def get_event_api(event_id: str):
    event = get_event(event_id)
    if not event:
        return {"error": "not found"}
    return event

