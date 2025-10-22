import streamlit as st

st.set_page_config(page_title="Resume Tips", page_icon="💡", layout="wide")

st.title("💡 Resume Writing Tips & Best Practices")

tab1, tab2, tab3, tab4 = st.tabs(["📝 Writing Tips", "🎨 Formatting", "🔑 Keywords", "❌ Common Mistakes"])

with tab1:
    st.header("Resume Writing Best Practices")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ DO's")
        st.markdown("""
        - **Use action verbs**: Start bullet points with strong verbs like "Developed", "Implemented", "Led"
        - **Quantify achievements**: Include numbers, percentages, and metrics
        - **Tailor for each job**: Customize resume for the specific role
        - **Keep it concise**: Aim for 1 page (freshers) or 2 pages (experienced)
        - **Use bullet points**: Makes it easy to scan
        - **Include relevant keywords**: Match job description terminology
        - **Highlight impact**: Show results, not just responsibilities
        - **Proofread carefully**: Zero typos or grammatical errors
        """)
    
    with col2:
        st.subheader("❌ DON'Ts")
        st.markdown("""
        - **Avoid personal pronouns**: Don't use "I", "me", "my"
        - **No lies or exaggerations**: Be honest about skills and experience
        - **Skip irrelevant info**: Focus on job-related content
        - **No generic objectives**: Use a targeted summary instead
        - **Avoid walls of text**: Use white space effectively
        - **Don't use photos**: Unless specifically requested
        - **No unprofessional email**: Use firstname.lastname@email.com format
        - **Skip salary information**: Discuss in interview
        """)
    
    st.divider()
    
    st.subheader("🎯 Resume Structure")
    st.markdown("""
    ### Ideal Resume Structure:
    
    1. **Header** (Name, Contact Info, Links)
       - Full Name
       - Phone Number
       - Professional Email
       - LinkedIn Profile
       - GitHub/Portfolio (for tech roles)
    
    2. **Professional Summary** (2-3 lines)
       - Brief overview of experience and expertise
       - Key skills and strengths
       - Career goals aligned with target role
    
    3. **Technical Skills**
       - Programming languages
       - Frameworks and tools
       - Databases and platforms
       - Soft skills
    
    4. **Work Experience** (Reverse chronological)
       - Job Title | Company Name | Duration
       - 3-5 bullet points per role
       - Focus on achievements and impact
    
    5. **Education**
       - Degree | University | Year
       - Relevant coursework (optional)
       - GPA if >3.5/4.0
    
    6. **Projects** (Especially for freshers)
       - Project name and brief description
       - Technologies used
       - Your role and contributions
       - Results or outcomes
    
    7. **Certifications & Achievements** (Optional)
       - Relevant certifications
       - Awards and recognitions
       - Publications or presentations
    """)

with tab2:
    st.header("Formatting Guidelines")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Layout")
        st.markdown("""
        **Font:**
        - Use professional fonts: Arial, Calibri, Times New Roman
        - Font size: 10-12pt for body, 14-16pt for headings
        - Consistent font throughout
        
        **Spacing:**
        - 1-inch margins on all sides
        - Adequate white space between sections
        - 1.15 line spacing
        
        **Colors:**
        - Stick to black/dark gray text
        - Can use one accent color for headers
        - Ensure high contrast for readability
        """)
    
    with col2:
        st.subheader("📐 Structure")
        st.markdown("""
        **Headers:**
        - Use clear section headers
        - Bold or slightly larger font
        - Consistent formatting
        
        **Bullet Points:**
        - Use standard bullets (•)
        - Align consistently
        - 3-5 bullets per section
        
        **Length:**
        - Freshers: 1 page
        - 3-5 years exp: 1-2 pages
        - 5+ years exp: 2 pages max
        """)
    
    st.divider()
    
    st.subheader("✅ ATS-Friendly Formatting")
    st.info("""
    **ATS (Applicant Tracking System) Tips:**
    - Use standard section headings
    - Avoid tables, text boxes, headers/footers
    - Save as PDF (unless doc/docx requested)
    - Don't use images or graphics
    - Stick to simple formatting
    - Use standard bullet points
    """)

