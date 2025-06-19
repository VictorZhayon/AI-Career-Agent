RESUME_PROMPT = """
Rewrite this resume for a {target_role} position in ATS-optimized format:

Resume:
{resume}

Target Job Description:
{job_desc}

Instructions:
1. Prioritize keywords: {job_desc_keywords}
2. Use professional formatting with clear section headers
3. Quantify achievements
4. Max 1-2 pages
5. Output in plain text format
"""

COVER_LETTER_PROMPT = """
Create a professional cover letter for {job_title} at {company}:

Resume:
{resume}

Job Description:
{job_desc}

Guidelines:
1. Address: [Hiring Manager] if unknown
2. Connect 3 key achievements to requirements
3. Show company awareness
4. Max 400 words
"""