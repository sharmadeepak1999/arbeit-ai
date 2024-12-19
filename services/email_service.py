import json
from models.llm import llm

def generate_job_application_email_dynamic(resume_details, job_details):
    prompt = f"""
    You are tasked with writing a job application email in around 200 words that is professional, engaging, and memorable. The letter must be inspired by the following examples, without any extra text, code, or explanation.

    ### Template:

    Dear Hiring Team,

    I was browsing through your job posting and had a moment of realization: this is the job for me. Not only does it align perfectly with my skills, but I also happen to have a knack for solving problems with the same level of enthusiasm I show when discovering new pizza toppings. You’re looking for someone with experience in Python, JavaScript, and Django—check, check, and check.

    Let me introduce myself a little better. I’m a software developer who thrives in challenging environments. I’ve built apps that solve real-world problems, like a to-do list app that estimates task duration using Python and Django. You can check out that project on my GitHub. I’m excited to bring my technical abilities, along with my enthusiasm for coding, to your team.

    While my resume will give you a rundown of my qualifications, what I really want to showcase is my passion for building technology that makes a difference. I’m not just looking for any job—I’m looking for a place where I can grow, contribute, and continue learning. If you’re looking for someone who brings both skill and energy to the table, then we should definitely talk.

    Looking forward to hearing from you soon,
    [Your Name]
    
    ### Instructions:
    - Stick to the template no matter what happens.
    - **Start with a self-aware and confident introduction** that references your skills honestly while making the story memorable. Use humor or a playful tone that reflects your personality.
    - **Highlight your education, college, current company/role and skills** clearly, aligning them with the job requirements. The tone should be **professional** but also **engaging**.
    - **Include examples of your work or projects** in the body of the letter, similar to the second example. Keep the focus on your capabilities rather than over-selling them.
    - Ensure the tone is **authentic**, mixing confidence with humor without being over-the-top.
    - The letter should feel **engaging and human**, but still reflect your qualifications and enthusiasm for the role.
    - Keep the letter **concise** (around 200 words), ensuring clarity and brevity.
    - The letter should be **memorable** and show personality without compromising professionalism.

    Resume Details:
    {json.dumps(resume_details, indent=4)}

    Job Description Details:
    {json.dumps(job_details, indent=4)}
    """
    
    response = llm.invoke(input=prompt)
    
    email_content = response.content if hasattr(response, 'content') else str(response)
    
    return email_content.strip()
