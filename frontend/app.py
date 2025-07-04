import streamlit as st
import os
import tempfile
from src.run_stock_estimator import get_report
from src.agent_utils import load_model
from src.utils import create_pdf_from_dict

FINANCIALS_API_KEY = os.getenv('FINANCIALS_API_KEY')
MODEL = load_model()


def generate_pdf(company_reports):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    create_pdf_from_dict(company_reports, temp_file.name)
    return temp_file.name

# Streamlit app
st.title("Company Report Generator")

company_input = st.text_area("Enter company names (comma-separated):")

if st.button("Generate PDF Report"):
    companies = [name.strip() for name in company_input.split(",") if name.strip()]
    if not companies:
        st.warning("Please enter at least one company.")
    else:
        reports = {c:get_report(c, MODEL, FINANCIALS_API_KEY) for c in companies}
        pdf_path = generate_pdf(reports)

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Download Report PDF",
                data=f,
                file_name="company_report.pdf",
                mime="application/pdf"
            )
