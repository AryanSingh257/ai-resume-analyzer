import streamlit as st
from utils.template_generator import ResumeTemplateGenerator

st.set_page_config(page_title="Template Generator", page_icon="📄", layout="wide")

st.title("📄 Resume Template Generator")
st.markdown("Generate professional resume templates customized for your target role")

generator = ResumeTemplateGenerator()

# Job role selection
col1, col2 = st.columns([2, 1])

with col1:
    job_role = st.selectbox(
        "Select Target Job Role",
        ["Software Developer", "Data Scientist", "Web Developer", 
         "DevOps Engineer", "Data Analyst", "ML Engineer"]
    )

with col2:
    template_format = st.radio("Format", ["Markdown", "HTML"])

st.divider()

# Generate template
if st.button("🎨 Generate Template", type="primary"):
    
    if template_format == "Markdown":
        template = generator.generate_markdown_template(job_role)
        
        st.subheader("📝 Your Resume Template")
        st.code(template, language="markdown")
        
        # Download button
        st.download_button(
            label="📥 Download Markdown Template",
            data=template,
            file_name=f"resume_template_{job_role.lower().replace(' ', '_')}.md",
            mime="text/markdown"
        )
        
        # Preview
        with st.expander("👁️ Preview"):
            st.markdown(template)
    
    else:  # HTML
        st.info("👇 Fill in your details to generate HTML template")
        
        with st.form("html_form"):
            name = st.text_input("Full Name", placeholder="John Doe")
            email = st.text_input("Email", placeholder="john.doe@email.com")
            phone = st.text_input("Phone", placeholder="+91-9876543210")
            linkedin = st.text_input("LinkedIn", placeholder="linkedin.com/in/johndoe")
            github = st.text_input("GitHub", placeholder="github.com/johndoe")
            
            summary = st.text_area(
                "Professional Summary",
                placeholder="Brief summary of your experience and expertise...",
                height=100
            )
            
            skills_input = st.text_input(
                "Skills (comma-separated)",
                placeholder="Python, Java, React, Node.js"
            )
            
            submitted = st.form_submit_button("Generate HTML Resume")
            
            if submitted:
                skills = [s.strip() for s in skills_input.split(',')]
                
                data = {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'linkedin': linkedin,
                    'github': github,
                    'summary': summary,
                    'skills': skills
                }
                
                html_template = generator.generate_html_template(data)
                
                st.success("✅ HTML Template Generated!")
                
                # Download button
                st.download_button(
                    label="📥 Download HTML Resume",
                    data=html_template,
                    file_name="resume.html",
                    mime="text/html"
                )
                
                # Preview in expander
                with st.expander("��️ Preview HTML Resume"):
                    st.components.v1.html(html_template, height=800, scrolling=True)

st.divider()

# Section-wise suggestions
st.subheader("💡 Section-wise Writing Tips")

suggestions = generator.get_section_suggestions(job_role)

cols = st.columns(2)
for i, (section, tips) in enumerate(suggestions.items()):
    with cols[i % 2]:
        with st.expander(f"📌 {section}"):
            for tip in tips:
                st.write(f"✓ {tip}")

# Additional resources
st.divider()
st.subheader("📚 Additional Resources")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Action Verbs**
    - Achieved
    - Developed
    - Implemented
    - Improved
    - Led
    - Optimized
    """)

with col2:
    st.markdown("""
    **Power Words**
    - Successfully
    - Efficiently
    - Strategically
    - Collaboratively
    - Proactively
    - Significantly
    """)

with col3:
    st.markdown("""
    **Metrics to Include**
    - Percentages (↑30%)
    - Time saved
    - Users impacted
    - Revenue generated
    - Team size
    - Project count
    """)
