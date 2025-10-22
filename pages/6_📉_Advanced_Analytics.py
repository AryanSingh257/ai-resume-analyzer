import streamlit as st
from utils.resume_parser import ResumeParser
from utils.ats_scorer import ATSScorer
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
import pandas as pd

st.set_page_config(page_title="Advanced Analytics", page_icon="📉", layout="wide")

st.title("📉 Advanced Resume Analytics")
st.markdown("Deep dive into resume patterns and trends")

# Initialize
parser = ResumeParser()
scorer = ATSScorer()

# Upload multiple resumes for analytics
uploaded_files = st.file_uploader(
    "Upload Resumes for Analysis",
    type=['pdf', 'docx', 'txt'],
    accept_multiple_files=True,
    help="Upload at least 5 resumes for meaningful analytics"
)

if uploaded_files and len(uploaded_files) >= 3:
    
    if st.button("🔍 Analyze Patterns", type="primary"):
        with st.spinner("Analyzing resumes..."):
            
            all_skills = []
            all_scores = []
            all_experience = []
            all_education = []
            contact_completeness = []
            
            for file in uploaded_files:
                try:
                    text = parser.extract_text_from_uploaded_file(file)
                    if text:
                        parsed = parser.parse_resume(text)
                        ats_result = scorer.calculate_ats_score(text)
                        
                        # Collect data
                        all_skills.extend(parsed['skills']['technical'])
                        all_scores.append(ats_result['score'])
                        all_experience.append(parsed['experience']['total_years'])
                        all_education.append(len(parsed.get('education', [])))
                        
                        # Contact completeness
                        completeness = sum([
                            bool(parsed['contact_info']['email']),
                            bool(parsed['contact_info']['phone']),
                            bool(parsed['contact_info']['links']['linkedin']),
                            bool(parsed['contact_info']['links']['github'])
                        ]) * 25
                        contact_completeness.append(completeness)
                
                except Exception as e:
                    st.error(f"Error processing {file.name}: {str(e)}")
            
            # Display analytics
            st.success(f"✅ Analyzed {len(uploaded_files)} resumes")
            
            # Key Metrics
            st.subheader("📊 Key Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Avg ATS Score", f"{sum(all_scores)/len(all_scores):.1f}/100")
            
            with col2:
                st.metric("Avg Experience", f"{sum(all_experience)/len(all_experience):.1f} yrs")
            
            with col3:
                st.metric("Avg Skills", f"{len(all_skills)/len(uploaded_files):.1f}")
            
            with col4:
                st.metric("Avg Completeness", f"{sum(contact_completeness)/len(contact_completeness):.0f}%")
            
            # Charts
            st.divider()
            
            # Top Skills
            st.subheader("🔥 Most In-Demand Skills")
            
            skill_counts = Counter(all_skills)
            top_skills = skill_counts.most_common(15)
            
            if top_skills:
                skills_df = pd.DataFrame(top_skills, columns=['Skill', 'Count'])
                
                fig = px.bar(
                    skills_df,
                    x='Count',
                    y='Skill',
                    orientation='h',
                    title="Top 15 Skills Across All Resumes",
                    color='Count',
                    color_continuous_scale='Blues'
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
            
            # Score Distribution
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 ATS Score Distribution")
                
                fig2 = go.Figure()
                fig2.add_trace(go.Histogram(
                    x=all_scores,
                    nbinsx=10,
                    marker_color='lightblue',
                    name='ATS Scores'
                ))
                fig2.update_layout(
                    xaxis_title="ATS Score",
                    yaxis_title="Number of Resumes",
                    showlegend=False
                )
                st.plotly_chart(fig2, use_container_width=True)
            
            with col2:
                st.subheader("💼 Experience Distribution")
                
                fig3 = go.Figure()
                fig3.add_trace(go.Box(
                    y=all_experience,
                    name='Experience Years',
                    marker_color='lightgreen'
                ))
                fig3.update_layout(yaxis_title="Years of Experience")
                st.plotly_chart(fig3, use_container_width=True)
            
            # Contact Completeness
            st.subheader("📞 Profile Completeness Analysis")
            
            completeness_ranges = {
                '0-25%': sum(1 for c in contact_completeness if c <= 25),
                '26-50%': sum(1 for c in contact_completeness if 25 < c <= 50),
                '51-75%': sum(1 for c in contact_completeness if 50 < c <= 75),
                '76-100%': sum(1 for c in contact_completeness if c > 75)
            }
            
            fig4 = go.Figure(data=[
                go.Pie(
                    labels=list(completeness_ranges.keys()),
                    values=list(completeness_ranges.values()),
                    hole=.3
                )
            ])
            fig4.update_layout(title="Profile Completeness Distribution")
            st.plotly_chart(fig4, use_container_width=True)
            
            # Insights
            st.divider()
            st.subheader("💡 Key Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Strengths:**")
                avg_score = sum(all_scores)/len(all_scores)
                if avg_score >= 70:
                    st.success("✅ Good overall ATS scores")
                if len(set(all_skills)) > 20:
                    st.success(f"✅ Diverse skill set ({len(set(all_skills))} unique skills)")
                if sum(all_experience)/len(all_experience) >= 2:
                    st.success("✅ Experienced candidate pool")
            
            with col2:
                st.markdown("**Areas for Improvement:**")
                if avg_score < 70:
                    st.warning("⚠️ ATS scores need improvement")
                if sum(contact_completeness)/len(contact_completeness) < 75:
                    st.warning("⚠️ Incomplete contact information")
                if len(set(all_skills)) < 15:
                    st.warning("⚠️ Limited skill diversity")
            
            # Recommendations
            st.divider()
            st.subheader("🎯 Recommendations")
            
            st.markdown(f"""
            Based on analysis of {len(uploaded_files)} resumes:
            
            1. **Most Common Skills**: {', '.join([s[0] for s in top_skills[:5]])}
            2. **Target ATS Score**: Aim for 75+ (current avg: {avg_score:.1f})
            3. **Profile Completeness**: Ensure all contact details are present
            4. **Skills Gap**: Consider adding trending skills to stand out
            """)
            
            # Export
            st.divider()
            
            analytics_data = {
                'total_resumes': len(uploaded_files),
                'avg_ats_score': sum(all_scores)/len(all_scores),
                'avg_experience': sum(all_experience)/len(all_experience),
                'top_skills': dict(top_skills[:10]),
                'avg_completeness': sum(contact_completeness)/len(contact_completeness)
            }
            
            import json
            st.download_button(
                label="📥 Download Analytics Report",
                data=json.dumps(analytics_data, indent=2),
                file_name="analytics_report.json",
                mime="application/json"
            )

else:
    st.info("👆 Upload at least 3 resumes to see advanced analytics")
    
    st.markdown("""
    ### Features:
    
    📊 **Pattern Recognition**
    - Identify most in-demand skills
    - Analyze score distributions
    - Track experience trends
    
    📈 **Visual Insights**
    - Interactive charts and graphs
    - Statistical summaries
    - Comparative analysis
    
    💡 **Recommendations**
    - Data-driven suggestions
    - Industry benchmarks
    - Improvement areas
    
    ### Use Cases:
    - **Recruiters**: Understand candidate pool
    - **Job Seekers**: Benchmark against others
    - **Career Counselors**: Identify trends
    - **Companies**: Analyze applicant quality
    """)

