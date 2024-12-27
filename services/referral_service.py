import json
from models.llm import llm

def generate_job_referral_dynamic(referral_template, resume_details, job_details):
    prompt = f"""
    Referral template: 
    {referral_template}

    Resume Details:
    {json.dumps(resume_details, indent=4)}

    Job Description Details:
    {json.dumps(job_details, indent=4)}

    Instructions:
    Create a referral request message using the provided referral template, resume details, and job description. Follow these instructions strictly:

    1. **Strict Adherence to Template**: 
    - Follow the structure, format, and tone of the provided referral template exactly.
    - Use the resume and job description details to fill in the sections of the template, ensuring that the content aligns with the job description and highlights relevant skills and experiences from the resume.

    2. **Content**:
    - Only include information that is available in the resume or job description. If any field (such as personal details, specific skills, or other job-related information) is missing, it should be excluded from the final letter.
    - If the template contains any placeholders for which no corresponding information is available, remove those placeholders from the letter.

    3. **Clarity and Conciseness**: 
    - Ensure that the final message is clear, concise, and directly relevant to the job.
    - Keep the content focused on the job description and resume without adding any unnecessary details or explanations.

    4. **Final Output**: 
    - Output only the completed referral request message, adhering strictly to the provided template. Do not add any explanations, additional content, or modifications beyond the template structure.
    """

    response = llm.invoke(input=prompt)
    
    referral_content = response.content if hasattr(response, 'content') else str(response)
    
    return referral_content.strip()
