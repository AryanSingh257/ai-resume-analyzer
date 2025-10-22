# 🚀 Quick Start Guide

## For First-Time Users

### Step 1: Installation (5 minutes)
```bash
# Navigate to project
cd resume-analyzer

# Activate virtual environment
source venv/bin/activate

# Verify installation
pip list | grep -E "streamlit|spacy|sklearn"
```

### Step 2: Run the App
```bash
streamlit run app.py
```

App will open at: `http://localhost:8501`

### Step 3: Try It Out

#### Test Single Resume
1. Go to main page
2. Upload `data/sample_resumes/test_resume.txt`
3. View results

#### Test Job Matching
1. Upload resume
2. Paste this job description:
```
Software Developer position requiring Python, React, Machine Learning.
Must have strong communication skills and 2+ years experience.
```
3. View match percentage

#### Test Comparison
1. Go to "Compare Resumes" page
2. Upload multiple resumes
3. View rankings

## For Expo Demo

### Pre-Demo Checklist
- [ ] Laptop charged
- [ ] Internet connection (for first run)
- [ ] Sample resumes ready
- [ ] Job description prepared
- [ ] App tested and working
- [ ] Backup plan ready

### 5-Minute Demo Script
1. **Start** (30s): Introduce problem
2. **Upload** (60s): Show poor resume analysis
3. **Compare** (60s): Compare 3 resumes
4. **Track** (45s): Show progress dashboard
5. **Conclude** (45s): Highlight key features

### Common Demo Issues
**Issue:** App won't start
**Fix:** `streamlit run app.py --server.port 8502`

**Issue:** File won't upload
**Fix:** Check file size < 10MB

**Issue:** Slow processing
**Fix:** Mention it's processing locally, not cloud

## Troubleshooting

### venv not activating
```bash
deactivate  # If already in a venv
source venv/bin/activate
```

### Module not found
```bash
pip install -r requirements.txt
```

### spaCy model missing
```bash
python -m spacy download en_core_web_sm
```

### Port already in use
```bash
streamlit run app.py --server.port 8503
```

## Quick Commands
```bash
# Start app
streamlit run app.py

# Stop app
Ctrl + C

# Check what's running
lsof -i :8501

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Support

Issues? Check:
1. README.md - Full documentation
2. demo_script.md - Demo guidelines
3. GitHub Issues - Report bugs
