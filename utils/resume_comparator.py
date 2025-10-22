class ResumeComparator:
    """Compare multiple resumes and rank them"""
    
    def __init__(self):
        pass
    
    def compare_resumes(self, resumes_data, job_description=""):
        """
        Compare multiple resumes
        resumes_data: list of dicts with 'name' and 'parsed_data' keys
        """
        comparisons = []
        
        for resume in resumes_data:
            name = resume['name']
            data = resume['parsed_data']
            text = resume['text']
            
            # Calculate metrics
            total_skills = data['skills']['total_count']
            experience_years = data['experience']['total_years']
            has_email = 1 if data['contact_info']['email'] else 0
            has_phone = 1 if data['contact_info']['phone'] else 0
            has_linkedin = 1 if data['contact_info']['links']['linkedin'] else 0
            has_github = 1 if data['contact_info']['links']['github'] else 0
            education_count = len(data.get('education', []))
            experience_count = len(data['experience']['details'])
            
            # Calculate overall score (0-100)
            score = (
                (total_skills * 2) +  # Skills worth 2 points each
                (experience_years * 5) +  # Experience worth 5 points per year
                (has_email * 5) +
                (has_phone * 5) +
                (has_linkedin * 5) +
                (has_github * 5) +
                (education_count * 10) +
                (experience_count * 5)
            )
            
            score = min(score, 100)  # Cap at 100
            
            comparisons.append({
                'name': name,
                'score': score,
                'skills': total_skills,
                'experience': experience_years,
                'education': education_count,
                'completeness': (has_email + has_phone + has_linkedin + has_github) * 25
            })
        
        # Sort by score descending
        comparisons.sort(key=lambda x: x['score'], reverse=True)
        
        return comparisons
    
    def generate_comparison_report(self, comparisons):
        """Generate a text report of comparison"""
        report = "RESUME COMPARISON REPORT\n"
        report += "=" * 60 + "\n\n"
        
        for i, comp in enumerate(comparisons, 1):
            report += f"{i}. {comp['name']}\n"
            report += f"   Overall Score: {comp['score']}/100\n"
            report += f"   Skills: {comp['skills']}\n"
            report += f"   Experience: {comp['experience']} years\n"
            report += f"   Education: {comp['education']} degree(s)\n"
            report += f"   Profile Completeness: {comp['completeness']}%\n"
            report += "\n"
        
        return report