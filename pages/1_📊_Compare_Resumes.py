import streamlit as st
from utils.resume_parser import ResumeParser
from utils.resume_comparator import ResumeComparator
import pandas as pd

st.set_page_config(page_title="Compare Resumes", page_icon="📊", layout="wide")

st.title("📊 Compare Multiple Resumes")
st.markdown("Upload multiple resumes to compare and rank them")

# Initialize
parser = ResumeParser()
comparator = ResumeComparator()

# File uploader for multiple files
uploaded_files = st.file_uploader(
    "Upload resumes to compare",
    type=['txt', 'pdf', 'docx'],
    accept_multiple_files=True
)

if uploaded_files and len(uploaded_files) > 1:
    st.success(f"✅ {len(uploaded_files)} resumes uploaded")
    
    if st.button("🔍 Compare Resumes", type="primary"):
        with st.spinner("Analyzing all resumes..."):
            resumes_data = []
            
            # Process each resume
            for file in uploaded_files:
                try:
                    text = parser.extract_text_from_uploaded_file(file)
                    parsed = parser.parse_resume(text)
                    
                    resumes_data.append({
                        'name': file.name,
                        'text': text,
                        'parsed_data': parsed
                    })
                except Exception as e:
                    st.error(f"Error processing {file.name}: {str(e)}")
            
            # Compare resumes
            if len(resumes_data) > 1:
                comparisons = comparator.compare_resumes(resumes_data)
                
                st.subheader("🏆 Rankings")
                
                # Create DataFrame for display
                df = pd.DataFrame(comparisons)
                df.index = df.index + 1  # Start index from 1
                
                # Display as table
                st.dataframe(
                    df,
                    column_config={
                        "name": "Resume Name",
                        "score": st.column_config.ProgressColumn(
                            "Overall Score",
                            format="%d",
                            min_value=0,
                            max_value=100,
                        ),
                        "skills": "Skills Count",
                        "experience": "Experience (Years)",
                        "education": "Education Count",
                        "completeness": st.column_config.ProgressColumn(
                            "Profile Completeness",
                            format="%d%%",
                            min_value=0,
                            max_value=100,
                        ),
                    },
                    hide_index=False,
                    use_container_width=True
                )
                
                # Visualizations
                st.subheader("📊 Visual Comparison")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Score comparison chart
                    import plotly.graph_objects as go
                    
                    fig = go.Figure(data=[
                        go.Bar(
                            x=[c['name'] for c in comparisons],
                            y=[c['score'] for c in comparisons],
                            marker_color=['gold', 'silver', '#CD7F32'] + ['lightblue'] * (len(comparisons) - 3)
                        )
                    ])
                    fig.update_layout(
                        title="Overall Score Comparison",
                        xaxis_title="Resume",
                        yaxis_title="Score",
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Skills vs Experience scatter
                    fig2 = go.Figure(data=[
                        go.Scatter(
                            x=[c['skills'] for c in comparisons],
                            y=[c['experience'] for c in comparisons],
                            mode='markers+text',
                            text=[c['name'][:15] for c in comparisons],
                            textposition="top center",
                            marker=dict(size=15, color=[c['score'] for c in comparisons], colorscale='Viridis', showscale=True)
                        )
                    ])
                    fig2.update_layout(
                        title="Skills vs Experience",
                        xaxis_title="Skills Count",
                        yaxis_title="Experience (Years)"
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                
                # Download comparison report
                report = comparator.generate_comparison_report(comparisons)
                st.download_button(
                    label="📥 Download Comparison Report",
                    data=report,
                    file_name="resume_comparison_report.txt",
                    mime="text/plain"
                )

elif uploaded_files and len(uploaded_files) == 1:
    st.warning("⚠️ Please upload at least 2 resumes to compare")
else:
    st.info("👆 Upload multiple resumes to get started")
    st.markdown("""
    ### How to use:
    1. Upload 2 or more resumes (any format)
    2. Click 'Compare Resumes'
    3. View rankings and visualizations
    4. Download comparison report
    """)