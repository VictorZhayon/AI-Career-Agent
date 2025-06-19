RESUME_PROMPT = """
Rewrite this resume for a {target_role} position in ATS-optimized format:

Resume:
{resume}

Target Job Description:
{job_desc}

Instructions:
1. Extract and prioritize the most important keywords from the job description
2. Use professional formatting with clear section headers
3. Quantify achievements where possible
4. Keep length to 1-2 pages maximum
5. Output in plain text format
"""

COVER_LETTER_PROMPT = """
Create a professional cover letter for {job_title} at {company}:

Resume:
{resume}

Job Description:
{job_desc}

Guidelines:
1. Address hiring manager personally (use [Hiring Manager] if unknown)
2. Connect 3 key resume achievements to job requirements
3. Show awareness of {company}'s values and mission
4. Keep under 400 words
5. Use professional but approachable tone
"""