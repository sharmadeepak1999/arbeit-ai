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
    Create a cover letter using the provided resume details, job description, and letter template. Ensure that the cover letter strictly adheres to the structure and tone of the template. The content should align closely with the job description while highlighting relevant skills and experiences from the resume. The final letter should be clear, concise, and no longer than 300 words. Do not output anything other than the letter itself, no explantion nothing.
    """
    response = llm.invoke(input=prompt)
    
    email_content = response.content if hasattr(response, 'content') else str(response)
    
    return email_content.strip()
