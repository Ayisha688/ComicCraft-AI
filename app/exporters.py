from pathlib import Path
from datetime import datetime
from PIL import Image

EXPORT_DIR = Path("static/exports")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def save_pdf(layout):
    filename = f"comic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    output = EXPORT_DIR / filename

    images = []

    for panel in layout:
        image_path = panel.get("image_path", "")
        image_file = Path(image_path.lstrip("/"))

        if image_file.exists():
            img = Image.open(image_file).convert("RGB")
            images.append(img.copy())
            img.close()

    if not images:
        raise ValueError("No comic images found.")

    first_image = images[0]
    remaining_images = images[1:]

    first_image.save(
        output,
        "PDF",
        resolution=100.0,
        save_all=True,
        append_images=remaining_images
    )

    for img in images:
        img.close()

    return f"/download/{filename}"