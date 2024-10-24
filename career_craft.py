import streamlit as st
import fitz 
from dotenv import load_dotenv
import os

load_dotenv()

st.title("CareerCraft: ATS-Optimized Resume Analyzer")

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "job_description_text" not in st.session_state:
    st.session_state.job_description_text = ""

uploaded_resume = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if st.button("Submit Resume"):
    if uploaded_resume:
        resume_path = "uploaded_resume.pdf"

        with open(resume_path, "wb") as f:
            f.write(uploaded_resume.getbuffer())

        doc_resume = fitz.open(resume_path)
        resume_text = ""
        for page in doc_resume:
            resume_text += page.get_text()
        doc_resume.close()

        st.session_state.resume_text = resume_text

if st.session_state.resume_text:
    st.subheader("Extracted Resume Text:")
    st.text_area("Resume Text", st.session_state.resume_text, height=300)

uploaded_job_description = st.text_area("Paste your job description (text)")

if st.button("Submit Job Description"):
    if uploaded_job_description:
        st.session_state.job_description_text = uploaded_job_description

if st.session_state.job_description_text:
    st.subheader("Job Description:")
    st.text_area("Job Description Text", st.session_state.job_description_text, height=300)

stop_words = set([
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
    "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was",
    "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and",
    "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between",
    "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on",
    "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all",
    "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same",
    "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"
])

if st.session_state.resume_text and st.session_state.job_description_text:
    if st.button("Analyze"):
        resume_words = set(word for word in st.session_state.resume_text.lower().split() if word not in stop_words)
        job_description_words = set(word for word in st.session_state.job_description_text.lower().split() if word not in stop_words)

        matching_keywords = resume_words.intersection(job_description_words)
        missing_keywords = job_description_words.difference(resume_words)

        fit_percentage = (len(matching_keywords) / len(job_description_words)) * 100 if job_description_words else 0

        st.subheader("Analysis Results:")
        st.write(f"**Matching Keywords ({len(matching_keywords)}):**")
        st.write(matching_keywords)

        st.write(f"**Missing Keywords ({len(missing_keywords)}):**")
        st.write(missing_keywords)

        st.write(f"**Fit Percentage:** {fit_percentage:.2f}%")

        if fit_percentage >= 75:
            st.success("Your resume is a good fit for the job description!")
        elif fit_percentage >= 50:
            st.warning("Your resume is a fair fit for the job description.")
        else:
            st.error("Your resume may not be a good fit for the job description.")
else:
    st.write("Please upload a resume and submit both inputs before analysis.")
