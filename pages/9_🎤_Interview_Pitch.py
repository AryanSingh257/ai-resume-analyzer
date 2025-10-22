import streamlit as st
from utils.resume_parser import ResumeParser
from utils.pitch_generator import InterviewPitchGenerator
import json

st.set_page_config(page_title="Interview Pitch Generator", page_icon="🎤", layout="wide")

st.title("🎤 Interview Pitch Generator")
st.markdown("Generate personalized answers to common interview questions based on your resume")

# Initialize
parser = ResumeParser()
pitch_gen = InterviewPitchGenerator()

# Sidebar for preferences
with st.sidebar:
    st.header("🎯 Personalization Options")
    st.markdown("Fill these to make pitches more tailored")
    
    target_role = st.text_input(
        "Target Job Role",
        placeholder="e.g., Software Developer, Data Scientist",
        help="The position you're applying for"
    )
    
    company_name = st.text_input(
        "Company Name (Optional)",
        placeholder="e.g., Google, Microsoft",
        help="Makes pitches company-specific"
    )
    
    company_values = st.text_input(
        "Company Values (comma-separated)",
        placeholder="e.g., Innovation, Collaboration, Excellence",
        help="Values mentioned in job description"
    )
    
    brand_keywords = st.text_input(
        "Your Brand Keywords",
        placeholder="e.g., Innovative, Reliable, Passionate",
        help="Words that describe your professional brand"
    )
    
    unique_points = st.text_area(
        "What Makes You Unique?",
        placeholder="e.g., Open source contributor\nMultilingual\nStartup experience",
        help="One unique point per line"
    )

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 Upload Your Resume")
    uploaded_file = st.file_uploader(
        "Upload resume",
        type=['pdf', 'docx', 'txt'],
        help="Upload your latest resume"
    )

with col2:
    st.header("❓ Select Questions")
    
    all_questions = pitch_gen.common_questions
    
    question_mode = st.radio(
        "Mode",
        ["Generate All", "Select Specific Questions", "Custom Question"]
    )

