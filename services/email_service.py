import json
from models.llm import llm

def generate_job_application_email_dynamic(letter_template, resume_details, job_details):
    prompt = f"""
    Letter template: 
    {letter_template}

    Resume Details:
    {json.dumps(resume_details, indent=4)}

    Job Description Details:
    {json.dumps(job_details, indent=4)}

    Instructions:
    Generate a cover letter using the provided letter template, resume details, and job description. Follow these instructions **strictly**:

    1. **Strict Adherence to Template**:
    - Follow the structure, format, and tone of the provided letter template exactly.
    - Use the resume and job description details to fill in the sections of the template.
    - Ensure that the content matches the job description while highlighting relevant skills and experiences from the resume.
    - Do not add any additional information or stray from the template in any way.

    2. **Content**:
    - Only include information that is present in the resume or job description. 
    - If any field is missing or irrelevant in either the resume or job description, omit it from the final letter. Do not leave any placeholders, blanks, or incomplete sections.
    - Use the job title from the job description where applicable.
    - Avoid redundancy—do not repeat information unless it is necessary for clarity.
    - Only include information that is available in the resume or job description. If any field (such as personal details, specific skills, or other job-related information) is missing, it should be excluded from the final letter.
    - If the template contains any placeholders for which no corresponding information is available, remove those placeholders from the letter.

    3. **Final Output**: Output **only** the completed letter, adhering **strictly** to the provided template. Do not include any explanations, placeholders, or additional information.
    """
    response = llm.invoke(input=prompt)
    
    email_content = response.content if hasattr(response, 'content') else str(response)
    
    return email_content.strip()