with tab3:
    st.header("Keywords & ATS Optimization")
    
    st.subheader("🔍 Understanding Keywords")
    st.markdown("""
    Keywords are specific terms that ATS systems look for in your resume.
    They're usually found in the job description.
    
    ### Types of Keywords:
    
    **1. Hard Skills:**
    - Programming languages (Python, Java, JavaScript)
    - Tools and technologies (React, Docker, AWS)
    - Specific methodologies (Agile, Scrum)
    
    **2. Soft Skills:**
    - Leadership
    - Communication
    - Problem-solving
    - Team collaboration
    
    **3. Certifications:**
    - AWS Certified
    - Google Cloud Professional
    - PMP Certification
    
    **4. Industry Terms:**
    - Machine Learning
    - Data Analysis
    - Full-Stack Development
    """)
    
    st.divider()
    
    st.subheader("💡 How to Use Keywords Effectively")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Step 1: Identify Keywords**
        - Read job description carefully
        - Highlight repeated terms
        - Note required vs preferred skills
        
        **Step 2: Natural Integration**
        - Don't just list keywords
        - Use them in context
        - Show how you used each skill
        """)
    
    with col2:
        st.markdown("""
        **Step 3: Strategic Placement**
        - Include in skills section
        - Mention in experience bullets
        - Add to project descriptions
        
        **Step 4: Avoid Keyword Stuffing**
        - Use naturally
        - Don't repeat excessively
        - Maintain readability
        """)
    
    st.info("💡 **Pro Tip:** Use both acronyms and full terms (e.g., 'ML' and 'Machine Learning')")

with tab4:
    st.header("Common Resume Mistakes to Avoid")
    
    mistakes = [
        {
            "title": "1. Typos and Grammatical Errors",
            "problem": "Nothing screams unprofessional louder than spelling mistakes",
            "solution": "Proofread multiple times, use spell-check, ask someone else to review"
        },
        {
            "title": "2. Using Generic Objective Statements",
            "problem": "'Seeking a challenging position' tells recruiters nothing",
            "solution": "Use a targeted summary highlighting your value proposition"
        },
        {
            "title": "3. Listing Responsibilities Instead of Achievements",
            "problem": "'Responsible for managing team' doesn't show impact",
            "solution": "'Led team of 5 to deliver project 2 weeks ahead of schedule'"
        },
        {
            "title": "4. Including Irrelevant Information",
            "problem": "High school achievements, unrelated hobbies waste space",
            "solution": "Focus on relevant experience, skills, and achievements"
        },
        {
            "title": "5. Using Unprofessional Email",
            "problem": "partyguy123@email.com won't get you the job",
            "solution": "Use firstname.lastname@email.com format"
        },
        {
            "title": "6. Poor Formatting",
            "problem": "Inconsistent fonts, spacing, and alignment look messy",
            "solution": "Use consistent formatting throughout, test on different devices"
        },
        {
            "title": "7. Lying or Exaggerating",
            "problem": "Claims can be verified and will backfire",
            "solution": "Be honest, focus on what you've genuinely accomplished"
        },
        {
            "title": "8. Too Long or Too Short",
            "problem": "5-page resumes won't be read, half-page ones lack detail",
            "solution": "Aim for 1 page (freshers) or 2 pages (experienced)"
        },
        {
            "title": "9. Missing Contact Information",
            "problem": "Can't contact you = can't interview you",
            "solution": "Include phone, email, LinkedIn at minimum"
        },
        {
            "title": "10. Not Tailoring for Each Job",
            "problem": "Generic resume doesn't match specific requirements",
            "solution": "Customize for each application, match job description keywords"
        }
    ]
    
    for mistake in mistakes:
        with st.expander(mistake["title"]):
            st.error(f"**Problem:** {mistake['problem']}")
            st.success(f"**Solution:** {mistake['solution']}")

st.divider()

st.header("🎓 Additional Resources")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📚 Learning")
    st.markdown("""
    - Resume writing courses
    - LinkedIn Learning
    - YouTube tutorials
    - Career counseling
    """)

with col2:
    st.subheader("🔧 Tools")
    st.markdown("""
    - Grammarly (grammar check)
    - Canva (design templates)
    - Google Docs (collaboration)
    - Our analyzer (ATS check!)
    """)

with col3:
    st.subheader("💼 Practice")
    st.markdown("""
    - Mock interviews
    - Resume reviews
    - Peer feedback
    - Career fairs
    """)