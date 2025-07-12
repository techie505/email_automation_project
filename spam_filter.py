import joblib
from sklearn.feature_extraction.text import CountVectorizer
import os

model = joblib.load("spam_classifier.joblib")

vectorizer = CountVectorizer()
vectorizer.fit(joblib.load("training_vocab.joblib"))  
def is_spam(text):
    vector = vectorizer.transform([text])
    return model.predict(vector)[0] == "spam"
