import streamlit as st
from utils.resume_parser import ResumeParser
from utils.ats_scorer import ATSScorer
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import os

st.set_page_config(page_title="Analytics Dashboard", page_icon="📈", layout="wide")

st.title("📈 Resume Analytics Dashboard")
st.markdown("Track your resume improvement over time")

# Initialize
parser = ResumeParser()
scorer = ATSScorer()

# Create analytics directory if it doesn't exist
if not os.path.exists('analytics_data'):
    os.makedirs('analytics_data')

# Load saved analyses
def load_history():
    history_file = 'analytics_data/history.json'
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            return json.load(f)
    return []

def save_analysis(data):
    history = load_history()
    history.append(data)
    with open('analytics_data/history.json', 'w') as f:
        json.dump(history, f, indent=2)

# Sidebar - Upload new resume
with st.sidebar:
    st.header("Add New Analysis")
    uploaded_file = st.file_uploader("Upload Resume", type=['txt', 'pdf', 'docx'])
    version_name = st.text_input("Version Name", placeholder="e.g., Version 1, After Review")
    
    if uploaded_file and version_name and st.button("Analyze & Save"):
        with st.spinner("Processing..."):
            try:
                text = parser.extract_text_from_uploaded_file(uploaded_file)
                parsed = parser.parse_resume(text)
                ats_result = scorer.calculate_ats_score(text)
                
                analysis_data = {
                    'timestamp': datetime.now().isoformat(),
                    'version_name': version_name,
                    'filename': uploaded_file.name,
                    'ats_score': ats_result['score'],
                    'skills_count': parsed['skills']['total_count'],
                    'experience_years': parsed['experience']['total_years'],
                    'has_email': bool(parsed['contact_info']['email']),
                    'has_phone': bool(parsed['contact_info']['phone']),
                    'has_linkedin': bool(parsed['contact_info']['links']['linkedin']),
                    'has_github': bool(parsed['contact_info']['links']['github']),
                    'education_count': len(parsed.get('education', [])),
                    'experience_count': len(parsed['experience']['details'])
                }
                
                save_analysis(analysis_data)
                st.success(f"✅ Analysis saved: {version_name}")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Main dashboard
history = load_history()

if history:
    st.subheader("📊 Your Progress Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    latest = history[-1]
    
    with col1:
        st.metric(
            "Latest ATS Score",
            f"{latest['ats_score']}/100",
            delta=f"{latest['ats_score'] - history[0]['ats_score']}" if len(history) > 1 else None
        )
    
    with col2:
        st.metric(
            "Skills Count",
            latest['skills_count'],
            delta=f"{latest['skills_count'] - history[0]['skills_count']}" if len(history) > 1 else None
        )
    
    with col3:
        st.metric(
            "Experience",
            f"{latest['experience_years']} years",
            delta=f"{latest['experience_years'] - history[0]['experience_years']}" if len(history) > 1 else None
        )
    
    with col4:
        completeness = sum([
            latest['has_email'],
            latest['has_phone'],
            latest['has_linkedin'],
            latest['has_github']
        ]) * 25
        st.metric("Profile Completeness", f"{completeness}%")
    
    # Progress over time
    st.subheader("📈 ATS Score Progress")
    
    # Prepare data for chart
    dates = [datetime.fromisoformat(h['timestamp']).strftime('%Y-%m-%d %H:%M') for h in history]
    scores = [h['ats_score'] for h in history]
    versions = [h['version_name'] for h in history]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=scores,
        mode='lines+markers',
        name='ATS Score',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=10),
        text=versions,
        hovertemplate='<b>%{text}</b><br>Score: %{y}<br>Date: %{x}<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="ATS Score",
        yaxis=dict(range=[0, 100]),
        height=400,
        hovermode='closest'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Skills progress
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💼 Skills Growth")
        skills_data = [h['skills_count'] for h in history]
        fig2 = go.Figure(data=[
            go.Bar(x=versions, y=skills_data, marker_color='lightblue')
        ])
        fig2.update_layout(xaxis_title="Version", yaxis_title="Skills Count", height=300)
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Profile Completeness")
        completeness_data = [
            sum([h['has_email'], h['has_phone'], h['has_linkedin'], h['has_github']]) * 25
            for h in history
        ]
        fig3 = go.Figure(data=[
            go.Bar(x=versions, y=completeness_data, marker_color='lightgreen')
        ])
        fig3.update_layout(xaxis_title="Version", yaxis_title="Completeness %", height=300)
        st.plotly_chart(fig3, use_container_width=True)
    
    # Detailed comparison table
    st.subheader("📋 Version Comparison")
    
    import pandas as pd
    df = pd.DataFrame(history)
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
    
    display_df = df[[
        'version_name', 'timestamp', 'ats_score', 'skills_count',
        'experience_years', 'education_count', 'experience_count'
    ]].rename(columns={
        'version_name': 'Version',
        'timestamp': 'Date',
        'ats_score': 'ATS Score',
        'skills_count': 'Skills',
        'experience_years': 'Experience (Years)',
        'education_count': 'Education',
        'experience_count': 'Jobs'
    })
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Insights
    st.subheader("💡 Insights & Recommendations")
    
    if len(history) > 1:
        score_improvement = latest['ats_score'] - history[0]['ats_score']
        skills_improvement = latest['skills_count'] - history[0]['skills_count']
        
        if score_improvement > 0:
            st.success(f"🎉 Great job! Your ATS score improved by {score_improvement} points!")
        elif score_improvement < 0:
            st.warning(f"⚠️ Your ATS score decreased by {abs(score_improvement)} points. Review recent changes.")
        else:
            st.info("📊 Your ATS score remained stable.")
        
        if skills_improvement > 0:
            st.success(f"✨ You added {skills_improvement} new skills!")
        
        # Recommendations
        st.markdown("**Next Steps:**")
        if latest['ats_score'] < 75:
            st.write("- Focus on improving your ATS score to 75+")
        if not latest['has_linkedin']:
            st.write("- Add your LinkedIn profile")
        if not latest['has_github']:
            st.write("- Add your GitHub profile (important for tech roles)")
        if latest['skills_count'] < 10:
            st.write("- Add more relevant skills (aim for 10-15)")
    
    # Export data
    st.subheader("📥 Export Data")
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="Download History (JSON)",
            data=json.dumps(history, indent=2),
            file_name="resume_history.json",
            mime="application/json"
        )
    
    with col2:
        if st.button("🗑️ Clear History", type="secondary"):
            if os.path.exists('analytics_data/history.json'):
                os.remove('analytics_data/history.json')
                st.success("History cleared!")
                st.rerun()

else:
    st.info("👆 Upload your first resume to start tracking your progress!")
    st.markdown("""
    ### How it works:
    1. Upload your resume in the sidebar
    2. Give it a version name (e.g., "Version 1", "After Interview Prep")
    3. Click "Analyze & Save"
    4. Track your improvements over time!
    
    ### Benefits:
    - 📊 Visualize your progress
    - 🎯 Track ATS score improvements
    - 💡 Get actionable insights
    - 📈 Compare different versions
    """)
    