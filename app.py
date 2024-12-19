import streamlit as st
from services.job_detail_service import extract_job_details_from_text
from services.resume_detail_service import extract_resume_details_from_text
from services.comparison_service import compare_resume_and_job_description
from services.email_service import generate_job_application_email_dynamic

def main():
    # Set the page title and icon
    st.set_page_config(
        page_title="Job Application Assistant",  # Title of the page
        page_icon="📄",  # You can set an emoji or an image icon
        layout="wide"  # Set layout to wide
    )

    st.title("Job Application Assistant")

    # Create two columns: one for input and one for results
    input_col, results_col = st.columns([1, 2])  # The first column is 1x wide, the second is 2x wide

    # Input fields in the left column
    with input_col:
        job_posting_text = st.text_area("Enter the Job Description", height=250)
        job_type = st.selectbox("Select Job Description Type", ['single', 'multiple'])
        resume_text = st.text_area("Enter the Resume Text", height=250)
        process_button = st.button("Process")  # Move the button here

    # Results section in the right column with a placeholder
    with results_col:
        # Use st.markdown to inject CSS for centering content
        placeholder = st.empty()  # Create a placeholder in the right column
        
        # Custom CSS to center the content horizontally and vertically
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
            # Center the placeholder message both vertically and horizontally
            placeholder.markdown('<div class="centered">Please input job description and resume details to process.</div>', unsafe_allow_html=True)
        else:
            # Once the user inputs data, the placeholder will be replaced by the results
            if process_button:
                with st.spinner("Processing... Please wait"):
                    job_details = extract_job_details_from_text(job_posting_text)
                    resume_details = extract_resume_details_from_text(resume_text)
                    comparison_results = compare_resume_and_job_description(resume_details, job_details)
                    job_application_email = generate_job_application_email_dynamic(resume_details, job_details)

                # Display results
                st.subheader("Comparison Results")
                matching_score = comparison_results.get('matching_score', 0)
                missing_skills = comparison_results.get('missing_skills', [])
                missing_keywords = comparison_results.get('missing_keywords', [])

                match_text = f"Matching Score: {matching_score}/100\n\n"
                match_text += f"Missing Skills: {', '.join(missing_skills) if missing_skills else 'None'}\n\n"
                match_text += f"Missing Keywords: {', '.join(missing_keywords) if missing_keywords else 'None'}\n"

                st.text(match_text)
                st.subheader("Generated Job Application Email")
                st.text(job_application_email)

if __name__ == "__main__":
    main()
