import streamlit as st
from backend.agent import CareerAgent
from backend.utils import parse_resume
import os
import base64
from datetime import datetime

# Initialize session state
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'last_resume_file' not in st.session_state:
    st.session_state.last_resume_file = None

# Initialize agent
try:
    agent = CareerAgent()
except Exception as e:
    st.error(f"Agent initialization failed: {str(e)}")
    st.stop()

# UI Configuration
st.set_page_config(
    page_title="AI Career Agent",
    layout="wide",
    page_icon="💼"
)

# Custom CSS
# st.markdown("""
# <style>
#     .stProgress > div > div > div > div {
#         background-color: #1DA1F2;
#     }
#     .stTextArea [data-baseweb=base-input] {
#         background-color: #F8F9FA;
#     }
#     .stDownloadButton button {
#         width: 100%;
#     }
#     .section-header {
#         border-bottom: 2px solid #1DA1F2;
#         padding-bottom: 0.5rem;
#         margin-bottom: 1rem;
#     }
#     .feature-card {
#         border-radius: 10px;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#         padding: 1.5rem;
#         margin-bottom: 1.5rem;
#         background: white;
#     }
# </style>
# """, unsafe_allow_html=True)

# Header
col = st.columns(1)
with col[0]:
    st.title("🛠 AI Career Agent")
    st.caption("Gemini-powered job application assistant - Transform resumes, generate cover letters, and land your dream job")
    st.caption("Built with ❤️ by Victor Zion | Version 1.0 | MVP Release")

# Feature Tabs
tab1, tab2 = st.tabs(["📝 Resume Transformer", "✉️ Cover Letter Generator"])

# Resume Transformation Feature
with tab1:
    st.header("📝 ATS-Optimized Resume Transformation", anchor="resume-transformer")
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    
    with st.form("resume_form"):
        c1, c2 = st.columns(2)
        with c1:
            uploaded_file = st.file_uploader(
                "Upload Resume", 
                type=["pdf", "txt"],
                help="PDF or text files only"
            )
        with c2:
            target_role = st.text_input(
                "Target Role/Position",
                placeholder="e.g., Senior Data Scientist",
                help="The job title you're applying for"
            )
            
        job_desc = st.text_area(
            "Paste Job Description",
            height=200,
            placeholder="Copy-paste the full job description here...",
            help="For best results, include the full job posting"
        )
        
        submitted = st.form_submit_button(
            "✨ Transform Resume", 
            use_container_width=True
        )
    
    if submitted:
        if not uploaded_file:
            st.warning("Please upload a resume file")
            st.stop()
        if not target_role:
            st.warning("Please specify target role")
            st.stop()
            
        with st.spinner("Parsing resume..."):
            resume_text = parse_resume(uploaded_file)
            st.session_state.resume_text = resume_text
            st.session_state.last_resume_file = uploaded_file.name
            
        with st.spinner("Optimizing for ATS systems..."):
            try:
                transformed = agent.transform_resume(
                    resume_text, 
                    target_role, 
                    job_desc
                )
                st.session_state.transformed_resume = transformed
            except Exception as e:
                st.error(f"Transformation failed: {str(e)}")
                st.stop()
    
    if 'transformed_resume' in st.session_state:
        st.subheader("Optimized Resume", divider="blue")
        
        # Download button with filename
        filename = f"AI_Career_Agent_Optimized_Resume{datetime.now().strftime('%Y%m%d')}.pdf"
        b64 = base64.b64encode(st.session_state.transformed_resume.encode()).decode()
        href = f'<a href="data:file/pdf;base64,{b64}" download="{filename}">⬇️ Download Optimized Resume</a>'
        st.markdown(href, unsafe_allow_html=True)
        
        # Preview with expander
        with st.expander("Preview Transformed Resume", expanded=True):
            st.text_area(
                "Optimized Content", 
                st.session_state.transformed_resume,
                height=500,
                label_visibility="collapsed"
            )
            
        # Feedback mechanism
        # st.subheader("How did we do?")
        # feedback = st.radio(
        #     "Quality of optimization:",
        #     ["Excellent", "Good", "Needs improvement"],
        #     horizontal=True
        # )
        # if st.button("Submit Feedback"):
        #     st.success("Thank you for your feedback! We'll use this to improve Career Agent")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Cover Letter Generation Feature
