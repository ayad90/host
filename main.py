import os
import asyncio
from pyrogram import Client, filters
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn

# --- TERA DATA ---
API_ID = 34774921
API_HASH = "b3b608be7a648c062923e96fd7a312c2"
BOT_TOKEN = "8931102368:AAGoac729b8MpmNgFRh3zsr201O3DPdzuiE"
BASE_URL = "https://host-1-tk2x.onrender.com" # Agar render link badle toh yahan update kar dena

app = FastAPI()

# Client initialize
tg_app = Client(
    "vip_vids_streamer",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True
)

@app.on_event("startup")
async def start_tg():
    if not tg_app.is_connected:
        await tg_app.start()
    print("--- SERVER IS LIVE ---")

@app.get("/")
async def index():
    return {"status": "running", "server": "VIP Cloud"}

# Bot: Video forward karne par link dega
@tg_app.on_message(filters.video | filters.document)
async def handle_video(client, message):
    file_id = message.video.file_id if message.video else message.document.file_id
    link = f"{BASE_URL}/stream/{file_id}"
    await message.reply_text(f"🚀 **VIP Link:**\n\n`{link}`")

# Stream: Video play karega
@app.get("/stream/{file_id}")
async def stream_video(file_id: str):
    async def file_generator():
        async for chunk in tg_app.get_file_chunks(file_id):
            yield chunk
    return StreamingResponse(file_generator(), media_type="video/mp4")

if __name__ == "__main__":
    # Render default port is 10000
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
