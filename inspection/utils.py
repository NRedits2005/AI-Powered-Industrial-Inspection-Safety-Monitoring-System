"""Utility helpers for image encoding and annotation."""
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from typing import List, Dict, Any


def pil_image_to_base64(img: Image.Image) -> str:
    """Convert PIL image to data URL (PNG)."""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    b64 = base64.b64encode(buffered.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def draw_detections(img: Image.Image, detections: List[Dict[str, Any]], analysis: Dict = None) -> Image.Image:
    """Draw bounding boxes and labels on a copy of the image.

    Returns a new PIL.Image.
    """
    out = img.convert("RGBA").copy()
    draw = ImageDraw.Draw(out)

    # Try to load a default font; fallback to PIL default
    try:
        font = ImageFont.truetype("arial.ttf", size=14)
    except Exception:
        font = ImageFont.load_default()

    color_map = {"crack": (255, 165, 0, 200), "corrosion": (255, 215, 0, 200), "leak": (220, 20, 60, 200)}

    for d in detections:
        x, y, w, h = d["bbox"]
        label = d["label"]
        conf = d.get("confidence", 0)
        col = color_map.get(label, (0, 200, 255, 180))

        # box
        draw.rectangle([x, y, x + w, y + h], outline=col, width=3)
        text = f"{label} {conf:.2f}"
        text_size = draw.textsize(text, font=font)
        text_bg = (0, 0, 0, 160)
        draw.rectangle([x, y - text_size[1] - 4, x + text_size[0] + 6, y], fill=text_bg)
        draw.text((x + 3, y - text_size[1] - 2), text, fill=(255, 255, 255, 255), font=font)

    # Optionally annotate overall severity
    if analysis:
        sev = analysis.get("severity", "N/A")
        summary = analysis.get("summary", {})
        info = f"Severity: {sev} — {summary.get('total',0)} defect(s)"
        draw.rectangle([4, 4, 260, 28], fill=(0, 0, 0, 140))
        draw.text((8, 6), info, fill=(255, 255, 255, 255), font=font)

    return out.convert("RGB")

