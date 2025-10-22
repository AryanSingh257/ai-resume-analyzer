import streamlit as st
from utils.resume_parser import ResumeParser
from utils.ats_scorer import ATSScorer
from utils.batch_processor import BatchProcessor
import pandas as pd
import zipfile
import os
from io import BytesIO

st.set_page_config(page_title="Batch Processing", page_icon="⚡", layout="wide")

st.title("⚡ Batch Resume Processing")
st.markdown("Upload multiple resumes at once and get comprehensive analysis")

# Initialize
parser = ResumeParser()
scorer = ATSScorer()
batch_processor = BatchProcessor(parser, scorer)

# File uploader
uploaded_files = st.file_uploader(
    "Upload Multiple Resumes",
    type=['pdf', 'docx', 'txt'],
    accept_multiple_files=True,
    help="You can upload up to 20 resumes at once"
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} files uploaded")
    
    if len(uploaded_files) > 20:
        st.error("⚠️ Maximum 20 files allowed. Please reduce the number of files.")
    else:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            process_btn = st.button("🚀 Process All Resumes", type="primary")
        
        if process_btn:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = []
            
            for i, file in enumerate(uploaded_files):
                status_text.text(f"Processing {file.name}...")
                
                try:
                    # Extract text
                    text = parser.extract_text_from_uploaded_file(file)
                    
                    if text:
                        # Parse
                        parsed = parser.parse_resume(text)
                        
                        # Score
                        ats_result = scorer.calculate_ats_score(text)
                        
                        results.append({
                            'filename': file.name,
                            'success': True,
                            'ats_score': ats_result['score'],
                            'rating': ats_result['rating'],
                            'skills_count': parsed['skills']['total_count'],
                            'experience_years': parsed['experience']['total_years'],
                            'has_email': '✅' if parsed['contact_info']['email'] else '❌',
                            'has_phone': '✅' if parsed['contact_info']['phone'] else '❌',
                            'has_linkedin': '✅' if parsed['contact_info']['links']['linkedin'] else '❌'
                        })
                    else:
                        results.append({
                            'filename': file.name,
                            'success': False,
                            'error': 'Could not extract text'
                        })
                
                except Exception as e:
                    results.append({
                        'filename': file.name,
                        'success': False,
                        'error': str(e)
                    })
                
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            status_text.text("✅ Processing complete!")
            
            # Separate successful and failed
            successful = [r for r in results if r.get('success', False)]
            failed = [r for r in results if not r.get('success', False)]
            
            # Display results
            st.divider()
            st.subheader("📊 Batch Processing Results")
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Processed", len(results))
            
            with col2:
                st.metric("Successful", len(successful))
            
            with col3:
                st.metric("Failed", len(failed))
            
            with col4:
                if successful:
                    avg_score = sum(r['ats_score'] for r in successful) / len(successful)
                    st.metric("Avg ATS Score", f"{avg_score:.1f}")
            
            # Results table
            if successful:
                st.subheader("✅ Successfully Processed Resumes")
                
                df = pd.DataFrame(successful)
                df = df.sort_values('ats_score', ascending=False)
                df.index = range(1, len(df) + 1)
                
                st.dataframe(
                    df[[
                        'filename', 'ats_score', 'rating', 'skills_count',
                        'experience_years', 'has_email', 'has_phone', 'has_linkedin'
                    ]],
                    column_config={
                        "filename": "Resume Name",
                        "ats_score": st.column_config.ProgressColumn(
                            "ATS Score",
                            format="%d",
                            min_value=0,
                            max_value=100,
                        ),
                        "rating": "Rating",
                        "skills_count": "Skills",
                        "experience_years": "Experience (Yrs)",
                        "has_email": "Email",
                        "has_phone": "Phone",
                        "has_linkedin": "LinkedIn"
                    },
                    use_container_width=True
                )
                
                # Visualizations
                st.subheader("�� Visual Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    import plotly.express as px
                    
                    fig = px.histogram(
                        df, x='ats_score',
                        nbins=10,
                        title="ATS Score Distribution",
                        labels={'ats_score': 'ATS Score', 'count': 'Number of Resumes'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig2 = px.scatter(
                        df, x='skills_count', y='ats_score',
                        hover_data=['filename'],
                        title="Skills vs ATS Score",
                        labels={'skills_count': 'Skills Count', 'ats_score': 'ATS Score'}
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                
                # Export options
                st.subheader("�� Export Results")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # CSV export
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV Report",
                        data=csv,
                        file_name="batch_analysis_results.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    # JSON export
                    import json
                    json_data = json.dumps(successful, indent=2)
                    st.download_button(
                        label="Download JSON Report",
                        data=json_data,
                        file_name="batch_analysis_results.json",
                        mime="application/json"
                    )
            
            # Failed resumes
            if failed:
                st.subheader("❌ Failed to Process")
                failed_df = pd.DataFrame(failed)
                st.dataframe(failed_df, use_container_width=True)

else:
    st.info("👆 Upload multiple resumes to get started")
    
    st.markdown("""
    ### How to use:
    1. **Upload** 2-20 resumes (PDF, DOCX, or TXT)
    2. **Click** "Process All Resumes"
    3. **View** comprehensive analysis and rankings
    4. **Export** results as CSV or JSON
    
    ### Benefits:
    - ⚡ Process multiple resumes simultaneously
    - 📊 Compare all candidates at once
    - 📈 Visual analytics and insights
    - 📥 Export for further analysis
    - 🎯 Identify top performers quickly
    """)
