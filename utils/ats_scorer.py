import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ATSScorer:
    """Calculate ATS score and match resume with job description"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
    
    def calculate_ats_score(self, resume_text, job_description=""):
        """Calculate ATS compatibility score (0-100)"""
        score = 0
        feedback = []
        
        # 1. Check for contact info (20 points)
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text):
            score += 10
        else:
            feedback.append("❌ Add email address")
        
        if re.search(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', resume_text):
            score += 10
        else:
            feedback.append("❌ Add phone number")
        
        # 2. Check for section headers (20 points)
        sections = ['education', 'experience', 'skills', 'projects']
        found_sections = sum(1 for s in sections if s in resume_text.lower())
        score += (found_sections / len(sections)) * 20
        
        if found_sections < len(sections):
            missing = [s for s in sections if s not in resume_text.lower()]
            feedback.append(f"❌ Add sections: {', '.join(missing)}")
        
        # 3. Check formatting (15 points)
        lines = resume_text.split('\n')
        if len(lines) > 10:  # Reasonable length
            score += 5
        
        # Check for bullet points
        if '•' in resume_text or '-' in resume_text:
            score += 5
        else:
            feedback.append("❌ Use bullet points for better readability")
        
        # Check for action verbs
        action_verbs = ['developed', 'created', 'managed', 'led', 'designed', 
                       'implemented', 'improved', 'achieved']
        if any(verb in resume_text.lower() for verb in action_verbs):
            score += 5
        else:
            feedback.append("❌ Use action verbs (developed, created, managed, etc.)")
        
        # 4. Check length (10 points)
        word_count = len(resume_text.split())
        if 300 <= word_count <= 800:
            score += 10
        elif word_count < 300:
            feedback.append("❌ Resume too short - add more details")
        else:
            feedback.append("⚠️ Resume too long - keep it concise")
        
        # 5. Check for quantifiable achievements (15 points)
        if re.search(r'\d+%|\d+ users|\d+ projects', resume_text, re.IGNORECASE):
            score += 15
        else:
            feedback.append("❌ Add quantifiable achievements (numbers, percentages)")
        
        # 6. Job description matching (20 points)
        if job_description:
            match_score = self.calculate_job_match(resume_text, job_description)
            score += match_score * 0.2
            if match_score < 50:
                feedback.append("❌ Low keyword match with job description")
        else:
            score += 10  # Default partial credit
        
        if not feedback:
            feedback.append("✅ Resume looks good!")
        
        return {
            'score': min(score, 100),  # Cap at 100
            'feedback': feedback,
            'rating': self._get_rating(score)
        }
    
    def calculate_job_match(self, resume_text, job_description):
        """Calculate similarity between resume and job description"""
        try:
            # Create TF-IDF vectors
            documents = [resume_text.lower(), job_description.lower()]
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Convert to percentage
            return round(similarity * 100, 2)
        except:
            return 0
    
    def find_missing_keywords(self, resume_text, job_description):
        """Find keywords in job description missing from resume"""
        # Extract important words from job description
        jd_words = set(re.findall(r'\b[a-z]{4,}\b', job_description.lower()))
        resume_words = set(re.findall(r'\b[a-z]{4,}\b', resume_text.lower()))
        
        # Common words to ignore
        stop_words = {'that', 'with', 'from', 'have', 'this', 'will', 'your', 
                     'about', 'their', 'which', 'they', 'been', 'were', 'what'}
        
        # Find missing keywords
        missing = jd_words - resume_words - stop_words
        
        # Return top 10 most relevant
        return list(missing)[:10]
    
    def _get_rating(self, score):
        """Convert score to rating"""
        if score >= 90:
            return "Excellent ⭐⭐⭐⭐⭐"
        elif score >= 75:
            return "Good ⭐⭐⭐⭐"
        elif score >= 60:
            return "Average ⭐⭐⭐"
        elif score >= 40:
            return "Needs Improvement ⭐⭐"
        else:
            return "Poor ⭐"