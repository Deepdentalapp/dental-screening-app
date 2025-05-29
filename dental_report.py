# dental_report.py

from PIL import Image, ImageDraw, ImageFont

def detect_all_issues(image_index):
    # Dummy issue detection for testing
    return [
        {"type": "caries", "tooth": 26, "bbox": (80, 60, 150, 120)},
        {"type": "broken", "tooth": 12, "bbox": (160, 100, 220, 160)},
        {"type": "lesion", "tooth": None, "bbox": (250, 140, 290, 180)}
    ] if image_index % 2 == 0 else [
        {"type": "missing", "tooth": 46, "bbox": (100, 60, 140, 100)},
        {"type": "caries", "tooth": 36, "bbox": (180, 110, 240, 160)},
        {"type": "malocclusion", "tooth": None, "bbox": None}
    ]

def annotate(image, issues):
    img = image.copy()
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    for issue in issues:
        bbox = issue["bbox"]
        t_type = issue["type"]
        tooth = issue["tooth"]
        color = {"caries": "red", "missing": "blue", "broken": "orange", "lesion": "green"}.get(t_type, "black")
        if bbox:
            x1, y1, x2, y2 = bbox
            label = f"{t_type} T{tooth}" if tooth else t_type
            if t_type == "lesion":
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                r = (x2 - x1) // 2
                draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color, width=3)
            else:
                draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
            draw.text((x1, y1 - 10), label, fill=color, font=font)
    return img

def create_pdf(images, findings, output_path="output.pdf"):
    # Placeholder function for PDF creation
    pass
    
