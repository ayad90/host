import os
import asyncio
from pyrogram import Client, filters
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import uvicorn
from contextlib import asynccontextmanager

# --- TERA SAARA DATA YAHAN DIRECT DAAL DIYA HAI ---
API_ID = 34774921
API_HASH = "b3b608be7a648c062923e96fd7a312c2"
BOT_TOKEN = "8931102368:AAGoac729b8MpmNgFRh3zsr201O3DPdzuiE"
BASE_URL = "https://host-1-tk2x.onrender.com" # Agar Render link badle toh bas ise change kar lena

# Lifespan manager to handle startup safely
@asynccontextmanager
async def lifespan(app: FastAPI):
    await tg_app.start()
    print("--- VIP SERVER STARTED SUCCESSFULLY ---")
    yield
    await tg_app.stop()

# Initialize Telegram Client
tg_app = Client(
    "vip_streamer", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    bot_token=BOT_TOKEN,
    in_memory=True
)

app = FastAPI(lifespan=lifespan)

# Bot Part: Video forward karo aur link lo
@tg_app.on_message(filters.video | filters.document)
async def get_link(client, message):
    file_id = message.video.file_id if message.video else message.document.file_id
    streaming_link = f"{BASE_URL}/stream/{file_id}"
    await message.reply_text(f"🚀 **VIP Link Ready:**\n\n`{streaming_link}`")

# Stream Part: Play video direct
@app.get("/stream/{file_id}")
async def stream_video(file_id: str):
    async def file_generator():
        async for chunk in tg_app.get_file_chunks(file_id):
            yield chunk
    return StreamingResponse(file_generator(), media_type="video/mp4")

@app.get("/")
async def health():
    return {"status": "Online", "msg": "Direct Key Mode Active"}

if __name__ == "__main__":
    # Render uses port 10000
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
