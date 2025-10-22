import streamlit as st
from utils.resume_parser import ResumeParser
from utils.ats_scorer import ATSScorer
from utils.job_predictor import JobRolePredictor
from utils.resume_improver import ResumeImprover
import json

import os
import subprocess

# Auto-download spaCy model if missing
try:
    import spacy
    nlp = spacy.load('en_core_web_sm')
except OSError:
    subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'])
    nlp = spacy.load('en_core_web_sm')

# Auto-download NLTK data if missing
import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

# Set page config must be first
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/resume-analyzer',
        'Report a bug': 'https://github.com/yourusername/resume-analyzer/issues',
        'About': '# AI Resume Analyzer\nBuilt with ❤️ for College Project Expo'
    }
)

# Page config
st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")

# Initialize
parser = ResumeParser()
scorer = ATSScorer()
predictor = JobRolePredictor()
improver = ResumeImprover()

# Cache model training
@st.cache_resource
def get_trained_predictor():
    pred = JobRolePredictor()
    pred.train()
    return pred

predictor = get_trained_predictor()

# Title
st.title("📄 AI Resume Analyzer & Job Matcher")
st.markdown("Upload your resume and get instant AI-powered analysis!")

# File uploader (moved here to avoid NameError)
uploaded_file = st.file_uploader("📤 Upload your Resume", type=['txt', 'pdf', 'docx'])

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    Ever felt like your resume is being judged by a robot?  
    Well... it is. 🤖  
    But hey, at least this one gives feedback instead of rejection emails! 📬
    """)
    st.header("🎯 Quick Stats")

    if uploaded_file:
        st.metric("File Size", f"{uploaded_file.size / 1024:.1f} KB")
        st.metric("Format", uploaded_file.name.split('.')[-1].upper())

    st.info("""
    This tool helps you:
    - ✅ Check ATS compatibility
    - 🎯 Match with job descriptions
    - 💡 Get improvement suggestions
    - 📊 Extract key information
    - 🤖 Predict suitable job roles
    """)

    st.header("Supported Formats")
    st.write("📄 TXT")
    st.write("📄 PDF")
    st.write("📄 DOCX")

# Job description input
st.header("📋 Job Description (Optional)")
job_description = st.text_area(
    "Paste the job description here",
    height=200,
    placeholder="Enter job description to match your resume..."
)

# Analysis Section
st.markdown("---")
st.header("📊 Analysis Results")

if uploaded_file is not None:
    try:
        # Extract text
        with st.spinner(f"Extracting text from {uploaded_file.name}..."):
            resume_text = parser.extract_text_from_uploaded_file(uploaded_file)

        if resume_text:
            # Parse resume
            with st.spinner("Analyzing resume..."):
                parsed_data = parser.parse_resume(resume_text)

            # ATS Score
            ats_result = scorer.calculate_ats_score(resume_text, job_description)
            score = ats_result['score']

            # Display ATS Score
            st.subheader("🎯 ATS Compatibility Score")
            color = "green" if score >= 75 else "orange" if score >= 50 else "red"
            st.markdown(f"<h1 style='color:{color};'>{score}/100</h1>", unsafe_allow_html=True)
            st.markdown(f"**Rating:** {ats_result['rating']}")

            # Job Match
            if job_description:
                job_match = scorer.calculate_job_match(resume_text, job_description)
                st.metric("Job Match", f"{job_match}%")

                missing_keywords = scorer.find_missing_keywords(resume_text, job_description)
                if missing_keywords:
                    st.warning(f"**Missing Keywords:** {', '.join(missing_keywords[:8])}")

            # Feedback
            st.subheader("💡 Suggestions")
            for feedback in ats_result['feedback']:
                if '❌' in feedback:
                    st.error(feedback)
                elif '⚠️' in feedback:
                    st.warning(feedback)
                else:
                    st.success(feedback)

            # Extracted Information
            st.subheader("📝 Extracted Information")

            with st.expander("👤 Contact Information"):
                st.json(parsed_data['contact_info'])

            if parsed_data.get('education'):
                with st.expander("🎓 Education"):
                    for edu in parsed_data['education']:
                        st.write(f"**{edu['degree']}** ({edu['year']})")
                        if edu.get('institution') != 'N/A':
                            st.write(f"📍 {edu['institution']}")
                        st.divider()

            if parsed_data['experience']['details']:
                with st.expander("💼 Work Experience"):
                    st.metric("Total Experience", f"{parsed_data['experience']['total_years']} years")
                    for exp in parsed_data['experience']['details'][:5]:
                        st.write(f"**{exp['title']}**")
                        if exp.get('company') != 'N/A':
                            st.write(f"🏢 {exp['company']}")
                        if exp.get('duration') != 'N/A':
                            st.write(f"📅 {exp['duration']}")
                        st.divider()

            with st.expander("💻 Skills"):
                if parsed_data['skills']['technical']:
                    st.write("**Technical Skills:**")
                    st.write(", ".join(parsed_data['skills']['technical']))

                if parsed_data['skills']['soft']:
                    st.write("\n**Soft Skills:**")
                    st.write(", ".join(parsed_data['skills']['soft']))

                st.metric("Total Skills Found", parsed_data['skills']['total_count'])

            # Job Role Prediction
            with st.expander("🎯 Predicted Job Roles"):
                with st.spinner("Predicting suitable roles..."):
                    prediction = predictor.predict(resume_text)
                st.success(f"**Best Match:** {prediction['predicted_role']}")
                st.metric("Confidence", f"{prediction['confidence']:.1f}%")
                st.write("**Other Suitable Roles:**")
                for role, conf in prediction['top_3_roles'][1:]:
                    st.write(f"- {role}: {conf:.1f}%")

            # Detailed Improvement Plan
            with st.expander("🔧 Detailed Improvement Plan"):
                suggestions = improver.analyze_and_suggest(parsed_data, resume_text)

                if suggestions['critical']:
                    st.error("🚨 **CRITICAL ISSUES** (Fix Immediately)")
                    for sug in suggestions['critical']:
                        st.write(f"**{sug['issue']}**")
                        st.write(f"→ {sug['suggestion']}")
                        st.info(f"Example: {sug['example']}")
                        st.divider()

                if suggestions['important']:
                    st.warning("⚠️ **IMPORTANT** (High Priority)")
                    for sug in suggestions['important']:
                        st.write(f"**{sug['issue']}**")
                        st.write(f"→ {sug['suggestion']}")
                        st.info(f"Example: {sug['example']}")
                        st.divider()

                if suggestions['nice_to_have']:
                    st.info("💡 **NICE TO HAVE** (When Time Permits)")
                    for sug in suggestions['nice_to_have']:
                        st.write(f"**{sug['issue']}**")
                        st.write(f"→ {sug['suggestion']}")
                        st.caption(f"Example: {sug['example']}")
                        st.divider()

                # Download improvement plan
                improvement_plan = improver.generate_improvement_plan(suggestions)
                st.download_button(
                    label="📥 Download Improvement Plan",
                    data=improvement_plan,
                    file_name="resume_improvement_plan.txt",
                    mime="text/plain"
                )

            # Export Section
            st.subheader("📥 Export Results")
            col_json, col_txt = st.columns(2)

            with col_json:
                st.download_button(
                    label="Download JSON",
                    data=json.dumps(parsed_data, indent=2),
                    file_name="resume_analysis.json",
                    mime="application/json"
                )

            with col_txt:
                report = f"""
