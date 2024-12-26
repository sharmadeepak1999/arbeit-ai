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
    Create a referral request message using the provided resume details, job description, and referral template. If any required information is missing from the job description or resume, omit it from the final message. The content should highlight relevant skills and experiences from the resume that align with the job description. The final message must be clear, concise, and tailored to the job while maintaining professionalism. Avoid adding any explanations or additional content.
    """
    response = llm.invoke(input=prompt)
    
    referral_content = response.content if hasattr(response, 'content') else str(response)
    
    return referral_content.strip()
