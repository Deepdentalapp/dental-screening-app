import streamlit as st
from PIL import Image
from dental_report import detect_all_issues, annotate, create_pdf

st.set_page_config(page_title="Dental AI Screening", layout="wide")

st.title("🦷 Dental AI Screening Report Generator")

uploaded_files = st.file_uploader(
    "Upload 6 standard dental images (frontal, lateral, occlusal, etc.)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

logo_file = st.file_uploader("Upload Clinic Logo", type=["jpg", "jpeg", "png"])
patient_name = st.text_input("Patient Name")
patient_age = st.text_input("Patient Age")
link = st.text_input("Clinic Website or WhatsApp Link", value="https://affodent.in")

if st.button("Generate Report"):
    if len(uploaded_files) != 6:
        st.error("Please upload exactly 6 dental images.")
    elif not logo_file:
        st.error("Please upload your clinic logo.")
    elif not patient_name or not patient_age:
        st.error("Please enter patient name and age.")
    else:
        images = [Image.open(file).convert("RGB") for file in uploaded_files]
        logo_image = Image.open(logo_file).convert("RGB")

        annotated_images = []
        all_findings = []
        filenames = []

        for img, file in zip(images, uploaded_files):
            findings = detect_all_issues(img)
            annotated = annotate(img, findings)
            annotated_images.append(annotated)
            all_findings.append(findings)
            filenames.append(file.name)

        pdf_bytes = create_pdf(annotated_images, all_findings, filenames, logo_image, patient_name, patient_age, link)
        st.success("PDF report generated successfully!")

        st.download_button(
            label="📄 Download Report",
            data=pdf_bytes,
            file_name=f"{patient_name}_Dental_Report.pdf",
            mime="application/pdf"
        )

import streamlit as st
from PIL import Image
import requests
import os

st.set_page_config(page_title="Dental Screening Report", layout="centered")
st.title("🦷 Dental Screening Report Generator")

# === Input patient details ===
patient_name = st.text_input("Patient Name")
patient_phone = st.text_input("Patient WhatsApp Number (with country code, e.g. 91XXXXXXXXXX)")

# === Dummy PDF generation step ===
# Replace this with your actual PDF generation logic
def generate_pdf(file_path):
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(file_path)
    c.drawString(100, 750, f"Dental Report for {patient_name}")
    c.save()

if st.button("Generate Report"):
    # Step 1: Generate the report
    report_file = "output.pdf"
    generate_pdf(report_file)

    st.success("✅ Report generated!")

    # Step 2: Upload to file.io
    def upload_to_fileio(file_path):
        with open(file_path, 'rb') as f:
            response = requests.post("https://file.io", files={"file": f})
        if response.status_code == 200:
            return response.json().get("link")
        else:
            return None

    report_link = upload_to_fileio(report_file)

    if report_link:
        st.success("📤 Report uploaded successfully!")

        # Step 3: WhatsApp links
        if patient_phone:
            patient_url = f"https://wa.me/{patient_phone}?text=Hi%20{patient_name}%2C%20your%20dental%20report%20is%20ready.%20Download%20it%20here:%20{report_link}"
            st.markdown(f"[📲 Send to Patient WhatsApp]({patient_url})", unsafe_allow_html=True)

        clinic_url = f"https://wa.me/919864272102?text=New%20report%20generated%20for%20{patient_name}.%20Link:%20{report_link}"
        st.markdown(f"[📩 Send to Clinic WhatsApp]({clinic_url})", unsafe_allow_html=True)

    else:
        st.error("❌ Failed to upload report to File.io.")
