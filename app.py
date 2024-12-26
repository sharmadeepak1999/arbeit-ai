import os
import time
import streamlit as st
from services.job_detail_service import extract_job_details_from_text
from services.resume_detail_service import extract_resume_details_from_text
from services.comparison_service import compare_resume_and_job_description
from services.email_service import generate_job_application_email_dynamic
from services.referral_service import generate_job_referral_dynamic
from services.connection_note_service import generate_connection_note_dynamic
from utils.json_template_loader import load_templates
from streamlit_cookies_controller import CookieController

# Function to load templates
def load_letter_templates():
    try:
        letter_templates = load_templates("templates/letter_templates.json")
        cover_letter_templates = [template for template in letter_templates if "cover letter" in template["name"].lower()]
        cover_letter_template_names = [template["name"] for template in cover_letter_templates]
        return cover_letter_templates, cover_letter_template_names
    except Exception as e:
        st.error(f"Error loading cover letter templates: {e}")
        return [], []

def load_other_templates():
    try:
        referral_template = load_templates("templates/referral_template.json")["template"]
        connection_note_template = load_templates("templates/connection_note_template.json")["template"]
        return referral_template, connection_note_template
    except Exception as e:
        st.error(f"Error loading referral or connection note templates: {e}")
        return "", ""

# Function to process job posting and resume
def process_input(job_posting_text, resume_text):
    if not job_posting_text or not resume_text:
        return None, None

    job_details = extract_job_details_from_text(job_posting_text)
    resume_details = extract_resume_details_from_text(resume_text)
    comparison_results = compare_resume_and_job_description(resume_details, job_details)

    return job_details, resume_details, comparison_results

# Function to generate content based on selected templates
def generate_application_content(selected_application_types, custom_templates, cover_letter_template_names, cover_letter_templates, job_details, resume_details, referral_template, connection_note_template):
    job_application_email = ""
    referral_message = ""
    connection_note = ""

    if "Cover Letter" in selected_application_types:
        selected_cover_letter_template = "Custom Cover Letter" if custom_templates.get("cover_letter") else cover_letter_template_names[0]
        selected_template = custom_templates.get("cover_letter") or next(template for template in cover_letter_templates if template["name"] == selected_cover_letter_template)["template"]
        job_application_email += generate_job_application_email_dynamic(selected_template, resume_details, job_details) + "\n\n"

    if "Referral Message" in selected_application_types:
        referral_message = custom_templates.get("referral", "") or generate_job_referral_dynamic(referral_template, resume_details, job_details)

    if "LinkedIn Connection Request Note" in selected_application_types:
        connection_note = custom_templates.get("connection_note", "") or generate_connection_note_dynamic(connection_note_template, resume_details, job_details)

    return job_application_email, referral_message, connection_note

# Main function
def main():
    # Set page title and layout
    st.set_page_config(
        page_title="Jobingo - Your AI Job Application Assistant",
        page_icon="📄",
        layout="wide"
    )

    st.title("🤖 Jobingo")

    # Load templates
    cover_letter_templates, cover_letter_template_names = load_letter_templates()
    referral_template, connection_note_template = load_other_templates()

    # Create two columns for input and results
    input_col, results_col = st.columns([1, 2])

    controller = CookieController()

    # Initialize cookie manager for storing inputs
    job_posting_text = controller.get("job_posting_text") or ""
    resume_text = controller.get("resume_text") or ""
    custom_templates = controller.get("custom_templates") or {}

    # Input fields for job description and resume text
    with input_col:
        job_posting_text = st.text_area("Enter the Job Description", height=250, value=job_posting_text)
        resume_text = st.text_area("Enter the Resume Text", height=250, value=resume_text)

        # Application type selection
        selected_application_types = st.multiselect(
            "Choose Application Types",
            options=["Cover Letter", "Referral Message", "LinkedIn Connection Request Note"],
            default=["Cover Letter"]
        )

        # Cover letter template selection
        if "Cover Letter" in selected_application_types:
            available_templates = []
            if custom_templates.get("cover_letter"):
                available_templates.append("Custom Cover Letter")
            available_templates.extend(cover_letter_template_names)
            selected_cover_letter_template = st.selectbox(
                "Choose Cover Letter Template",
                options=available_templates,
                index=0
            )

        # Custom templates section
        with st.expander("Enter Custom Templates", expanded=False):
            custom_cover_letter = st.text_area("Custom Cover Letter Template", height=150, value=custom_templates.get("cover_letter", ""))
            custom_referral = st.text_area("Custom Referral Message Template", height=150, value=custom_templates.get("referral", ""))
            custom_connection_note = st.text_area("Custom Connection Note Template", height=150, value=custom_templates.get("connection_note", ""))
            save_button = st.button("Save")

            if save_button:
                custom_templates["cover_letter"] = custom_cover_letter if custom_cover_letter else ""
                custom_templates["referral"] = custom_referral if custom_referral else ""
                custom_templates["connection_note"] = custom_connection_note if custom_connection_note else ""
                st.success("Custom templates saved successfully!")
                controller.set("custom_templates", custom_templates)
                time.sleep(2)
                st.rerun()

        process_button = st.button("✨ Process")

    # Results section
    with results_col:
        placeholder = st.empty()
        st.markdown("""
            <style>
                .centered {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100%;
                    text-align: center;
                    color: #888888;
                    font-size: 18px;
                    width: 100%;
                }
            </style>
        """, unsafe_allow_html=True)

        if not job_posting_text or not resume_text:
            placeholder.markdown('<div class="centered">📝 Please input job description and resume details to process.</div>', unsafe_allow_html=True)
        else:
            if process_button:
                with st.spinner("Processing... Please wait ⏳"):
                    job_details, resume_details, comparison_results = process_input(job_posting_text, resume_text)

                    if job_details and resume_details:
                        # Generate application content
                        job_application_email, referral_message, connection_note = generate_application_content(
                            selected_application_types, custom_templates, cover_letter_template_names, cover_letter_templates,
                            job_details, resume_details, referral_template, connection_note_template
                        )

                        # Display results
                        st.subheader("⚖️ Comparison Results")
                        matching_score = comparison_results.get('matching_score', 0)
                        missing_skills = comparison_results.get('missing_skills', [])
                        missing_keywords = comparison_results.get('missing_keywords', [])
                        st.text(f"✅ Matching Score: {matching_score}/100\n\n❌ Missing Skills: {', '.join(missing_skills) if missing_skills else 'None'}\n\n❌ Missing Keywords: {', '.join(missing_keywords) if missing_keywords else 'None'}\n")

                        # Show generated content
                        if job_application_email:
                            st.subheader("📧 Generated Job Application Email")
                            st.text(job_application_email)
                        if referral_message:
                            st.subheader("🔗 Generated Referral Message")
                            st.text(referral_message)
                        if connection_note:
                            st.subheader("🔗 Generated LinkedIn Connection Note")
                            st.text(connection_note)

                        # Store inputs in cookies after processing
                        controller.set("job_posting_text", job_posting_text)
                        controller.set("resume_text", resume_text)
                    else:
                        placeholder.markdown('<div class="centered">📝 Error in processing the inputs, please check the text format.</div>', unsafe_allow_html=True)
            else:
                placeholder.markdown('<div class="centered">Click "Process" to start the magic 🚀</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
