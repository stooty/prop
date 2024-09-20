import sqlite3
import pytesseract
from PIL import Image
import PyPDF2
import os
import json

# API-Needed: Replace this with actual Claude API client
from claude_api_client import ClaudeAPI

def extract_text_from_image(file_path):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def process_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
        return extract_text_from_image(file_path)
    elif file_extension.lower() == '.pdf':
        return extract_text_from_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

def generate_proposal(resume_text, job_description_text):
    # API-Needed: Replace this with actual Claude API call
    claude_api = ClaudeAPI()
    prompt = f"""
    Given the following resume and job description, create a compelling proposal for the freelancer to send to the employer. The proposal should:
    1. Be attention-grabbing and concise
    2. Highlight how the freelancer's experience and skills match the job requirements
    3. Include a bullet point list of steps the freelancer will take to complete the job
    
    Resume:
    {resume_text}
    
    Job Description:
    {job_description_text}
    """
    response = claude_api.generate_text(prompt)
    return response

def main(resume_id, job_description_id):
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()
    
    cursor.execute("SELECT file_path FROM uploads WHERE id = ?", (resume_id,))
    resume_path = cursor.fetchone()[0]
    
    cursor.execute("SELECT file_path FROM uploads WHERE id = ?", (job_description_id,))
    job_description_path = cursor.fetchone()[0]
    
    resume_text = process_file(resume_path)
    job_description_text = process_file(job_description_path)
    
    proposal = generate_proposal(resume_text, job_description_text)
    
    conn.close()
    
    return json.dumps({'success': True, 'proposal': proposal})

if __name__ == "__main__":
    import sys
    resume_id = int(sys.argv[1])
    job_description_id = int(sys.argv[2])
    print(main(resume_id, job_description_id))
