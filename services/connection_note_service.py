import json
from models.llm import llm

def generate_connection_note_dynamic(connection_note_template, resume_details, job_details):
    prompt = f"""
    Connection note template: 
    {connection_note_template}
    
    Resume Details:
    {json.dumps(resume_details, indent=4)}

    Job Description Details:
    {json.dumps(job_details, indent=4)}
    
    Instructions:
    Create a linkedin connection request note using the provided resume details, job description, and template. Ensure that the message strictly adheres to the structure and tone of the template. The content should be aligned with the job description while highlighting relevant skills and experiences from the resume. The final message should be clear, concise and within 200 characters. Do not output anything other than the note itself, no explantion nothing.
    """
    response = llm.invoke(input=prompt)
    
    note_content = response.content if hasattr(response, 'content') else str(response)
    
    return note_content.strip()
