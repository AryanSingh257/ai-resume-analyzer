from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import os

class JobRolePredictor:
    """Predict job role from resume text using ML"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=500)
        self.model = MultinomialNB()
        self.is_trained = False
        
        # Job roles and their typical keywords
        self.job_roles = {
            'Software Developer': ['python', 'java', 'javascript', 'react', 'node.js', 'backend', 'frontend', 'api'],
            'Data Scientist': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'statistics', 'data analysis'],
            'Web Developer': ['html', 'css', 'javascript', 'react', 'angular', 'vue', 'responsive', 'ui/ux'],
            'DevOps Engineer': ['docker', 'kubernetes', 'jenkins', 'aws', 'azure', 'ci/cd', 'terraform', 'linux'],
            'Mobile Developer': ['android', 'ios', 'swift', 'kotlin', 'react native', 'flutter', 'mobile app'],
            'Data Analyst': ['excel', 'sql', 'tableau', 'power bi', 'data visualization', 'analytics', 'reporting'],
            'ML Engineer': ['machine learning', 'tensorflow', 'pytorch', 'neural networks', 'nlp', 'computer vision', 'deep learning'],
            'Full Stack Developer': ['frontend', 'backend', 'full stack', 'react', 'node.js', 'mongodb', 'sql', 'api']
        }
    
    def create_training_data(self):
        """Create synthetic training data from job roles"""
        texts = []
        labels = []
        
        for role, keywords in self.job_roles.items():
            # Create 10 variations for each role
            for i in range(10):
                # Randomly combine keywords
                import random
                sample_keywords = random.sample(keywords, min(5, len(keywords)))
                text = ' '.join(sample_keywords * random.randint(2, 5))
                texts.append(text)
                labels.append(role)
        
        return texts, labels
    
    def train(self):
        """Train the model with synthetic data"""
        texts, labels = self.create_training_data()
        
        # Vectorize
        X = self.vectorizer.fit_transform(texts)
        
        # Train
        self.model.fit(X, labels)
        self.is_trained = True
        
        print("✅ Model trained successfully!")
    
    def predict(self, resume_text):
        """Predict job role from resume"""
        if not self.is_trained:
            self.train()
        
        # Vectorize resume
        X = self.vectorizer.transform([resume_text.lower()])
        
        # Predict
        prediction = self.model.predict(X)[0]
        
        # Get probability scores
        probabilities = self.model.predict_proba(X)[0]
        
        # Get top 3 predictions
        top_indices = probabilities.argsort()[-3:][::-1]
        top_roles = [(self.model.classes_[i], probabilities[i] * 100) for i in top_indices]
        
        return {
            'predicted_role': prediction,
            'top_3_roles': top_roles,
            'confidence': max(probabilities) * 100
        }
    
    def save_model(self, filepath='models/job_predictor.pkl'):
        """Save trained model"""
        os.makedirs('models', exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump((self.vectorizer, self.model), f)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath='models/job_predictor.pkl'):
        """Load trained model"""
        try:
            with open(filepath, 'rb') as f:
                self.vectorizer, self.model = pickle.load(f)
            self.is_trained = True
            print(f"Model loaded from {filepath}")
        except FileNotFoundError:
            print("No saved model found. Training new model...")
            self.train()