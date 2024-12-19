import json
from models.llm import llm

def extract_job_details_from_text(job_description_text):
    prompt = f"""
    Extract the following details from the job posting in JSON format only. 
    Do not include any extra text, explanations, or formatting outside of the JSON:
    - "company_name": The name of the company.
    - "role": The job title or role.
    - "years_of_experience_required": The number of years of experience required (if specified).
    - "contact_email": The contact email address (if available).
    - "apply_link": The application link (if available).
    - "skills": An array of skills mentioned in the job description.
    - "keywords": An array of important keywords mentioned in the job description.
    - "job_location": The location or region where the job is based.
    - "salary_range": Any salary range or compensation details mentioned.
    - "employment_type": The type of employment (e.g., full-time, part-time, contract, internship).
    - "work_schedule": Any details about the work schedule (e.g., remote, hybrid, shift timings).
    - "company_description": A brief overview of the company or its industry.
    - "benefits": Any benefits or perks offered (e.g., health insurance, retirement plans).
    - "education_requirements": Specific education qualifications or degrees required.
    - "certifications_required": Any specific certifications required for the role.
    - "job_responsibilities": A list of key job responsibilities or duties.
    - "desired_qualities": Soft skills or personal qualities desired in the candidate.
    - "career_growth_opportunities": Information about potential growth and development within the company.
    - "application_deadline": The deadline for submitting the application (if provided).
    - "company_website": The company's website or link to more information.
    - "recruiter_name": Name of the recruiter or hiring manager (if available).
    - "recruiter_contact_info": Contact details for the recruiter (if available).
    Job Posting: {job_description_text}
    """

    response = llm.invoke(input=prompt)
    response_content = response.content if hasattr(response, 'content') else str(response)
    cleaned_response = response_content.strip("```").strip()

    if cleaned_response.startswith('json\n'):
        cleaned_response = cleaned_response[5:].strip()

    try:
        job_details = json.loads(cleaned_response)
    except json.JSONDecodeError:
        job_details = {"error": "Failed to parse the response into JSON", "response": cleaned_response}
    
    return job_details
