import google.generativeai as genai
import os
from .prompts import RESUME_PROMPT, COVER_LETTER_PROMPT
from dotenv import load_dotenv
load_dotenv()

class CareerAgent:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def transform_resume(self, resume: str, target_role: str, job_desc: str) -> str:
        prompt = RESUME_PROMPT.format(
            resume=resume,
            target_role=target_role,
            job_desc=job_desc
        )
        response = self.model.generate_content(prompt)
        return response.text.strip()

    def generate_cover_letter(self, resume: str, job_title: str, company: str, job_desc: str) -> str:
        prompt = COVER_LETTER_PROMPT.format(
            resume=resume,
            job_title=job_title,
            company=company,
            job_desc=job_desc
        )
        response = self.model.generate_content(prompt)
        return response.text.strip()
    