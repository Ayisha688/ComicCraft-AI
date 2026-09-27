# ComicCraft - AI Comic Story Creator

ComicCraft is a FastAPI web application that turns a user's story idea into a 5-panel comic.

## Architecture

- Frontend: HTML + CSS + Jinja2
- Backend: FastAPI
- Story generation: Gemini API
- Image generation: Hugging Face Diffusers + Stable Diffusion
- PDF export: FPDF
- Local server: Uvicorn

## Features

- Story prompt
- Character name
- Setting
- Tone
- Art style
- 5-panel outline
- Narration and dialogue
- AI-generated panel images
- Comic preview
- PDF download
- JSON API
- Image test endpoint

## Local setup

```bash
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Put your Gemini API key in `.env`.

Run:

```bash
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

API docs: http://127.0.0.1:8000/docs

## Important

Stable Diffusion is computationally heavy. A CUDA-compatible GPU is strongly recommended. CPU generation may be very slow.

Do not commit `.env` or API keys to GitHub.
