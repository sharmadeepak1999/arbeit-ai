import json
from models.llm import llm

def extract_resume_details_from_text(resume_text):
    prompt = f"""
    Extract the following details from the resume into a JSON object. The JSON should have the following keys:
    - "applicant_name": The applicant's name, properly capitalized and formatted.
    - "skills": An array of unique skills.
    - "keywords": An array of important keywords.
    - "latest_education": The most recent education degree (e.g., Bachelor's, Master's, etc.).
    - "latest_college_name": The name of the college or university for the latest education.
    - "current_company": The name of the current company.
    - "current_role": The current job role.
    - "contact_information": An object containing phone number, email address, and LinkedIn (if available).
    - "work_experience": A list of previous job titles, companies, and durations.
    - "certifications": An array of certifications or additional training completed.
    - "languages": An array of languages spoken and proficiency levels.
    - "achievements": A list of notable professional or academic achievements.
    - "projects": A list of specific projects the applicant has worked on, including the scope and role.
    - "location": The current city or region of the applicant.
    - "hobbies_interests": An array of personal interests or hobbies.
    - "volunteer_experience": A list of volunteer work or community involvement.
    - "references": A list of references (if available).
    - "social_media_profiles": A list of links to professional social media profiles (e.g., LinkedIn, GitHub).
    Resume Text: {resume_text}

    Output only the JSON data. Do not include any extra text, explanation, or formatting.
    """

    response = llm.invoke(input=prompt)
    response_content = response.content if hasattr(response, 'content') else str(response)
    cleaned_response = response_content.strip("```").strip()

    if cleaned_response.startswith('json\n'):
        cleaned_response = cleaned_response[5:].strip()

    try:
        details = json.loads(cleaned_response)
    except json.JSONDecodeError:
        details = {"error": "Failed to parse the response into JSON", "response": cleaned_response}
    
    return details
