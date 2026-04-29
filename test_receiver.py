from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/test")
async def test(request: Request):
    body = await request.body()
    print("RECEIVED BODY:", body)
    print("RECEIVED HEADERS:", dict(request.headers))
    return {"ok": True}
