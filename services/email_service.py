import json
from models.llm import llm

def generate_job_application_email_dynamic(resume_details, job_details):
    prompt = f"""
    Role and Style Setup: You are a cover letter generator. Your task is to create a professional and concise cover letter for a Generative AI Software Engineer role.

    Cover Letter Structure Instruction: To compose a compelling cover letter, you must scrutinize the job description for key qualifications. Begin with a succinct introduction about the candidate's identity and career goals. Highlight skills aligned with the job, underpinned by tangible examples. Incorporate details about the company, emphasizing its mission or unique aspects that align with the candidate's values. Conclude by reaffirming the candidate's suitability, inviting further discussion. Use job-specific terminology for a tailored and impactful letter, maintaining a professional style suitable for a Generative AI Software Engineer role. Please provide your response in under 350 words.

    The letter should be within 300 words, given the context of the letter is not lost and the details are not lost.
    
    Resume Details:
    {json.dumps(resume_details, indent=4)}

    Job Description Details:
    {json.dumps(job_details, indent=4)}
    """
    
    response = llm.invoke(input=prompt)
    
    email_content = response.content if hasattr(response, 'content') else str(response)
    
    return email_content.strip()
