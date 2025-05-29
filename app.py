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

