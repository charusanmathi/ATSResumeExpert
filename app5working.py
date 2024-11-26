from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
import requests
from PIL import Image 
import pdf2image
import google.generativeai as genai
from google.cloud import language_v1

# Set up environment variables and API keys
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/Users/charulatha/Documents/Data Science/End to End Projects/Krish Naik/Python/GenAIprojects/ATS.json'
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Function to setup PDF file
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [{"mime_type": "image/jpeg", "data": base64.b64encode(img_byte_arr).decode()}]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Google NLP Keyword Extraction
def extract_keywords(job_description):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=job_description, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(document=document)
    keywords = [entity.name for entity in response.entities if entity.type == language_v1.Entity.Type.KEYWORD]
    return keywords

# Streamlit App UI
st.set_page_config(page_title="ATS Resume Expert", layout="wide")

# Sidebar for actions
st.sidebar.title("Actions")
action = st.sidebar.radio("Select an action", [
    "Tell Me About the Resume",
    "How Can I Improve my Skills",
    "Percentage Match",
    "Recommendations to Improve ATS Score",
    "Modify into Measurable Achievements",
    "Keyword Recommendations",
    "Rewrite Resume to Suit Job Description",
    "Generate Cover Letter"
])

# Header
st.header("ATS Tracking System")
st.write("Upload a PDF resume and job description to get started.")

# File uploader and text input for job description
input_text = st.text_area("Job Description:", key="input", height=200)
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

# Button to process resume and job description
submit_button = st.button("Process Resume")

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")
    pdf_content = input_pdf_setup(uploaded_file)

    if submit_button:
        if action == "Tell Me About the Resume":
            prompt = """
            You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
            Please share your professional evaluation on whether the candidate's profile aligns with the role. 
            Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
            """
            response = get_gemini_response(input_text, pdf_content, prompt)
            st.subheader("The Response is:")
            st.write(response)

        elif action == "How Can I Improve my Skills":
            prompt = """
            You are an HR consultant with technical knowledge across multiple domains. Your task is to evaluate the skills listed on the candidate's resume compared to the job description.
            Identify any critical skills, tools, or certifications that are missing but highly valued for this role.
            Provide actionable advice on specific technical and soft skills the candidate could develop or improve to better align with the requirements of their target job.
            """
            response = get_gemini_response(input_text, pdf_content, prompt)
            st.subheader("Skill Improvement Suggestions:")
            st.write(response)

        elif action == "Percentage Match":
            prompt = """
            You are an expert ATS scanner with deep knowledge of data science, software development, and ATS functionality.
            Based on the provided job description, evaluate the resume to calculate a compatibility match score as a percentage.
            After the percentage, list the missing keywords or skills that prevent a higher match score and provide any brief thoughts on how these might be improved in the resume.
            """
            response = get_gemini_response(input_text, pdf_content, prompt)
            st.subheader("Percentage Match:")
            st.write(response)

        elif action == "Recommendations to Improve ATS Score":
            prompt = """
            You are an ATS optimization specialist with expertise in resume parsing and matching algorithms.
            Review the candidate's resume and provide recommendations on how to improve their ATS score for the given job description.
            Suggest specific keywords, phrases, and structuring tips that could make the resume more ATS-friendly, focusing on areas like formatting, keywords alignment, and section optimization.
            Conclude with actionable insights for enhancing visibility in an ATS system.
            """
            response = get_gemini_response(input_text, pdf_content, prompt)
            st.subheader("ATS Score Improvement Recommendations:")
            st.write(response)

        elif action == "Modify into Measurable Achievements":
            prompt = """
            You are a professional resume editor with a talent for translating job roles and responsibilities into impactful, measurable achievements.
            Review the candidate’s resume and identify sections where responsibilities could be transformed into quantified accomplishments.
            Rewrite key responsibilities or vague statements to make them results-oriented and backed by metrics (e.g., “Increased team efficiency by 30%” or “Led a project that reduced processing time by 50%”).
            Provide improved, measurable versions of statements from the resume to enhance its impact.
            """
            response = get_gemini_response(input_text, pdf_content, prompt)
            st.subheader("Measurable Achievements Suggestions:")
            st.write(response)

        elif action == "Keyword Recommendations":
            prompt = """
            You are an expert in keyword optimization for resumes. Based on the provided job description and resume,
            suggest important keywords and phrases the candidate should include to improve their ATS score.
            Provide a list of relevant technical and non-technical keywords and explain their importance in making the resume more visible to ATS systems.
            """
            response = get_gemini_response(input_text, pdf_content, prompt)
            st.subheader("Keyword Recommendations:")
            st.write(response)

        elif action == "Rewrite Resume to Suit Job Description":
            prompt = """
            You are an expert resume writer. Based on the uploaded resume and the provided job description,
            rewrite the resume to better suit the job description, making sure not to include any false or fabricated information.
            Ensure that all the information is directly pulled from the resume, highlighting the most relevant skills and experiences to match the job description.
            """
            response = get_gemini_response(input_text, pdf_content, prompt)
            st.subheader("Rewritten Resume:")
            st.write(response)

        elif action == "Generate Cover Letter":
            prompt = """
            You are an expert cover letter writer. Based on the following job description and the candidate's resume, generate a tailored cover letter for this role.
            The cover letter should:
            1. Reflect only the skills, experience, and qualifications listed in the candidate's resume.
            2. Not include any new, additional, or fabricated information.
            3. Emphasize how the candidate’s existing skills and experience align with the job requirements.
            """
            response = get_gemini_response(input_text, pdf_content, prompt)
            st.subheader("Generated Cover Letter:")
            st.write(response)

else:
    st.write("Please upload a resume and provide a job description to proceed.")
