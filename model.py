import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

# Sample dataset
data = pd.DataFrame({
    'text': [
        'Congratulations! You won a free iPhone',
        'Call this number now to claim prize',
        'Meeting scheduled at 10am',
        'Lunch at 2pm today?',
        'URGENT! Your account has been compromised',
        'Can we reschedule the interview?'
    ],
    'label': ['spam', 'spam', 'ham', 'ham', 'spam', 'ham']
})

# Train model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['text'])
y = data['label']

model = MultinomialNB()
model.fit(X, y)

# Save model and vectorizer
joblib.dump(model, 'spam_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
