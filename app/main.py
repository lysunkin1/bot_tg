from fastapi import FastAPI, Request

from app.bot_client import handle_client_update
from app.bot_admin import handle_admin_update

app = FastAPI()


@app.get("/")
async def health():
    return {"status": "ok"}


@app.post("/webhook/client")
async def client_webhook(request: Request):
    update = await request.json()
    await handle_client_update(update)
    return {"ok": True}


@app.post("/webhook/admin")
async def admin_webhook(request: Request):
    update = await request.json()
    await handle_admin_update(update)
    return {"ok": True}
