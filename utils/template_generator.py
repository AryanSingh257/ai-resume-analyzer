class ResumeTemplateGenerator:
    """Generate resume templates based on user input"""
    
    def __init__(self):
        pass
    
    def generate_markdown_template(self, job_role="Software Developer"):
        """Generate a markdown resume template"""
        
        templates = {
            "Software Developer": """
# [YOUR NAME]

**Email:** your.email@example.com | **Phone:** +91-XXXXXXXXXX  
**LinkedIn:** linkedin.com/in/yourname | **GitHub:** github.com/yourusername  
**Location:** City, State

---

## PROFESSIONAL SUMMARY

Results-driven Software Developer with [X] years of experience in developing scalable applications. Proficient in [Technologies]. Passionate about building efficient solutions and continuous learning.

---

## TECHNICAL SKILLS

**Languages:** Python, Java, JavaScript, C++  
**Frameworks:** React, Node.js, Django, Flask  
**Databases:** MySQL, MongoDB, PostgreSQL  
**Tools:** Git, Docker, AWS, Jenkins  
**Soft Skills:** Problem Solving, Team Collaboration, Communication

---

## WORK EXPERIENCE

### Software Developer | [Company Name]
*[Month Year] – Present | [Location]*

- Developed and maintained web applications using React and Node.js, serving 10,000+ users
- Implemented RESTful APIs that improved system performance by 30%
- Collaborated with cross-functional teams to deliver features on time
- Conducted code reviews and mentored junior developers

### Software Developer Intern | [Company Name]
*[Month Year] – [Month Year] | [Location]*

- Built responsive web interfaces using React and Material-UI
- Integrated third-party APIs and payment gateways
- Reduced page load time by 40% through optimization techniques
- Participated in Agile sprint planning and daily standups

---

## PROJECTS

### E-Commerce Platform
*Technologies: React, Node.js, MongoDB, Stripe*

- Developed full-stack e-commerce application with user authentication
- Implemented shopping cart, payment processing, and order management
- Deployed on AWS with CI/CD pipeline using GitHub Actions

### Machine Learning Image Classifier
*Technologies: Python, TensorFlow, Flask*

- Built CNN model for image classification with 92% accuracy
- Created REST API for model serving using Flask
- Deployed as web application with real-time predictions

---

## EDUCATION

### Bachelor of Technology in Computer Science
**[University Name]** | [City, State]  
*Graduated: [Month Year]* | **CGPA:** X.XX/10.00

**Relevant Coursework:** Data Structures, Algorithms, Database Systems, Machine Learning

---

## CERTIFICATIONS

- AWS Certified Developer Associate | [Year]
- Machine Learning Specialization - Coursera | [Year]
- React Developer Certification | [Year]

---

## ACHIEVEMENTS

- Won 1st place in College Hackathon [Year]
- Published research paper on [Topic] in [Conference/Journal]
- Contributed to 5+ open-source projects on GitHub
""",
            
            "Data Scientist": """
# [YOUR NAME]

**Email:** your.email@example.com | **Phone:** +91-XXXXXXXXXX  
**LinkedIn:** linkedin.com/in/yourname | **GitHub:** github.com/yourusername  
**Portfolio:** yourportfolio.com

---

## PROFESSIONAL SUMMARY

Data Scientist with [X] years of experience in statistical analysis, machine learning, and data visualization. Skilled at extracting insights from complex datasets and building predictive models.

---

## TECHNICAL SKILLS

**Languages:** Python, R, SQL  
**ML/DL:** TensorFlow, PyTorch, Scikit-learn, Keras  
**Data Tools:** Pandas, NumPy, Matplotlib, Seaborn  
**Visualization:** Tableau, Power BI, Plotly  
**Cloud:** AWS, Azure, Google Cloud Platform  
**Other:** Git, Docker, Jupyter, Apache Spark

---

## WORK EXPERIENCE

### Data Scientist | [Company Name]
*[Month Year] – Present | [Location]*

- Developed predictive models that increased revenue by 25%
- Built recommendation system using collaborative filtering, improving user engagement by 40%
- Analyzed customer data using Python and SQL to identify trends
- Created interactive dashboards in Tableau for executive reporting

### Data Analyst Intern | [Company Name]
*[Month Year] – [Month Year] | [Location]*

- Conducted exploratory data analysis on 1M+ records
- Automated data pipelines using Python, reducing manual work by 60%
- Presented findings to stakeholders with compelling visualizations

---

## PROJECTS

### Customer Churn Prediction
*Technologies: Python, Scikit-learn, XGBoost, Flask*

- Built ML model to predict customer churn with 88% accuracy
- Implemented feature engineering and hyperparameter tuning
- Deployed model as REST API for real-time predictions

### Sentiment Analysis on Social Media
*Technologies: Python, NLP, BERT, Streamlit*

- Analyzed 100K+ tweets using BERT for sentiment classification
- Achieved 91% accuracy on test dataset
- Created interactive web app for real-time sentiment analysis

---

## EDUCATION

### Bachelor/Master of Science in Data Science
**[University Name]** | [City, State]  
*Graduated: [Month Year]* | **CGPA:** X.XX/10.00

**Relevant Coursework:** Statistical Learning, Deep Learning, NLP, Big Data Analytics

---

## CERTIFICATIONS

- Google Data Analytics Professional Certificate
- Deep Learning Specialization - Coursera
- Tableau Desktop Specialist

---

## PUBLICATIONS & ACHIEVEMENTS

- Published paper on [Topic] in [Journal] | [Year]
- Kaggle Expert (Top 5% in competitions)
- Won Best Data Science Project Award | [Year]
"""
        }
        
        return templates.get(job_role, templates["Software Developer"])
    
    def generate_html_template(self, data):
        """Generate a styled HTML resume"""
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get('name', 'Resume')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 850px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 50px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #2c3e50;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        h1 {{
            font-size: 36px;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        .contact-info {{
            color: #555;
            font-size: 14px;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        .section-title {{
            font-size: 20px;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 5px;
            margin-bottom: 15px;
            text-transform: uppercase;
        }}
        .job-title {{
            font-weight: bold;
            color: #2c3e50;
        }}
        .company {{
            color: #3498db;
            font-style: italic;
        }}
        .duration {{
            color: #777;
            font-size: 14px;
        }}
        ul {{
            margin-left: 20px;
            margin-top: 10px;
        }}
        li {{
            margin-bottom: 5px;
        }}
        .skills {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .skill-tag {{
            background: #3498db;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
        }}
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{data.get('name', '[YOUR NAME]')}</h1>
            <div class="contact-info">
                {data.get('email', 'email@example.com')} | 
                {data.get('phone', '+91-XXXXXXXXXX')} | 
                {data.get('linkedin', 'linkedin.com/in/yourname')} | 
                {data.get('github', 'github.com/yourusername')}
            </div>
        </div>

        <div class="section">
            <div class="section-title">Professional Summary</div>
            <p>{data.get('summary', 'Add your professional summary here...')}</p>
        </div>

        <div class="section">
            <div class="section-title">Technical Skills</div>
            <div class="skills">
                {''.join([f'<span class="skill-tag">{skill}</span>' for skill in data.get('skills', ['Python', 'JavaScript', 'React'])])}
            </div>
        </div>

        <div class="section">
            <div class="section-title">Work Experience</div>
            <div style="margin-bottom: 20px;">
                <div class="job-title">Software Developer</div>
                <div class="company">Company Name</div>
                <div class="duration">Jan 2023 - Present</div>
                <ul>
                    <li>Developed and maintained scalable web applications</li>
                    <li>Improved system performance by 30%</li>
                    <li>Collaborated with cross-functional teams</li>
                </ul>
            </div>
        </div>

        <div class="section">
            <div class="section-title">Education</div>
            <div>
                <div class="job-title">B.Tech in Computer Science</div>
                <div class="company">University Name</div>
                <div class="duration">2019 - 2023 | CGPA: 8.5/10</div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">Projects</div>
            <div style="margin-bottom: 15px;">
                <div class="job-title">E-Commerce Platform</div>
                <div class="duration">Technologies: React, Node.js, MongoDB</div>
                <ul>
                    <li>Built full-stack application with 10+ features</li>
                    <li>Implemented payment gateway integration</li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
"""
        return html
    def get_section_suggestions(self, job_role):
        """Get suggestions for each resume section"""
        
        suggestions = {
            "Professional Summary": [
                "Keep it to 2-3 sentences",
                "Highlight years of experience",
                "Mention key technical skills",
                "Include career goals aligned with the role"
            ],
            "Skills": [
                "List 10-15 relevant skills",
                "Categorize: Languages, Frameworks, Tools",
                "Match keywords from job description",
                "Include both technical and soft skills"
            ],
            "Experience": [
                "Start with action verbs (Developed, Implemented, Led)",
                "Quantify achievements with numbers",
                "Focus on impact and results",
                "Use STAR method (Situation, Task, Action, Result)"
            ],
            "Projects": [
                "Include 2-4 significant projects",
                "Mention technologies used",
                "Explain your specific role",
                "Highlight outcomes and metrics"
            ],
            "Education": [
                "List degree and major",
                "Include graduation year and GPA (if >3.0)",
                "Add relevant coursework",
                "Mention academic achievements"
            ]
        }
        
        return suggestions