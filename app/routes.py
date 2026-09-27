from pathlib import Path

from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf


BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


class PromptRequest(BaseModel):
    story_prompt: str
    character_name: str
    setting: str
    tone: str
    art_style: str


def create_comic(data: PromptRequest):
    outline = generate_outline(
        data.story_prompt,
        data.character_name,
        data.setting,
        data.tone,
        data.art_style,
    )

    story = generate_story(
        outline,
        data.story_prompt,
        data.character_name,
        data.setting,
        data.tone,
        data.art_style,
    )

    # Reuse the 5 images already generated.
    existing_images = [
        "/static/panels/Classic_comic_book_art_style_vibrant_inks_and_halftone_dots_41449.png",
        "/static/panels/Comic_book_medium_shot_with_high_contrast_lighting_Arun_knee_97323.png",
        "/static/panels/Comic_book_panel_expressive_character_acting_sharp_linework_65739.png",
        "/static/panels/Comic_book_panel_expressive_character_acting_sharp_linework_65739.png",
        "/static/panels/Whimsical_comic_book_style_wide_panel_warm_magical_lighting_13774.png",
    ]

    panels = []

    for i, panel in enumerate(outline):
        image_path = (
            existing_images[i]
            if i < len(existing_images)
            else ""
        )

        panels.append({
            **panel,
            "image_path": image_path
        })

    layout = build_comic_layout(
        panels,
        story
    )

    pdf_path = save_pdf(layout)

    return layout, pdf_path


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        data = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )

        layout, pdf_path = create_comic(data)

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "request": request,
                "layout": layout,
                "pdf_path": pdf_path,
            },
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


@router.post("/generate-comic/json")
async def generate_json(data: PromptRequest):
    try:
        layout, pdf_path = create_comic(data)

        return JSONResponse(
            content={
                "layout": layout,
                "pdf_path": pdf_path
            }
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


@router.get("/download/{filename}")
async def download_pdf(filename: str):
    safe_name = Path(filename).name
    path = Path("static/exports") / safe_name

    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail="PDF not found"
        )

    return FileResponse(
        path=str(path),
        media_type="application/pdf",
        filename=safe_name,
    )


@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={
            "request": request
        },
    )


@router.get("/test-image", response_class=HTMLResponse)
async def test_image(
    request: Request,
    prompt: str = "a brave fox in an enchanted forest"
):
    try:
        from app.image_generator import generate_image

        image_path = generate_image(
            prompt,
            "comic book"
        )

        return templates.TemplateResponse(
            request=request,
            name="test_image.html",
            context={
                "request": request,
                "image_path": image_path,
                "prompt": prompt,
            },
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


@router.get("/test-pdf")
async def test_pdf():
    try:
        image_files = [
            "static/panels/Classic_comic_book_art_style_vibrant_inks_and_halftone_dots_41449.png",
            "static/panels/Comic_book_medium_shot_with_high_contrast_lighting_Arun_knee_97323.png",
            "static/panels/Comic_book_panel_expressive_character_acting_sharp_linework_65739.png",
            "static/panels/Comic_book_panel_expressive_character_acting_sharp_linework_65739.png",
            "static/panels/Whimsical_comic_book_style_wide_panel_warm_magical_lighting_13774.png",
        ]

        panels = []

        for i, image_file in enumerate(image_files):
            panels.append({
                "panel": i + 1,
                "title": f"Comic Panel {i + 1}",
                "scene_description": "Comic scene",
                "image_prompt": "",
                "image_path": "/" + image_file,
                "narration": "Comic narration",
                "dialogue": "",
                "caption": "Comic caption",
            })

        pdf_path = save_pdf(panels)

        return {
            "message": "PDF created successfully!",
            "pdf_path": pdf_path,
            "panels": len(panels),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )