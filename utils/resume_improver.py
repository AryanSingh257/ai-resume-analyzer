class ResumeImprover:
    """Generate specific improvement suggestions for resumes"""
    
    def __init__(self):
        self.action_verbs = [
            'Developed', 'Created', 'Implemented', 'Managed', 'Led',
            'Designed', 'Built', 'Improved', 'Achieved', 'Increased',
            'Reduced', 'Optimized', 'Delivered', 'Launched', 'Established'
        ]
        
        self.power_words = [
            'successfully', 'efficiently', 'effectively', 'strategically',
            'collaboratively', 'independently', 'proactively'
        ]
    
    def analyze_and_suggest(self, parsed_data, resume_text):
        """Generate comprehensive improvement suggestions"""
        suggestions = {
            'critical': [],
            'important': [],
            'nice_to_have': []
        }
        
        # Critical suggestions
        if not parsed_data['contact_info']['email']:
            suggestions['critical'].append({
                'issue': 'Missing Email',
                'suggestion': 'Add a professional email address at the top of your resume',
                'example': 'john.doe@email.com'
            })
        
        if not parsed_data['contact_info']['phone']:
            suggestions['critical'].append({
                'issue': 'Missing Phone Number',
                'suggestion': 'Include your phone number for recruiters to contact you',
                'example': '+91-9876543210'
            })
        
        if parsed_data['skills']['total_count'] < 5:
            suggestions['critical'].append({
                'issue': 'Too Few Skills Listed',
                'suggestion': 'Add more relevant skills. Aim for at least 10-15 skills',
                'example': 'Add technical skills like programming languages, tools, frameworks'
            })
        
        # Important suggestions
        if not parsed_data['contact_info']['links']['linkedin']:
            suggestions['important'].append({
                'issue': 'Missing LinkedIn Profile',
                'suggestion': 'Add your LinkedIn profile URL to increase credibility',
                'example': 'linkedin.com/in/yourname'
            })
        
        if not parsed_data['contact_info']['links']['github']:
            suggestions['important'].append({
                'issue': 'Missing GitHub Profile',
                'suggestion': 'For tech roles, include your GitHub profile to showcase projects',
                'example': 'github.com/yourusername'
            })
        
        # Check for action verbs
        has_action_verbs = any(verb.lower() in resume_text.lower() for verb in self.action_verbs)
        if not has_action_verbs:
            suggestions['important'].append({
                'issue': 'Weak Action Verbs',
                'suggestion': 'Start bullet points with strong action verbs',
                'example': 'Use: "Developed", "Implemented", "Led" instead of "Responsible for"'
            })
        
        # Check for quantifiable achievements
        import re
        has_numbers = bool(re.search(r'\d+%|\d+ users|\d+ projects|\$\d+', resume_text))
        if not has_numbers:
            suggestions['important'].append({
                'issue': 'Lack of Quantifiable Achievements',
                'suggestion': 'Add numbers and metrics to demonstrate impact',
                'example': '"Improved performance by 30%", "Managed team of 5", "Reduced costs by $10K"'
            })
        
        # Nice to have suggestions
        if len(parsed_data.get('education', [])) == 0:
            suggestions['nice_to_have'].append({
                'issue': 'Education Section Missing',
                'suggestion': 'Add your educational qualifications',
                'example': 'B.Tech in Computer Science, XYZ University (2019-2023)'
            })
        
        if len(parsed_data['experience']['details']) == 0:
            suggestions['nice_to_have'].append({
                'issue': 'No Work Experience Listed',
                'suggestion': 'Include internships, projects, or freelance work',
                'example': 'Software Developer Intern at ABC Company (June 2022 - Aug 2022)'
            })
        
        word_count = len(resume_text.split())
        if word_count < 200:
            suggestions['nice_to_have'].append({
                'issue': 'Resume Too Short',
                'suggestion': f'Your resume has only {word_count} words. Aim for 300-800 words',
                'example': 'Add more details about your projects, responsibilities, and achievements'
            })
        elif word_count > 1000:
            suggestions['nice_to_have'].append({
                'issue': 'Resume Too Long',
                'suggestion': f'Your resume has {word_count} words. Keep it concise (300-800 words)',
                'example': 'Remove redundant information and focus on relevant achievements'
            })
        
        return suggestions
    
    def generate_improvement_plan(self, suggestions):
        """Generate a prioritized improvement plan"""
        plan = "RESUME IMPROVEMENT PLAN\n"
        plan += "=" * 60 + "\n\n"
        
        if suggestions['critical']:
            plan += "🚨 CRITICAL (Fix Immediately):\n"
            plan += "-" * 60 + "\n"
            for i, sug in enumerate(suggestions['critical'], 1):
                plan += f"{i}. {sug['issue']}\n"
                plan += f"   → {sug['suggestion']}\n"
                plan += f"   Example: {sug['example']}\n\n"
        
        if suggestions['important']:
            plan += "⚠️  IMPORTANT (High Priority):\n"
            plan += "-" * 60 + "\n"
            for i, sug in enumerate(suggestions['important'], 1):
                plan += f"{i}. {sug['issue']}\n"
                plan += f"   → {sug['suggestion']}\n"
                plan += f"   Example: {sug['example']}\n\n"
        
        if suggestions['nice_to_have']:
            plan += "💡 NICE TO HAVE (When Time Permits):\n"
            plan += "-" * 60 + "\n"
            for i, sug in enumerate(suggestions['nice_to_have'], 1):
                plan += f"{i}. {sug['issue']}\n"
                plan += f"   → {sug['suggestion']}\n"
                plan += f"   Example: {sug['example']}\n\n"
        
        return plan