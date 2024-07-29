from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.bot import ChatBot
from app.database import Collection

VERSION = "0.0.1"
API = FastAPI(
    title="HistoryBot",
    version=VERSION,
    docs_url="/",
)
API.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
history = Collection("Chat", "History")
bot = ChatBot()


@API.get("/version")
def version():
    return VERSION


@API.get("/chat", tags=["ChatBot"])
async def chat(prompt: str):
    query = {"role": "user", "content": prompt}
    history.write(query)
    recent = history.recent(10)
    result = bot(recent)
    history.write({"role": "assistant", "content": result})
    return result
