import streamlit as st

st.set_page_config(page_title="Help & FAQ", page_icon="❓", layout="wide")

st.title("❓ Help & Frequently Asked Questions")

# Search functionality
search = st.text_input("🔍 Search for help", placeholder="Type your question...")

# FAQ Data
faqs = {
    "Getting Started": [
        {
            "q": "How do I upload my resume?",
            "a": "Go to the main page and click the 'Choose a file' button. Select your resume in PDF, DOCX, or TXT format."
        },
        {
            "q": "What file formats are supported?",
            "a": "We support PDF, DOCX (Microsoft Word), and TXT (plain text) files. Make sure your PDF is text-based, not image-based."
        },
        {
            "q": "Is my data safe?",
            "a": "Yes! All processing happens locally on your machine. We don't upload your resume to any external servers or store your data."
        }
    ],
    "ATS Scores": [
        {
            "q": "What is an ATS score?",
            "a": "ATS (Applicant Tracking System) score measures how well your resume will perform with automated screening systems used by 75% of companies. Score ranges from 0-100."
        },
        {
            "q": "What's a good ATS score?",
            "a": "- 90-100: Excellent\n- 75-89: Good\n- 60-74: Average\n- Below 60: Needs improvement"
        },
        {
            "q": "How is the ATS score calculated?",
            "a": "The score is based on: Contact info (20%), Section structure (20%), Formatting (15%), Content length (10%), Achievements (15%), and Job match (20%)."
        },
        {
            "q": "Why is my score low?",
            "a": "Common reasons: missing contact information, poor formatting, lack of quantifiable achievements, missing keywords, or inconsistent structure."
        }
    ],
    "Features": [
        {
            "q": "What is job matching?",
            "a": "Job matching calculates how similar your resume is to a job description using AI. It identifies missing keywords and gives you a match percentage."
        },
        {
            "q": "How does job role prediction work?",
            "a": "Our ML model analyzes your skills and experience to predict the top 3 most suitable job roles for you with confidence scores."
        },
        {
            "q": "Can I compare multiple resumes?",
            "a": "Yes! Go to the 'Compare Resumes' page, upload 2+ resumes, and see side-by-side rankings with visualizations."
        },
        {
            "q": "How do I track my progress?",
            "a": "Use the 'Analytics Dashboard' to save different versions of your resume and track improvements over time."
        }
    ],
    "Troubleshooting": [
        {
            "q": "My PDF won't upload",
            "a": "Ensure: 1) File size is under 10MB, 2) PDF is text-based (not scanned image), 3) File is not password-protected."
        },
        {
            "q": "The extracted text looks wrong",
            "a": "This can happen with complex formatting or image-based PDFs. Try: 1) Saving as plain text, 2) Simplifying formatting, 3) Using DOCX instead."
        },
        {
            "q": "Skills are not being detected",
            "a": "Make sure skills are clearly listed in a 'Skills' section and use standard technology names (e.g., 'Python' not 'Py')."
        },
        {
            "q": "App is slow or freezing",
            "a": "Try: 1) Refresh the page, 2) Use smaller files, 3) Close other tabs, 4) Clear browser cache."
        }
    ],
    "Best Practices": [
        {
            "q": "How often should I update my resume?",
            "a": "Update every 3-6 months or after significant achievements. Use our tracker to monitor improvements."
        },
        {
            "q": "Should I customize my resume for each job?",
            "a": "Yes! Use the job matching feature to identify missing keywords and tailor your resume accordingly."
        },
        {
            "q": "What's the ideal resume length?",
            "a": "1 page for freshers/students, 1-2 pages for 3-5 years experience, 2 pages for 5+ years. Keep it concise!"
        },
        {
            "q": "How many skills should I list?",
            "a": "Aim for 10-15 relevant skills. Too few (under 5) looks inexperienced, too many (over 20) looks unfocused."
        }
    ]
}

# Display FAQs
for category, questions in faqs.items():
    
    # Filter by search
    if search:
        questions = [q for q in questions if search.lower() in q['q'].lower() or search.lower() in q['a'].lower()]
    
    if questions:  # Only show category if it has matching questions
        st.subheader(f"📌 {category}")
        
        for faq in questions:
            with st.expander(faq['q']):
                st.markdown(faq['a'])
        
        st.divider()

# Quick Links
st.subheader("🔗 Quick Links")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **📚 Learn More**
    - [Resume Tips](#)
    - [Template Generator](#)
    - [Best Practices](#)
    """)

with col2:
    st.markdown("""
    **🛠️ Tools**
    - [ATS Analyzer](#)
    - [Batch Processing](#)
    - [Comparison Tool](#)
    """)

with col3:
    st.markdown("""
    **📊 Analytics**
    - [Progress Tracker](#)
    - [Advanced Analytics](#)
    - [Settings](#)
    """)

# Video Tutorials Section
st.divider()
st.subheader("🎥 Video Tutorials")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Getting Started (2 min)**
    - How to upload your resume
    - Understanding your ATS score
    - Basic tips for improvement
    
    [▶️ Watch Tutorial](#)
    """)

with col2:
    st.markdown("""
    **Advanced Features (3 min)**
    - Job matching explained
    - Comparing multiple resumes
    - Tracking your progress
    
    [▶️ Watch Tutorial](#)
    """)

# Contact Support
st.divider()
st.subheader("📞 Need More Help?")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    If you can't find an answer to your question:
    
    1. **Check our documentation** - Comprehensive guides available
    2. **Search above** - Use the search box to find specific topics
    3. **Contact us** - Reach out for personalized support
    
    **Email:** support@resumeanalyzer.com  
    **Response Time:** Within 24 hours
    """)

with col2:
    with st.form("support_form"):
        st.markdown("**Quick Support**")
        name = st.text_input("Name")
        email = st.text_input("Email")
        issue = st.text_area("Describe your issue")
        
        if st.form_submit_button("Send"):
            st.success("✅ Message sent! We'll respond within 24 hours.")

# Tips
st.divider()
st.info("""
💡 **Pro Tip**: Bookmark this page for quick reference while improving your resume!
""")