RESUME ANALYSIS REPORT
{'=' * 50}

ATS Score: {score}/100
Rating: {ats_result['rating']}

Contact Information:
- Name: {parsed_data['contact_info']['name']}
- Email: {parsed_data['contact_info']['email']}
- Phone: {parsed_data['contact_info']['phone']}

Skills Found: {parsed_data['skills']['total_count']}
Technical: {', '.join(parsed_data['skills']['technical'][:10])}
Soft: {', '.join(parsed_data['skills']['soft'])}

Predicted Role: {prediction['predicted_role']}
Confidence: {prediction['confidence']:.1f}%

Total Experience: {parsed_data['experience']['total_years']} years
"""
                st.download_button(
                    label="Download Report",
                    data=report,
                    file_name="resume_report.txt",
                    mime="text/plain"
                )

        else:
            st.error("❌ Could not extract text from the file. Please check the format.")

    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.info("Please make sure the file is not corrupted and is in a supported format.")

else:
    st.info("👆 Upload a resume to get started!")
    st.markdown("""
    ### How to use:
    1. Upload your resume (PDF, DOCX, or TXT)
    2. Optionally paste a job description
    3. Get instant analysis and suggestions
    4. Download your analysis report
    """)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for Project Expo | AI-Powered Resume Analysis")
st.caption("Supports PDF, DOCX, and TXT formats | Powered by spaCy, scikit-learn & Streamlit")