if uploaded_file:
    try:
        # Parse resume
        with st.spinner("Analyzing your resume..."):
            text = parser.extract_text_from_uploaded_file(uploaded_file)
            parsed_data = parser.parse_resume(text)
        
        st.success("✅ Resume analyzed successfully!")
        
        # Show quick stats
        with st.expander("📊 Quick Resume Stats"):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Skills", parsed_data['skills']['total_count'])
            with col2:
                st.metric("Experience", f"{parsed_data['experience']['total_years']} yrs")
            with col3:
                st.metric("Education", len(parsed_data.get('education', [])))
            with col4:
                st.metric("Jobs", len(parsed_data['experience']['details']))
        
        st.divider()
        
        # Prepare preferences
        preferences = {
            'target_role': target_role if target_role else None,
            'company_name': company_name if company_name else None,
            'company_values': [v.strip() for v in company_values.split(',')] if company_values else None,
            'brand_keywords': [k.strip() for k in brand_keywords.split(',')] if brand_keywords else None,
            'unique_points': [p.strip() for p in unique_points.split('\n') if p.strip()] if unique_points else None
        }
        
        # Generate pitches based on mode
        if question_mode == "Generate All":
            st.header("📝 Your Interview Pitches")
            st.markdown("Here are personalized answers to the most common interview questions:")
            
            if st.button("🎯 Generate All Pitches", type="primary"):
                with st.spinner("Crafting your pitches..."):
                    pitches = pitch_gen.generate_all_pitches(parsed_data, preferences)
                
                # Display each pitch
                for i, (question, answer) in enumerate(pitches.items(), 1):
                    with st.expander(f"Question {i}: {question}", expanded=i==1):
                        st.markdown(answer)
                        
                        # Copy to clipboard button
                        col1, col2 = st.columns([3, 1])
                        with col2:
                            if st.button(f"📋 Copy", key=f"copy_{i}"):
                                st.toast("✅ Copied to clipboard! (Use Ctrl+C to copy the text above)")
                        
                        # Tips
                        st.info(f"💡 **Tip**: Practice this answer out loud. Aim for 60-90 seconds delivery.")
                
                # Download all pitches
                st.divider()
                st.subheader("📥 Export Your Pitches")
                
                # Create downloadable content
                all_pitches_text = "INTERVIEW PITCH DOCUMENT\n"
                all_pitches_text += "=" * 60 + "\n\n"
                all_pitches_text += f"Generated for: {parsed_data['contact_info']['name']}\n"
                if target_role:
                    all_pitches_text += f"Target Role: {target_role}\n"
                if company_name:
                    all_pitches_text += f"Company: {company_name}\n"
                all_pitches_text += "\n" + "=" * 60 + "\n\n"
                
                for question, answer in pitches.items():
                    all_pitches_text += f"Q: {question}\n"
                    all_pitches_text += "-" * 60 + "\n"
                    all_pitches_text += f"{answer}\n\n"
                    all_pitches_text += "=" * 60 + "\n\n"
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.download_button(
                        label="📄 Download as Text",
                        data=all_pitches_text,
                        file_name="interview_pitches.txt",
                        mime="text/plain"
                    )
                
                with col2:
                    pitches_json = json.dumps(pitches, indent=2)
                    st.download_button(
                        label="📋 Download as JSON",
                        data=pitches_json,
                        file_name="interview_pitches.json",
                        mime="application/json"
                    )
        
        elif question_mode == "Select Specific Questions":
            st.header("❓ Select Questions to Answer")
            
            selected_questions = st.multiselect(
                "Choose questions",
                all_questions,
                default=all_questions[:3]
            )
            
            if selected_questions and st.button("Generate Selected Pitches", type="primary"):
                for question in selected_questions:
                    with st.expander(f"❓ {question}", expanded=True):
                        if "tell me about yourself" in question.lower():
                            pitch = pitch_gen.generate_tell_me_about_yourself(
                                parsed_data, target_role, company_name
                            )
                        elif "personal brand" in question.lower():
                            pitch = pitch_gen.generate_personal_brand(
                                parsed_data, preferences.get('brand_keywords')
                            )
                        elif "why should we hire" in question.lower():
                            pitch = pitch_gen.generate_why_hire_you(
                                parsed_data, target_role, preferences.get('company_values')
                            )
                        elif "strengths" in question.lower():
                            pitch = pitch_gen.generate_key_strengths(parsed_data)
                        elif "5 years" in question.lower() or "five years" in question.lower():
                            pitch = pitch_gen.generate_five_year_vision(parsed_data, target_role)
                        elif "unique" in question.lower():
                            pitch = pitch_gen.generate_what_makes_you_unique(
                                parsed_data, preferences.get('unique_points')
                            )
                        else:
                            pitch = pitch_gen.generate_custom_pitch(question, parsed_data)
                        
                        st.markdown(pitch)
        
        else:  # Custom Question
            st.header("💬 Ask Your Custom Question")
            
            custom_question = st.text_input(
                "Enter your interview question",
                placeholder="e.g., What is your approach to learning new technologies?"
            )
            
            additional_context = st.text_area(
                "Additional Context (Optional)",
                placeholder="Any specific points you want to include in the answer...",
                height=100
            )
            
            if custom_question and st.button("Generate Answer", type="primary"):
                with st.expander("Your Custom Pitch", expanded=True):
                    pitch = pitch_gen.generate_custom_pitch(
                        custom_question,
                        parsed_data,
                        additional_context
                    )
                    st.markdown(pitch)
        
        # Practice tips
        st.divider()
        st.subheader("🎯 Interview Pitch Tips")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **📝 Preparation**
            - Read pitch multiple times
            - Practice out loud
            - Time yourself (60-90 sec)
            - Record and listen
            """)
        
        with col2:
            st.markdown("""
            **🗣️ Delivery**
            - Make eye contact
            - Smile and be confident
            - Use natural pauses
            - Show enthusiasm
            """)
        
        with col3:
            st.markdown("""
            **✅ Customization**
            - Adapt to interviewer
            - Add recent examples
            - Be authentic
            - Ask for feedback
            """)
    
    except Exception as e:
        st.error(f"❌ Error processing resume: {str(e)}")

else:
    st.info("👆 Upload your resume to generate interview pitches")
    
    st.markdown("""
    ### How it works:
    
    1. **Upload Your Resume** - We'll analyze your skills, experience, and background
    2. **Add Preferences** (Optional) - Personalize pitches with target role, company info
    3. **Generate Pitches** - Get tailored answers to common interview questions
    4. **Practice & Refine** - Use these as starting points and make them your own
    
    ### Features:
    
    ✨ **Smart Analysis** - Extracts key information from your resume  
    🎯 **Personalized** - Tailored to your background and target role  
    📝 **Multiple Questions** - Covers 10+ common interview questions  
    💾 **Exportable** - Download for practice and reference  
    🚫 **No AI APIs** - Everything runs locally, your data stays private  
    
    ### Popular Questions Covered:
    
    - Tell me about yourself
    - What is your personal brand?
    - Why should we hire you?
    - What are your key strengths?
    - Where do you see yourself in 5 years?
    - What makes you unique?
    - And more!
    """)
    
    st.divider()
    
    st.warning("""
    **⚠️ Important Note:**  
    These pitches are starting points based on your resume data. 
    Always personalize them with:
    - Specific examples from your experience
    - Genuine enthusiasm and personality
    - Research about the company
    - Recent accomplishments
    """)