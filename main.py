import os
import asyncio
from pyrogram import Client, filters
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

# --- CONFIGURATION (Render variables se aayega) ---
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Telegram Client Setup
tg_app = Client("my_streamer", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
app = FastAPI()

@app.on_event("startup")
async def startup():
    await tg_app.start()

# 1. BOT PART: Jab aap video forward karenge, ye link dega
@tg_app.on_message(filters.video | filters.document)
async def get_link(client, message):
    file_id = message.video.file_id if message.video else message.document.file_id
    # Ye base_url hum Render se milne ke baad settings mein update karenge
    base_url = os.environ.get("BASE_URL", "https://your-app.onrender.com")
    streaming_link = f"{base_url}/stream/{file_id}"
    await message.reply_text(f"🚀 **Aapka VIP Link taiyaar hai:**\n\n`{streaming_link}`")

# 2. STREAMING PART: Ye video play karega
@app.get("/stream/{file_id}")
async def stream_video(file_id: str):
    async def file_generator():
        async for chunk in tg_app.get_file_chunks(file_id):
            yield chunk
    return StreamingResponse(file_generator(), media_type="video/mp4")

@app.get("/")
async def health_check():
    return {"status": "Server is Online"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
