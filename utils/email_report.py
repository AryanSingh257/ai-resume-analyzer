class EmailReportGenerator:
    """Generate email-friendly resume analysis reports"""
    
    def __init__(self):
        pass
    
    def generate_email_report(self, parsed_data, ats_result, job_match=None):
        """Generate a formatted email report"""
        
        report = f"""
Subject: Your Resume Analysis Report

Dear {parsed_data['contact_info']['name']},

Thank you for using our AI-Powered Resume Analyzer! Here's your comprehensive resume analysis:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 ANALYSIS SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 ATS Compatibility Score: {ats_result['score']}/100
⭐ Rating: {ats_result['rating']}
"""
        
        if job_match:
            report += f"🎯 Job Match: {job_match}%\n"
        
        report += f"""
�� Total Skills Found: {parsed_data['skills']['total_count']}
📅 Experience: {parsed_data['experience']['total_years']} years

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 CONTACT INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Name: {parsed_data['contact_info']['name']}
Email: {parsed_data['contact_info']['email'] or 'Not found'}
Phone: {parsed_data['contact_info']['phone'] or 'Not found'}
LinkedIn: {parsed_data['contact_info']['links']['linkedin'] or 'Not added'}
GitHub: {parsed_data['contact_info']['links']['github'] or 'Not added'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 IMPROVEMENT SUGGESTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        
        for i, feedback in enumerate(ats_result['feedback'], 1):
            report += f"{i}. {feedback}\n"
        
        report += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔑 YOUR SKILLS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Technical Skills ({len(parsed_data['skills']['technical'])}):
{', '.join(parsed_data['skills']['technical'][:15])}

Soft Skills ({len(parsed_data['skills']['soft'])}):
{', '.join(parsed_data['skills']['soft'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Review and implement the suggestions above
2. Update your resume and re-analyze
3. Track your progress in the Analytics Dashboard
4. Check our Resume Tips page for best practices

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Need help? Visit our Tips & Best Practices page for detailed guidance.

Best regards,
AI Resume Analyzer Team

---
This is an automated report. Please do not reply to this email.
Generated on: {self._get_timestamp()}
"""
        
        return report
    
    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
