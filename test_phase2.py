from utils.resume_parser import ResumeParser
from utils.text_extractor import TextExtractor
import json

# Initialize
extractor = TextExtractor()
parser = ResumeParser()

# Read the test resume
with open('/home/aryan/Codes/ClgProjects/resume-analyzer/data/sample_resumes/test_resume.txt', 'r') as f:
    text = f.read()

# Clean the text
clean_text = extractor.clean_text(text)

# Parse the resume
parsed_data = parser.parse_resume(clean_text)

# Print results nicely
print(json.dumps(parsed_data, indent=2))