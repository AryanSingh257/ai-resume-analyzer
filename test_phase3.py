from utils.resume_parser import ResumeParser
from utils.text_extractor import TextExtractor
from utils.ats_scorer import ATSScorer
import json

# Initialize
extractor = TextExtractor()
parser = ResumeParser()
scorer = ATSScorer()

# Read the test resume
with open('/home/aryan/Codes/ClgProjects/resume-analyzer/data/sample_resumes/test_resume.txt', 'r') as f:
    resume_text = f.read()

clean_text = extractor.clean_text(resume_text)

# Parse resume
parsed_data = parser.parse_resume(clean_text)

# Sample job description
job_description = """
Software Developer position requiring Python, React, and Node.js experience.
Must have experience with machine learning and MongoDB.
Strong communication and leadership skills required.
"""

# Calculate ATS score
ats_result = scorer.calculate_ats_score(clean_text, job_description)

# Calculate job match
job_match = scorer.calculate_job_match(clean_text, job_description)

# Find missing keywords
missing_keywords = scorer.find_missing_keywords(clean_text, job_description)

# Display results
print("=" * 50)
print("RESUME ANALYSIS REPORT")
print("=" * 50)
print(f"\n📊 ATS Score: {ats_result['score']}/100")
print(f"Rating: {ats_result['rating']}")
print(f"\n🎯 Job Match: {job_match}%")

print("\n📝 Feedback:")
for item in ats_result['feedback']:
    print(f"  {item}")

print(f"\n🔍 Missing Keywords: {', '.join(missing_keywords[:5])}")

print("\n👤 Contact Info:")
print(json.dumps(parsed_data['contact_info'], indent=2))

print(f"\n💼 Skills Found: {parsed_data['skills']['total_count']}")
print(f"Technical: {', '.join(parsed_data['skills']['technical'][:5])}")