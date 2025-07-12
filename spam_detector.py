import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib

def train_model():
    df = pd.read_csv(r"C:\Users\anush\OneDrive\Desktop\email_automation_project\spam.csv")

    df = df.rename(columns={"Message": "text", "Category": "label"})
    df = df[["text", "label"]]

    X = df["text"]
    y = df["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    vectorizer = CountVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = MultinomialNB()
    model.fit(X_train_vec, y_train)
    y_pred = model.predict(X_test_vec)

    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    joblib.dump(model, "spam_classifier.joblib")
    joblib.dump(vectorizer.vocabulary_, "training_vocab.joblib")
    print(" Model trained and saved as 'spam_classifier.joblib' and 'training_vocab.joblib'")

if __name__ == "__main__":
    train_model()
