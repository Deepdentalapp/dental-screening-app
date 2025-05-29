
import streamlit as st
from PIL import Image
from dental_report import detect_all_issues, annotate, create_pdf
import io

st.set_page_config(page_title="AffoDent Dental AI", layout="centered")
st.title("🦷 AffoDent Dental Screening Tool")

patient_name = st.text_input("Patient Name")
patient_age = st.text_input("Patient Age")
link = "https://wa.me/919864272102"

logo_file = st.file_uploader("Upload clinic logo", type=["png", "jpg", "jpeg"])
if logo_file:
    logo_image = Image.open(logo_file)

uploaded_files = st.file_uploader("Upload 6 intraoral images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
if uploaded_files and logo_file and patient_name and patient_age:
    if len(uploaded_files) != 6:
        st.warning("Please upload exactly 6 images.")
    else:
        images = [Image.open(f).convert("RGB") for f in uploaded_files]
        filenames = [f.name for f in uploaded_files]

        if st.button("Run Diagnosis"):
            all_findings = []
            annotated_images = []

            for idx, img in enumerate(images):
                issues = detect_all_issues(idx)
                annotated = annotate(img, issues)
                annotated_images.append(annotated)
                all_findings.append(issues)

            st.success("Diagnosis complete! Generating PDF report...")
            pdf_bytes = create_pdf(annotated_images, all_findings, filenames, logo_image, patient_name, patient_age, link)

            st.download_button("📄 Download PDF Report", data=pdf_bytes, file_name="dental_report.pdf", mime="application/pdf")
else:
    st.info("Please upload all required fields: 6 images, logo, and patient details.")
