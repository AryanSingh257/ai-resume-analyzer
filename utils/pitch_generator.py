class InterviewPitchGenerator:
    """Generate interview pitches based on resume data"""
    
    def __init__(self):
        self.common_questions = [
            "Tell me about yourself",
            "What is your personal brand?",
            "Why should we hire you?",
            "What are your key strengths?",
            "Where do you see yourself in 5 years?",
            "What makes you unique?",
            "Describe your ideal work environment",
            "What motivates you?",
            "Why are you interested in this role?",
            "What value can you bring to our team?"
        ]
    
    def generate_tell_me_about_yourself(self, parsed_data, target_role=None, company_name=None):
        """Generate 'Tell me about yourself' pitch"""
        
        name = parsed_data['contact_info']['name']
        experience_years = parsed_data['experience']['total_years']
        tech_skills = parsed_data['skills']['technical'][:5]  # Top 5 skills
        education = parsed_data.get('education', [])
        
        # Build the pitch
        pitch = f"Hello, I'm {name}. "
        
        # Education background
        if education:
            degree = education[0]['degree']
            pitch += f"I hold a {degree} degree, "
        
        # Experience
        if experience_years > 0:
            pitch += f"and I have {experience_years} years of professional experience "
        else:
            pitch += f"and I'm a recent graduate with strong foundational skills "
        
        # Skills
        if tech_skills:
            skills_str = ", ".join(tech_skills[:3])
            pitch += f"in {skills_str}. "
        
        # Specific experiences
        experiences = parsed_data['experience']['details']
        if experiences:
            recent_role = experiences[0]['title']
            pitch += f"\n\nIn my recent role as a {recent_role}, I've worked on various projects "
            pitch += "that have helped me develop both technical and collaborative skills. "
        
        # Target role connection
        if target_role:
            pitch += f"\n\nI'm particularly interested in {target_role} positions because "
            pitch += "they align perfectly with my skill set and career aspirations. "
        
        # Company specific
        if company_name:
            pitch += f"I'm excited about the opportunity at {company_name} because "
            pitch += "I believe my background and passion would make me a valuable addition to your team."
        else:
            pitch += "I'm eager to contribute my skills to a dynamic team and continue growing professionally."
        
        return pitch
    
    def generate_personal_brand(self, parsed_data, brand_keywords=None):
        """Generate personal brand statement"""
        
        tech_skills = parsed_data['skills']['technical']
        soft_skills = parsed_data['skills']['soft']
        experience_years = parsed_data['experience']['total_years']
        
        # Determine professional identity
        if experience_years >= 5:
            identity = "seasoned professional"
        elif experience_years >= 2:
            identity = "experienced professional"
        else:
            identity = "passionate technologist"
        
        pitch = f"I am a {identity} who combines "
        
        # Technical expertise
        if tech_skills:
            primary_skills = tech_skills[:3]
            pitch += f"expertise in {', '.join(primary_skills)} "
        
        # Soft skills
        if soft_skills:
            pitch += f"with strong {soft_skills[0].lower()} and {soft_skills[1].lower()} skills. "
        
        pitch += "\n\nMy brand is built on three pillars:\n"
        
        # Pillars based on data
        pillars = []
        
        if len(tech_skills) >= 5:
            pillars.append("**Technical Excellence**: Proficient in multiple technologies and always learning")
        
        if len(soft_skills) >= 2:
            pillars.append("**Collaboration**: Strong team player with excellent communication")
        
        if parsed_data['experience']['total_years'] > 0:
            pillars.append("**Results-Driven**: Proven track record of delivering impactful projects")
        else:
            pillars.append("**Innovation**: Fresh perspective with enthusiasm for problem-solving")
        
        for i, pillar in enumerate(pillars[:3], 1):
            pitch += f"{i}. {pillar}\n"
        
        # User-provided keywords
        if brand_keywords:
            pitch += f"\n**My defining qualities:** {', '.join(brand_keywords)}"
        
        return pitch
    
    def generate_why_hire_you(self, parsed_data, target_role=None, company_values=None):
        """Generate 'Why should we hire you?' pitch"""
        
        tech_skills = parsed_data['skills']['technical']
        soft_skills = parsed_data['skills']['soft']
        experience_years = parsed_data['experience']['total_years']
        
        pitch = "You should hire me because I bring a unique combination of:\n\n"
        
        reasons = []
        
        # Technical proficiency
        if tech_skills:
            top_skills = ", ".join(tech_skills[:4])
            reasons.append(
                f"**1. Technical Proficiency**: I have hands-on experience with {top_skills}, "
                "which directly aligns with your technical requirements."
            )
        
        # Experience or fresh perspective
        if experience_years >= 2:
            reasons.append(
                f"**2. Proven Experience**: With {experience_years} years of professional experience, "
                "I've successfully delivered multiple projects and understand industry best practices."
            )
        else:
            reasons.append(
                "**2. Fresh Perspective**: As a recent graduate, I bring current knowledge of "
                "latest technologies and innovative approaches to problem-solving."
            )
        
        # Soft skills
        if soft_skills:
            reasons.append(
                f"**3. Strong Interpersonal Skills**: My {soft_skills[0].lower()} and "
                f"{soft_skills[1].lower() if len(soft_skills) > 1 else 'adaptability'} skills "
                "ensure smooth collaboration and effective communication within teams."
            )
        
        # Quick learner
        skill_count = parsed_data['skills']['total_count']
        if skill_count >= 10:
            reasons.append(
                f"**4. Continuous Learner**: With {skill_count} skills in my arsenal, "
                "I've demonstrated my ability to quickly adapt and learn new technologies."
            )
        
        # Company-specific
        if company_values:
            reasons.append(
                f"**5. Cultural Fit**: Your company's values of {', '.join(company_values)} "
                "resonate strongly with my personal values and work ethic."
            )
        else:
            reasons.append(
                "**5. Passion & Drive**: I'm genuinely passionate about technology and "
                "committed to contributing meaningfully to your team's success."
            )
        
        pitch += "\n\n".join(reasons[:5])
        
        pitch += "\n\n**In short**, I offer the perfect blend of technical skills, relevant experience, "
        pitch += "and cultural fit that will make me productive from day one."
        
        return pitch
    
    def generate_key_strengths(self, parsed_data):
        """Generate key strengths pitch"""
        
        tech_skills = parsed_data['skills']['technical']
        soft_skills = parsed_data['skills']['soft']
        experience = parsed_data['experience']['details']
        
        pitch = "My key strengths that set me apart are:\n\n"
        
        strengths = []
        
        # Technical depth
        if len(tech_skills) >= 5:
            strengths.append(
                f"**🔧 Technical Versatility**: Proficient in {len(tech_skills)} different "
                f"technologies including {', '.join(tech_skills[:3])}, enabling me to adapt "
                "to various project requirements quickly."
            )
        
        # Problem solving
        if 'problem solving' in [s.lower() for s in soft_skills]:
            strengths.append(
                "**💡 Problem-Solving**: Strong analytical abilities to break down complex "
                "challenges and develop efficient, scalable solutions."
            )
        
        # Leadership/teamwork
        if any(skill.lower() in ['leadership', 'teamwork', 'collaboration'] for skill in soft_skills):
            strengths.append(
                "**👥 Collaboration**: Excellent team player with proven ability to work "
                "effectively in cross-functional teams and mentor junior members."
            )
        
        # Communication
        if 'communication' in [s.lower() for s in soft_skills]:
            strengths.append(
                "**💬 Communication**: Ability to translate technical concepts into clear, "
                "understandable language for both technical and non-technical stakeholders."
            )
        
        # Project experience
        if len(experience) >= 2:
            strengths.append(
                f"**📊 Proven Track Record**: Successfully delivered {len(experience)} projects, "
                "demonstrating my ability to meet deadlines and exceed expectations."
            )
        
        for strength in strengths[:5]:
            pitch += f"{strength}\n\n"
        
        pitch += "These strengths, combined with my continuous learning mindset, make me a "
        pitch += "valuable asset who can contribute immediately while growing with the organization."
        
        return pitch
    
    def generate_five_year_vision(self, parsed_data, target_role=None):
        """Generate 5-year career vision"""
        
        experience_years = parsed_data['experience']['total_years']
        tech_skills = parsed_data['skills']['technical']
        
        pitch = "In the next five years, I envision myself:\n\n"
        
        timeline = []
        
        # Year 1-2
        if experience_years < 2:
            timeline.append(
                "**Years 1-2**: Building a strong foundation by mastering core technologies "
                f"like {', '.join(tech_skills[:2]) if tech_skills else 'relevant tech stack'}, "
                "taking ownership of features, and learning from experienced team members."
            )
        else:
            timeline.append(
                "**Years 1-2**: Taking on more complex projects, leading small teams, and "
                "mentoring junior developers while deepening my technical expertise."
            )
        
        # Year 3-4
        timeline.append(
            "**Years 3-4**: Growing into a technical leadership role, architecting solutions, "
            "and contributing to strategic technical decisions that drive business impact."
        )
        
        # Year 5
        if target_role and 'senior' not in target_role.lower():
            timeline.append(
                f"**Year 5**: Advancing to a senior role, possibly as a Senior {target_role or 'Developer'}, "
                "where I can mentor others, lead critical initiatives, and contribute to the company's "
                "long-term technical vision."
            )
        else:
            timeline.append(
                "**Year 5**: Taking on a leadership position where I can drive innovation, "
                "mentor teams, and contribute to both technical excellence and business growth."
            )
        
        for item in timeline:
            pitch += f"{item}\n\n"
        
        pitch += "Throughout this journey, I'm committed to continuous learning, staying updated "
        pitch += "with industry trends, and adding value to every team I work with."
        
        return pitch
    
    def generate_what_makes_you_unique(self, parsed_data, unique_points=None):
        """Generate uniqueness pitch"""
        
        tech_skills = parsed_data['skills']['technical']
        soft_skills = parsed_data['skills']['soft']
        education = parsed_data.get('education', [])
        
        pitch = "What makes me unique is the combination of:\n\n"
        
        unique_aspects = []
        
        # Diverse skill set
        if len(tech_skills) >= 8:
            unique_aspects.append(
                f"**🎯 Diverse Technical Arsenal**: Unlike typical candidates who specialize in "
                f"one area, I bring expertise across {len(tech_skills)} technologies, from "
                f"{tech_skills[0]} to {tech_skills[-1]}, allowing me to see the bigger picture."
            )
        
        # Balanced profile
        if len(tech_skills) >= 5 and len(soft_skills) >= 3:
            unique_aspects.append(
                "**⚖️ Technical + Interpersonal Balance**: I combine strong technical capabilities "
                "with excellent soft skills, making me effective at both coding and collaborating."
            )
        
        # Educational background
        if education:
            degree = education[0]['degree']
            unique_aspects.append(
                f"**🎓 Strong Foundation**: My {degree} background provides me with solid "
                "theoretical knowledge that I complement with hands-on practical experience."
            )
        
        # User-provided unique points
        if unique_points:
            for i, point in enumerate(unique_points, 1):
                unique_aspects.append(f"**✨ {point}**")
        
        # Learning agility
        unique_aspects.append(
            "**📚 Rapid Learner**: My track record of picking up new technologies quickly "
            "means I can adapt to your tech stack and start contributing faster than most."
        )
        
        for aspect in unique_aspects[:5]:
            pitch += f"{aspect}\n\n"
        
        pitch += "This unique combination allows me to bring fresh perspectives, bridge gaps "
        pitch += "between teams, and deliver value from multiple angles."
        
        return pitch
    
    def generate_custom_pitch(self, question, parsed_data, additional_context=None):
        """Generate pitch for custom question"""
        
        tech_skills = parsed_data['skills']['technical'][:5]
        experience_years = parsed_data['experience']['total_years']
        
        pitch = f"**Question:** {question}\n\n**Answer:**\n\n"
        
        # Generic template
        pitch += f"Based on my background with {', '.join(tech_skills)} "
        
        if experience_years > 0:
            pitch += f"and {experience_years} years of experience, "
        
        pitch += "I believe I can address this effectively.\n\n"
        
        if additional_context:
            pitch += f"{additional_context}\n\n"
        
        pitch += "I'm committed to bringing value through my technical skills, collaborative "
        pitch += "approach, and dedication to continuous improvement."
        
        return pitch
    
    def generate_all_pitches(self, parsed_data, preferences=None):
        """Generate all common pitches"""
        
        if preferences is None:
            preferences = {}
        
        pitches = {
            "Tell me about yourself": self.generate_tell_me_about_yourself(
                parsed_data,
                preferences.get('target_role'),
                preferences.get('company_name')
            ),
            "What is your personal brand?": self.generate_personal_brand(
                parsed_data,
                preferences.get('brand_keywords')
            ),
            "Why should we hire you?": self.generate_why_hire_you(
                parsed_data,
                preferences.get('target_role'),
                preferences.get('company_values')
            ),
            "What are your key strengths?": self.generate_key_strengths(parsed_data),
            "Where do you see yourself in 5 years?": self.generate_five_year_vision(
                parsed_data,
                preferences.get('target_role')
            ),
            "What makes you unique?": self.generate_what_makes_you_unique(
                parsed_data,
                preferences.get('unique_points')
            )
        }
        
        return pitches
