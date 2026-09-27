from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import router


app = FastAPI(
    title="ComicCraft - AI Comic Story Creator",
    description="Generate a 5-panel AI comic using Gemini and Stable Diffusion.",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

app.include_router(router)