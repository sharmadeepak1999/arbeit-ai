import streamlit as st
from services.job_detail_service import extract_job_details_from_text
from services.resume_detail_service import extract_resume_details_from_text
from services.comparison_service import compare_resume_and_job_description
from services.email_service import generate_job_application_email_dynamic
from services.referral_service import generate_job_referral_dynamic
from services.connection_note_service import generate_connection_note_dynamic
from utils.json_template_loader import load_templates
from streamlit_cookies_controller import CookieController
import os

def main():
    # Set the page title and icon
    st.set_page_config(
        page_title="JobKart - Your AI Job Application Assistant",
        page_icon="📄",
        layout="wide"
    )

    st.title("🤖 JobKart")

    # Load letter templates from JSON file
    try:
        letter_templates = load_templates("templates/letter_templates.json")
        cover_letter_templates = [template for template in letter_templates if "cover letter" in template["name"].lower()]
        cover_letter_template_names = [template["name"] for template in cover_letter_templates]
    except Exception as e:
        st.error(f"Error loading cover letter templates: {e}")
        return
    
    # Load referral template (only one template)
    try:
        referral_template = load_templates("templates/referral_template.json")["template"]  # Assuming there's only one template
        connection_note_template = load_templates("templates/connection_note_template.json")["template"]  # Assuming there's only one template
    except Exception as e:
        st.error(f"Error loading referral or connection note templates: {e}")
        return

    # Create two columns: one for input and one for results
    input_col, results_col = st.columns([1, 2])

    controller = CookieController()

    # Initialize cookie manager
    job_posting_text = controller.get("job_posting_text") or ""
    resume_text = controller.get("resume_text") or ""
    
    # Load custom templates from cookies if they exist
    custom_templates = controller.get("custom_templates") or {}

    # Input fields in the left column
    with input_col:
        # Displaying input fields
        job_posting_text = st.text_area("Enter the Job Description", height=250, value=job_posting_text)
        resume_text = st.text_area("Enter the Resume Text", height=250, value=resume_text)

        # Multi-select options for different application types
        selected_application_types = st.multiselect(
            "Choose Application Types",
            options=["Cover Letter", "Referral Message", "LinkedIn Connection Request Note"],
            default=["Cover Letter"]  # Default to showing Cover Letter
        )

        # If "Cover Letter" is selected, show template options (single-select)
        if "Cover Letter" in selected_application_types:
            # Check if custom cover letter exists, and if so, add it as the first option
            available_templates = []
            if custom_templates.get("cover_letter"):
                available_templates.append("Custom Cover Letter")  # Add custom option as the first option

            # Add predefined templates after custom template if available
            available_templates.extend(cover_letter_template_names)

            # Set the default option to the first one if available
            selected_cover_letter_template = st.selectbox(
                "Choose Cover Letter Template",  # Dropdown for cover letter templates
                options=available_templates,
                index=0  # Default to the first option (custom if available, else the first predefined template)
            )

        # Display input fields for custom templates (closed by default)
        with st.expander("Enter Custom Templates", expanded=False):  # Setting expanded=False to keep it closed by default
            # Create text areas for custom templates
            custom_cover_letter = st.text_area("Custom Cover Letter Template", height=150, value=custom_templates.get("cover_letter", ""))
            custom_referral = st.text_area("Custom Referral Message Template", height=150, value=custom_templates.get("referral", ""))
            custom_connection_note = st.text_area("Custom Connection Note Template", height=150, value=custom_templates.get("connection_note", ""))

            # Add a button to save custom templates
            save_button = st.button("Save Custom Templates")

            # Save the templates when the button is clicked
            if save_button:
                custom_templates["cover_letter"] = custom_cover_letter if custom_cover_letter else ""
                custom_templates["referral"] = custom_referral if custom_referral else ""
                custom_templates["connection_note"] = custom_connection_note if custom_connection_note else ""

                # Store custom templates in cookies
                controller.set("custom_templates", custom_templates)

                # Show success message
                st.success("Custom templates saved successfully!")

                # Refresh the page
                st.rerun()

        # Define a session state for the button
        if "process_clicked" not in st.session_state:
            st.session_state.process_clicked = False

        process_button = st.button(
            "✨ Process",
            disabled=st.session_state.process_clicked
        )

    # Results section in the right column
    with results_col:
        placeholder = st.empty()

        # CSS for centering content
        st.markdown(
            """
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
            """,
            unsafe_allow_html=True
        )

        if not job_posting_text or not resume_text:
            placeholder.markdown('<div class="centered">📝 Please input job description and resume details to process.</div>', unsafe_allow_html=True)
        else:
            if process_button:
                # Set the session state to disable the button
                st.session_state.process_clicked = True

                with st.spinner("Processing... Please wait ⏳"):
                    # Process the inputs
                    job_details = extract_job_details_from_text(job_posting_text)
                    resume_details = extract_resume_details_from_text(resume_text)
                    comparison_results = compare_resume_and_job_description(resume_details, job_details)

                    # Prepare the selected templates for each type
                    job_application_email = ""
                    referral_message = ""
                    connection_note = ""
                    
                    # Generate cover letter(s)
                    if "Cover Letter" in selected_application_types:
                        if selected_cover_letter_template == "Custom Cover Letter" and custom_templates.get("cover_letter"):
                            # Use custom cover letter template
                            selected_template = custom_templates["cover_letter"]
                        else:
                            # Use predefined template
                            selected_template = next(template for template in cover_letter_templates if template["name"] == selected_cover_letter_template)["template"]
                        job_application_email += generate_job_application_email_dynamic(selected_template, resume_details, job_details) + "\n\n"
                    
                    # Generate LinkedIn referral message (using the single template)
                    if "Referral Message" in selected_application_types:
                        referral_message = custom_templates.get("referral", "") or generate_job_referral_dynamic(referral_template, resume_details, job_details)

                    # Generate LinkedIn connection request note (using the single template)
                    if "LinkedIn Connection Request Note" in selected_application_types:
                        connection_note = custom_templates.get("connection_note", "") or generate_connection_note_dynamic(connection_note_template, resume_details, job_details)

                # Reset the session state to enable the button after processing
                st.session_state.process_clicked = False

                # Display results
                st.subheader("⚖️ Comparison Results")
                matching_score = comparison_results.get('matching_score', 0)
                missing_skills = comparison_results.get('missing_skills', [])
                missing_keywords = comparison_results.get('missing_keywords', [])

                match_text = f"✅ Matching Score: {matching_score}/100\n\n"
                match_text += f"❌ Missing Skills: {', '.join(missing_skills) if missing_skills else 'None'}\n\n"
                match_text += f"❌ Missing Keywords: {', '.join(missing_keywords) if missing_keywords else 'None'}\n"

                st.text(match_text)
                
                # Display generated content
                if job_application_email:
                    st.subheader("📧 Generated Job Application Email")
                    st.text(job_application_email)
                
                if referral_message:
                    st.subheader("🔗 Generated Referral Message")
                    st.text(referral_message)

                if connection_note:
                    st.subheader("🔗 Generated LinkedIn Connection Note")
                    st.text(connection_note)

                # Save inputs to cookies after the button is clicked
                controller.set("job_posting_text", job_posting_text)
                controller.set("resume_text", resume_text)

            else:
                placeholder.markdown('<div class="centered">Click "Process" to start the magic 🚀</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
