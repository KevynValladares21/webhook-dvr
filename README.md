# Webhook DVR

Webhook DVR is a lightweight webhook capture and replay service built with FastAPI.

It records incoming webhook HTTP requests (body, headers, query parameters) and allows developers to inspect and replay them later. This helps debug third-party integrations such as Stripe, GitHub, Shopify, and similar webhook-based systems.

---

## Motivation

Webhook integrations are often difficult to debug because:

- Events fire asynchronously and unpredictably
- Payloads are lost if a server is down or fails
- Reproducing failures can be difficult
- Replaying historical events is rarely supported

Webhook DVR acts as a **"DVR for webhooks"**, recording events for inspection and replay.

---

## Current Features

- Capture webhook requests via ingestion endpoint
- Store:
  - Raw request body
  - Headers
  - Query parameters
  - Source label
  - Timestamp
- Retrieve events by ID
- In-memory event storage (MVP implementation)

---

## Tech Stack

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic Settings
- Ruff (linting)

---

## Project Structure

```
app/
  api/
    routes.py        # API endpoints
  core/
    config.py        # App configuration
  storage.py         # In-memory event storage
  main.py            # App entrypoint
```

---

## Getting Started

### Clone the repository

```bash
git clone <repo-url>
cd webhook-dvr
```

### Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -e ".[dev]"
```

### Run the server

```bash
uvicorn app.main:app --reload
```

API documentation will be available at:

```
http://localhost:8000/docs
```

---

## Usage

### Ingest a webhook

```bash
curl -X POST "http://localhost:8000/ingest/test" \
  -H "X-Custom-Header: hello" \
  -d '{"hello": "world"}'
```

Response:

```json
{
  "event_id": "..."
}
```

---

### Retrieve an event

```bash
curl http://localhost:8000/events/<event_id>
```

---

## Design Notes

Webhook DVR intentionally stores **raw request data** to preserve fidelity for debugging and replay.

This project emphasizes:

- Backend architecture clarity
- Event-driven system thinking
- Reliability and debuggability of integrations

---

## Roadmap

- PostgreSQL persistence
- Webhook replay endpoint
- API key authentication
- Pagination and filtering
- Docker deployment
- Automated tests

---

## License

MIT

