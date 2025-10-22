import nltk
import os

def download_nltk_data():
    """Download required NLTK data"""
    packages = ['punkt', 'stopwords', 'wordnet']
    
    for package in packages:
        try:
            nltk.data.find(f'tokenizers/{package}')
        except LookupError:
            nltk.download(package, quiet=True)

if __name__ == "__main__":
    download_nltk_data()
