import json
from models.llm import llm

def compare_resume_and_job_description(resume_json, job_json):
    prompt = f"""
    You are given two JSON objects: one containing skills and keywords from a resume, and the other from a job description.
    Compare them and provide the result **ONLY** in JSON format, without any extra text, code, or explanation.

    Resume JSON:
    {json.dumps(resume_json, indent=4)}

    Job Description JSON:
    {json.dumps(job_json, indent=4)}

    Task:
    - Compare the skills and keywords between the resume and job description.
    - Calculate a matching score out of 100, reflecting how well the resume matches the job description.
    - Identify the skills and keywords from the job description that are missing in the resume.
    - Consider variations in skill/keyword names (e.g., "JavaScript" vs "JS") and treat them as matches.

    {{"matching_score": <matching_score_out_of_100>, "missing_skills": <list_of_skills_missing_in_resume>, "missing_keywords": <list_of_keywords_missing_in_resume>}}
    """

    response = llm.invoke(input=prompt)
    response_content = response.content if hasattr(response, 'content') else str(response)
    cleaned_response = response_content.strip("```").strip()

    if cleaned_response.startswith('json\n'):
        cleaned_response = cleaned_response[5:].strip()

    try:
        comparison_results = json.loads(cleaned_response)
    except json.JSONDecodeError:
        comparison_results = {"error": "Failed to parse the response into JSON", "response": cleaned_response}

    return comparison_results
