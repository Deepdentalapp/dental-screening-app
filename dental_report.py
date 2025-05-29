import io
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import qrcode

def create_pdf(images, findings, filenames, logo_image, patient_name, patient_age, website_or_whatsapp_link):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Resize logo
    logo_resized = logo_image.resize((80, 80))

    # Generate QR Code
    qr = qrcode.QRCode(box_size=3, border=2)
    qr.add_data(website_or_whatsapp_link)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_buf = io.BytesIO()
    qr_img.save(qr_buf, format="PNG")
    qr_buf.seek(0)

    pt_id = f"PT{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    today = datetime.datetime.now().strftime("%d-%m-%Y")
    summary_issues = []

    # Loop through all 6 images
    for idx, img in enumerate(images):
        summary_issues += findings[idx]
        c.drawImage(ImageReader(logo_resized), 50, height - 90, width=80, height=80)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(140, height - 40, "AffoDent")
        c.setFont("Helvetica", 11)
        c.drawString(140, height - 60, "House no 4, College Hostel Road, Panbazar")
        c.drawString(140, height - 75, "Guwahati, Assam - 781001")
        c.drawString(140, height - 90, "Mobile: 9864272102")
        c.drawString(400, height - 40, f"Patient ID: {pt_id}-{idx+1:02d}")
        c.drawString(400, height - 60, f"Date: {today}")
        c.drawString(400, height - 75, f"Name: {patient_name}")
        c.drawString(400, height - 90, f"Age: {patient_age}")
        c.drawString(50, height - 120, f"Image: {filenames[idx]}")

        # Resize and place the dental image
        img_resized = img.resize((400, 250))
        c.drawImage(ImageReader(img_resized), 50, height - 430, width=400, height=250)

        # Write findings
        y = height - 450
        for issue in findings[idx]:
            line = f"• {issue['type'].capitalize()}"
            if issue["tooth"]:
                line += f" (Tooth {issue['tooth']})"
            c.drawString(50, y, line)
            y -= 18

        # QR + Signature
        c.drawImage(ImageReader(qr_buf), 50, 30, width=60, height=60)
        c.drawString(400, 60, "__________________________")
        c.drawString(400, 45, "Dr. Deep Sharma")
        c.drawString(400, 30, "Signature")

        c.showPage()

    # Summary Page
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 40, f"Diagnosis Summary - {patient_name} (Age: {patient_age})")
    c.setFont("Helvetica", 11)
    y = height - 80

    if summary_issues:
        grouped = {}
        for issue in summary_issues:
            key = issue['type']
            grouped.setdefault(key, []).append(issue.get("tooth"))
        for k, v in grouped.items():
            line = f"• {k.capitalize()}: {', '.join(f'T{t}' if t else 'N/A' for t in v)}"
            c.drawString(50, y, line)
            y -= 18
    else:
        c.drawString(50, y, "No significant findings.")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

# Placeholder for required functions (dummy for now)
def detect_all_issues(images):
    # Replace with actual detection logic
    return [[{"type": "caries", "tooth": "16"}] for _ in images]

def annotate(images, findings):
    # Replace with actual annotation logic
    return images
    
