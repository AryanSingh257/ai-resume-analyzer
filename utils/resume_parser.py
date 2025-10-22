import re
import spacy
import pdfplumber
from docx import Document

class ResumeParser:
    """Parse resume and extract structured information from multiple file formats"""
    
    def __init__(self):
        # Load spaCy model for NER
        self.nlp = spacy.load('en_core_web_sm')
    
    def read_file(self, file_path):
        """Read and extract text from different file formats"""
        if file_path.endswith('.pdf'):
            return self._read_pdf(file_path)
        elif file_path.endswith('.docx'):
            return self._read_docx(file_path)
        elif file_path.endswith('.txt'):
            return self._read_txt(file_path)
        else:
            raise ValueError("Unsupported file format. Use PDF, DOCX, or TXT")
    
    def _read_pdf(self, file_path):
        """Extract text from PDF file"""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return self._clean_text(text)
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None
    
    def _read_docx(self, file_path):
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return self._clean_text(text)
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            return None
    
    def _read_txt(self, file_path):
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return self._clean_text(text)
        except Exception as e:
            print(f"Error reading TXT: {e}")
            return None
    
    def _clean_text(self, text):
        """Clean extracted text"""
        if not text:
            return ""
        
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep essential punctuation
        text = re.sub(r'[^\w\s@.,:()\-/]', '', text)
        return text.strip()
    
    def extract_text_from_uploaded_file(self, uploaded_file):
        """Extract text from Streamlit uploaded file object"""
        file_name = uploaded_file.name
        
        if file_name.endswith('.txt'):
            return self._clean_text(uploaded_file.getvalue().decode('utf-8'))
        
        elif file_name.endswith('.pdf'):
            # Save temporarily
            with open("temp_file.pdf", "wb") as f:
                f.write(uploaded_file.getvalue())
            text = self._read_pdf("temp_file.pdf")
            # Clean up temp file
            import os
            os.remove("temp_file.pdf")
            return text
        
        elif file_name.endswith('.docx'):
            # Save temporarily
            with open("temp_file.docx", "wb") as f:
                f.write(uploaded_file.getvalue())
            text = self._read_docx("temp_file.docx")
            # Clean up temp file
            import os
            os.remove("temp_file.docx")
            return text
        
        else:
            raise ValueError("Unsupported file format")
    
    def extract_name(self, text):
        """Extract name from resume (usually at the top)"""
        lines = text.split('\n')[:5]  # Check first 5 lines
        
        # Try spaCy NER first
        for line in lines:
            if len(line.strip()) > 0:
                doc = self.nlp(line)
                for ent in doc.ents:
                    if ent.label_ == 'PERSON':
                        return ent.text
        
        # Fallback: first non-empty line that looks like a name
        for line in lines:
            line = line.strip()
            words = line.split()
            if 1 <= len(words) <= 4 and line[0].isupper() and not any(char.isdigit() for char in line):
                return line
        
        return "Name not found"
    
    def extract_email(self, text):
        """Extract email address"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else None
    
    def extract_phone(self, text):
        """Extract phone number"""
        # Multiple phone patterns
        patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # +1-234-567-8900
            r'\+?\d{2}[-.\s]?\d{10}',  # +91-9876543210
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # (123) 456-7890
            r'\d{10}',  # 9876543210
        ]
        
        for pattern in patterns:
            phones = re.findall(pattern, text)
            for phone in phones:
                digits = re.sub(r'\D', '', phone)
                if 10 <= len(digits) <= 15:
                    return phone.strip()
        
        return None
    
    def extract_links(self, text):
        """Extract LinkedIn, GitHub, Portfolio URLs"""
        urls = {
            'linkedin': None,
            'github': None,
            'portfolio': None
        }
        
        # LinkedIn pattern
        linkedin_pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+'
        linkedin = re.search(linkedin_pattern, text, re.IGNORECASE)
        if linkedin:
            urls['linkedin'] = linkedin.group()
        
        # GitHub pattern
        github_pattern = r'(?:https?://)?(?:www\.)?github\.com/[\w-]+'
        github = re.search(github_pattern, text, re.IGNORECASE)
        if github:
            urls['github'] = github.group()
        
        # Portfolio/website pattern
        url_pattern = r'https?://(?:www\.)?[\w\-\.]+\.\w{2,}(?:/[\w\-\./?%&=]*)?'
        all_urls = re.findall(url_pattern, text)
        for url in all_urls:
            if 'linkedin' not in url.lower() and 'github' not in url.lower():
                urls['portfolio'] = url
                break
        
        return urls
    
    def extract_skills(self, text):
        """Extract technical and soft skills with word boundary checking"""
        
        import re
        
        technical_skills = {
            # Programming Languages (exact matches needed)
            'python': ['python'],
            'java': ['java', 'javase', 'javaee'],
            'javascript': ['javascript', 'js'],
            'c++': ['c++', 'cpp'],
            'c#': ['c#', 'csharp'],
            'c': ['\\bc\\b'],  # Word boundary for single letter
            'ruby': ['ruby'],
            'php': ['php'],
            'swift': ['swift'],
            'kotlin': ['kotlin'],
            'go': ['\\bgolang\\b', '\\bgo\\b'],  # Specific patterns
            'rust': ['rust'],
            'typescript': ['typescript', 'ts'],
            'r': ['\\br\\b'],  # Word boundary
            'matlab': ['matlab'],
            'scala': ['scala'],
            
            # Web Technologies
            'html': ['html', 'html5'],
            'css': ['css', 'css3'],
            'react': ['react', 'reactjs', 'react.js'],
            'angular': ['angular', 'angularjs'],
            'vue': ['vue', 'vuejs', 'vue.js'],
            'node.js': ['node.js', 'nodejs', 'node'],
            'express': ['express', 'expressjs', 'express.js'],
            'django': ['django'],
            'flask': ['flask'],
            'spring': ['spring', 'spring boot', 'springboot'],
            'asp.net': ['asp.net', 'aspnet'],
            'jquery': ['jquery'],
            'bootstrap': ['bootstrap'],
            'tailwind': ['tailwind', 'tailwindcss'],
            
            # Databases
            'sql': ['sql'],
            'mysql': ['mysql'],
            'postgresql': ['postgresql', 'postgres'],
            'mongodb': ['mongodb', 'mongo'],
            'oracle': ['oracle db', 'oracle'],
            'redis': ['redis'],
            'cassandra': ['cassandra'],
            'dynamodb': ['dynamodb'],
            'sqlite': ['sqlite'],
            'firebase': ['firebase'],
            'nosql': ['nosql'],
            
            # ML/AI
            'machine learning': ['machine learning', 'ml'],
            'deep learning': ['deep learning', 'dl'],
            'tensorflow': ['tensorflow'],
            'pytorch': ['pytorch'],
            'keras': ['keras'],
            'scikit-learn': ['scikit-learn', 'sklearn', 'scikit learn'],
            'pandas': ['pandas'],
            'numpy': ['numpy'],
            'opencv': ['opencv'],
            'nlp': ['nlp', 'natural language processing'],
            'computer vision': ['computer vision', 'cv'],
            'neural networks': ['neural networks', 'neural network', 'nn'],
            'ai': ['artificial intelligence', '\\bai\\b'],
            
            # Cloud & DevOps
            'aws': ['aws', 'amazon web services'],
            'azure': ['azure', 'microsoft azure'],
            'gcp': ['gcp', 'google cloud'],
            'google cloud': ['google cloud platform', 'google cloud'],
            'docker': ['docker'],
            'kubernetes': ['kubernetes', 'k8s'],
            'jenkins': ['jenkins'],
            'git': ['\\bgit\\b'],  # Word boundary to avoid "digit"
            'github': ['github'],
            'gitlab': ['gitlab'],
            'ci/cd': ['ci/cd', 'ci cd', 'cicd'],
            'terraform': ['terraform'],
            'ansible': ['ansible'],
            
            # Other
            'rest api': ['rest api', 'restful', 'rest'],
            'graphql': ['graphql'],
            'microservices': ['microservices', 'micro services'],
            'agile': ['agile'],
            'scrum': ['scrum'],
            'linux': ['linux'],
            'unix': ['unix'],
            'bash': ['bash'],
            'power bi': ['power bi', 'powerbi'],
            'tableau': ['tableau'],
            'excel': ['excel', 'ms excel'],
            'data structures': ['data structures', 'dsa'],
            'algorithms': ['algorithms', 'algo'],
            'oop': ['oop', 'object oriented'],
            'testing': ['testing', 'unit testing']
        }
        
        soft_skills = {
            'leadership': ['leadership', 'leader', 'leading'],
            'communication': ['communication', 'communicate'],
            'teamwork': ['teamwork', 'team work', 'team player'],
            'problem solving': ['problem solving', 'problem-solving'],
            'critical thinking': ['critical thinking'],
            'time management': ['time management'],
            'adaptability': ['adaptability', 'adaptable'],
            'collaboration': ['collaboration', 'collaborate'],
            'creativity': ['creativity', 'creative'],
            'analytical': ['analytical', 'analysis'],
            'presentation': ['presentation'],
            'negotiation': ['negotiation'],
            'conflict resolution': ['conflict resolution'],
            'decision making': ['decision making', 'decision-making']
        }
        
        found_technical = set()
        found_soft = set()
        
        text_lower = text.lower()
        
        # Find technical skills
        for skill_name, patterns in technical_skills.items():
            for pattern in patterns:
                # Use regex with word boundaries for better matching
                if '\\b' in pattern:
                    # Already has word boundaries
                    if re.search(pattern, text_lower):
                        found_technical.add(skill_name.title())
                        break
                else:
                    # Add word boundaries
                    regex_pattern = r'\b' + re.escape(pattern) + r'\b'
                    if re.search(regex_pattern, text_lower):
                        found_technical.add(skill_name.title())
                        break
        
        # Find soft skills
        for skill_name, patterns in soft_skills.items():
            for pattern in patterns:
                regex_pattern = r'\b' + re.escape(pattern) + r'\b'
                if re.search(regex_pattern, text_lower, re.IGNORECASE):
                    found_soft.add(skill_name.title())
                    break
        
        return {
            'technical': sorted(list(found_technical)),
            'soft': sorted(list(found_soft)),
            'total_count': len(found_technical) + len(found_soft)
        }
    
    def _extract_section(self, text, section_keywords):
        """Helper: Extract text under a section heading"""
        text_lower = text.lower()
        
        for keyword in section_keywords:
            # Look for section headers
            patterns = [
                r'\n\s*' + keyword + r'\s*:?\s*\n',
                r'\n\s*' + keyword + r'\s*$',
                r'^' + keyword + r'\s*:?\s*\n'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text_lower, re.MULTILINE)
                
                if match:
                    start = match.end()
                    
                    # Find next section (usually starts with capital letter)
                    next_section = re.search(r'\n[A-Z][A-Z\s]{3,}:?\s*\n', text[start:])
                    end = start + next_section.start() if next_section else len(text)
                    
                    return text[start:end].strip()
        
        return None
    
    def extract_education(self, text):
        """Extract education details"""
        education = []
        
        degree_patterns = [
            r'B\.?Tech|Bachelor of Technology|BTech',
            r'B\.?E\.?|Bachelor of Engineering',
            r'M\.?Tech|Master of Technology|MTech',
            r'MBA|Master of Business Administration',
            r'B\.?Sc|Bachelor of Science|BSc',
            r'M\.?Sc|Master of Science|MSc',
            r'BCA|Bachelor of Computer Applications',
            r'MCA|Master of Computer Applications',
            r'Ph\.?D|Doctorate|PhD',
            r'B\.?A\.?|Bachelor of Arts',
            r'M\.?A\.?|Master of Arts'
        ]
        
        # Try to find education section first
        education_section = self._extract_section(text, 
            ['education', 'academic', 'qualification', 'academics'])
        
        if not education_section:
            education_section = text
        
        # Extract degrees
        for pattern in degree_patterns:
            matches = re.finditer(pattern, education_section, re.IGNORECASE)
            for match in matches:
                # Get context around the degree
                start = max(0, match.start() - 150)
                end = min(len(education_section), match.end() + 150)
                context = education_section[start:end]
                
                # Extract year
                year_pattern = r'20\d{2}|19\d{2}'
                years = re.findall(year_pattern, context)
                
                # Extract university/college
                uni_pattern = r'(?:at|from)?\s*([A-Z][A-Za-z\s&,\.]+(?:University|College|Institute|School))'
                university = re.search(uni_pattern, context)
                
                education.append({
                    'degree': match.group(),
                    'year': years[-1] if years else 'N/A',
                    'institution': university.group(1).strip() if university else 'N/A'
                })
        
        return education
    
    def extract_experience(self, text):
        """Extract work experience"""
        experience = []
        
        # Find experience section
        exp_section = self._extract_section(text, 
            ['experience', 'work history', 'employment', 'professional experience', 'work experience'])
        
        if not exp_section:
            exp_section = text
        
        # Common job title keywords
        title_keywords = [
            'engineer', 'developer', 'analyst', 'manager', 'consultant',
            'intern', 'associate', 'specialist', 'architect', 'lead',
            'designer', 'scientist', 'administrator', 'coordinator'
        ]
        
        # Extract job titles
        for keyword in title_keywords:
            pattern = r'([A-Z][A-Za-z\s]+?' + keyword + r'[A-Za-z\s]*?)(?:\s+at\s+|\n|,)'
            titles = re.finditer(pattern, exp_section, re.IGNORECASE)
            
            for match in titles:
                title = match.group(1).strip()
                
                # Get context for company and duration
                start = match.start()
                end = min(len(exp_section), match.end() + 200)
                context = exp_section[start:end]
                
                # Extract company
                company_pattern = r'at\s+([A-Z][A-Za-z\s&,\.]+?)(?:\n|,|\s{2,})'
                company = re.search(company_pattern, context)
                
                # Extract duration
                duration_pattern = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})\s*[-–to]+\s*((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}|Present)'
                duration = re.search(duration_pattern, context, re.IGNORECASE)
                
                experience.append({
                    'title': title,
                    'company': company.group(1).strip() if company else 'N/A',
                    'duration': duration.group() if duration else 'N/A'
                })
        
        # Remove duplicates
        seen = set()
        unique_exp = []
        for exp in experience:
            key = (exp['title'].lower(), exp['company'].lower())
            if key not in seen:
                seen.add(key)
                unique_exp.append(exp)
        
        return unique_exp
    
    def calculate_experience_years(self, text):
        """Calculate total years of experience"""
        year_pattern = r'20\d{2}|19\d{2}'
        years = [int(y) for y in re.findall(year_pattern, text)]
        
        if len(years) >= 2:
            # Calculate difference between max and min year
            total_years = max(years) - min(years)
            return min(total_years, 40)  # Cap at reasonable maximum
        
        return 0
    
    def parse_resume_from_file(self, file_path):
        """Parse resume directly from file path"""
        text = self.read_file(file_path)
        
        if not text:
            raise ValueError("Could not extract text from file")
        
        return self.parse_resume(text)
    
    def parse_resume(self, text):
        """Main method to parse complete resume from text"""
        
        parsed_data = {
            'contact_info': {
                'name': self.extract_name(text),
                'email': self.extract_email(text),
                'phone': self.extract_phone(text),
                'links': self.extract_links(text)
            },
            'education': self.extract_education(text),
            'skills': self.extract_skills(text),
            'experience': {
                'details': self.extract_experience(text),
                'total_years': self.calculate_experience_years(text)
            },
            'raw_text': text[:500] + "..." if len(text) > 500 else text  # First 500 chars
        }
        
        return parsed_data