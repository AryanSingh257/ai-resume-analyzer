import streamlit as st
import json
import os

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

st.title("⚙️ Settings & Configuration")
st.markdown("Customize your resume analyzer experience")

# Create config directory
if not os.path.exists('config'):
    os.makedirs('config')

config_file = 'config/settings.json'

# Default settings
default_settings = {
    'ats_weights': {
        'contact_info': 20,
        'section_structure': 20,
        'formatting': 15,
        'content_length': 10,
        'achievements': 15,
        'job_match': 20
    },
    'min_ats_score': 60,
    'preferred_skills': [],
    'alert_on_low_score': True,
    'show_advanced_metrics': False
}

# Load settings
def load_settings():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return default_settings

# Save settings
def save_settings(settings):
    with open(config_file, 'w') as f:
        json.dump(settings, f, indent=2)

settings = load_settings()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["⚖️ ATS Scoring", "🎯 Preferences", "📊 Display", "🔄 Reset"])

with tab1:
    st.subheader("ATS Score Weights")
    st.markdown("Customize how different factors contribute to the ATS score")
    
    col1, col2 = st.columns(2)
    
    with col1:
        contact_weight = st.slider(
            "Contact Information",
            0, 50, settings['ats_weights']['contact_info'],
            help="Weight for email, phone, links"
        )
        
        structure_weight = st.slider(
            "Section Structure",
            0, 50, settings['ats_weights']['section_structure'],
            help="Weight for proper sections"
        )
        
        format_weight = st.slider(
            "Formatting Quality",
            0, 50, settings['ats_weights']['formatting'],
            help="Weight for formatting and readability"
        )
    
    with col2:
        length_weight = st.slider(
            "Content Length",
            0, 50, settings['ats_weights']['content_length'],
            help="Weight for appropriate length"
        )
        
        achieve_weight = st.slider(
            "Quantifiable Achievements",
            0, 50, settings['ats_weights']['achievements'],
            help="Weight for metrics and numbers"
        )
        
        match_weight = st.slider(
            "Job Description Match",
            0, 50, settings['ats_weights']['job_match'],
            help="Weight for keyword matching"
        )
    
    total_weight = (contact_weight + structure_weight + format_weight + 
                   length_weight + achieve_weight + match_weight)
    
    if total_weight != 100:
        st.warning(f"⚠️ Total weight is {total_weight}%. Should be 100%.")
    else:
        st.success("✅ Weights sum to 100%")
    
    if st.button("Save ATS Weights"):
        settings['ats_weights'] = {
            'contact_info': contact_weight,
            'section_structure': structure_weight,
            'formatting': format_weight,
            'content_length': length_weight,
            'achievements': achieve_weight,
            'job_match': match_weight
        }
        save_settings(settings)
        st.success("✅ Settings saved!")

with tab2:
    st.subheader("Preferences")
    
    min_score = st.slider(
        "Minimum Acceptable ATS Score",
        0, 100, settings['min_ats_score'],
        help="Get alerts when score is below this"
    )
    
    alert_low = st.checkbox(
        "Alert on Low ATS Score",
        value=settings['alert_on_low_score'],
        help="Show warning when score is below minimum"
    )
    
    st.markdown("---")
    st.subheader("Preferred Skills (Optional)")
    st.markdown("Add skills you want to track across resumes")
    
    preferred_skills = st.text_area(
        "Skills (comma-separated)",
        value=', '.join(settings.get('preferred_skills', [])),
        placeholder="Python, JavaScript, React, Machine Learning"
    )
    
    if st.button("Save Preferences"):
        settings['min_ats_score'] = min_score
        settings['alert_on_low_score'] = alert_low
        settings['preferred_skills'] = [s.strip() for s in preferred_skills.split(',') if s.strip()]
        save_settings(settings)
        st.success("✅ Preferences saved!")

with tab3:
    st.subheader("Display Options")
    
    show_advanced = st.checkbox(
        "Show Advanced Metrics",
        value=settings.get('show_advanced_metrics', False),
        help="Display additional technical metrics"
    )
    
    theme = st.selectbox(
        "Color Theme",
        ["Default", "Dark", "Light"],
        help="Appearance preference (requires app restart)"
    )
    
    show_tips = st.checkbox(
        "Show Inline Tips",
        value=True,
        help="Display helpful tips throughout the app"
    )
    
    if st.button("Save Display Settings"):
        settings['show_advanced_metrics'] = show_advanced
        settings['theme'] = theme
        settings['show_tips'] = show_tips
        save_settings(settings)
        st.success("✅ Display settings saved!")

with tab4:
    st.subheader("Reset Settings")
    
    st.warning("⚠️ This will reset all settings to default values")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🔄 Reset to Defaults", type="secondary"):
            save_settings(default_settings)
            st.success("✅ Settings reset to defaults!")
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Analytics History"):
            if os.path.exists('analytics_data/history.json'):
                os.remove('analytics_data/history.json')
                st.success("✅ Analytics history cleared!")

# Display current settings
st.divider()
st.subheader("📄 Current Configuration")

with st.expander("View Current Settings"):
    st.json(settings)

st.divider()

st.markdown("""
### 💡 Tips:

- **ATS Weights**: Adjust based on your industry standards
- **Minimum Score**: Set realistic targets (60-70 for beginners, 80+ for experienced)
- **Preferred Skills**: Track specific skills relevant to your field
- **Display Options**: Customize for your workflow

### 🔒 Privacy Note:
All settings are stored locally on your machine. No data is sent to external servers.
""")