with tab2:
    st.header("✉️ Personalized Cover Letter Generator", anchor="cover-letter")
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    
    if not st.session_state.resume_text:
        st.info("ℹ️ Upload your resume in the Resume Transformer tab first")
    
    with st.form("cover_letter_form"):
        c1, c2 = st.columns(2)
        with c1:
            company = st.text_input(
                "Company Name",
                placeholder="e.g., Google",
                help="The company you're applying to"
            )
        with c2:
            job_title = st.text_input(
                "Job Title",
                placeholder="e.g., Machine Learning Engineer",
                help="Position you're applying for"
            )
            
        cover_job_desc = st.text_area(
            "Paste Job Description",
            height=200,
            placeholder="Copy-paste the job description here...",
            key="cover_job_desc"
        )
        
        # Personalization options
        with st.expander("Advanced Options"):
            tone = st.select_slider(
                "Writing Tone",
                options=["Formal", "Professional", "Enthusiastic", "Creative"],
                value="Professional"
            )
            highlight = st.text_input(
                "Key Achievement to Highlight",
                placeholder="e.g., Increased conversion by 30%",
                help="Specific accomplishment to emphasize"
            )
        
        submitted_cover = st.form_submit_button(
            "✨ Generate Cover Letter", 
            use_container_width=True
        )
    
    if submitted_cover:
        if not st.session_state.resume_text:
            st.warning("Please upload your resume in the Resume Transformer tab first")
            st.stop()
        if not company or not job_title:
            st.warning("Please provide company name and job title")
            st.stop()
            
        with st.spinner("Crafting personalized cover letter..."):
            try:
                cover_letter = agent.generate_cover_letter(
                    st.session_state.resume_text,
                    job_title,
                    company,
                    cover_job_desc
                )
                st.session_state.cover_letter = cover_letter
            except Exception as e:
                st.error(f"Generation failed: {str(e)}")
                st.stop()
    
    if 'cover_letter' in st.session_state:
        st.subheader("Generated Cover Letter", divider="green")
        
        # Download button
        filename = f"{company.replace(' ', '_')}_cover_letter_{datetime.now().strftime('%Y%m%d')}.docx"
        b64 = base64.b64encode(st.session_state.cover_letter.encode()).decode()
        href = f'<a href="data:file/docx;base64,{b64}" download="{filename}">⬇️ Download Cover Letter</a>'
        st.markdown(href, unsafe_allow_html=True)
        
        # Preview with expander
        with st.expander("Preview Cover Letter", expanded=True):
            st.text_area(
                "Cover Letter Content", 
                st.session_state.cover_letter,
                height=400,
                label_visibility="collapsed"
            )
        
        # Personalization options
        if st.button("🔄 Regenerate with Different Tone"):
            st.session_state.pop('cover_letter', None)
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API status
    if os.getenv("GEMINI_API_KEY"):
        st.success("Gemini Engaged")
    else:
        st.error("Gemini Disengaged")
    
    # Resume info
    if st.session_state.resume_text:
        st.subheader("Current Resume")
        st.caption(f"File: {st.session_state.last_resume_file or 'Not specified'}")
        st.caption(f"{len(st.session_state.resume_text.splitlines())} lines parsed")
        if st.button("Clear Resume"):
            st.session_state.resume_text = ""
            st.session_state.last_resume_file = None
            st.session_state.pop('transformed_resume', None)
            st.experimental_rerun()
    
    # System info
    st.divider()
    st.subheader("About Career Agent")
    st.caption("Version 1.0 | MVP Release")
    st.caption("Core Features:")
    st.markdown("- ATS-optimized resume transformation")
    st.markdown("- AI-generated personalized cover letters")
    st.markdown("- Job description analysis")
    
    # st.divider()
    # st.markdown("**Next Phase Features:**")
    # st.markdown("- STAR interview preparation")
    # st.markdown("- LinkedIn profile optimization")
    # st.markdown("- Salary negotiation scripts")

# Footer
st.divider()
footer_cols = st.columns(3)
with footer_cols[1]:
    st.caption("© 2024 AI Career Agent | Powered by Google Gemini | Created by Victor Zion with ❤️ and ☕")