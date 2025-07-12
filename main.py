import csv
import time
import os
from email_sender import send_email
import joblib
from sklearn.feature_extraction.text import CountVectorizer


model = joblib.load("spam_classifier.joblib")
vocab = joblib.load("training_vocab.joblib")


vectorizer = CountVectorizer(decode_error="replace", vocabulary=vocab)


with open("templates/email_template.txt", "r") as f:
    template = f.read()


attachment_files = [os.path.join("attachments", "5th sem.pdf")]

with open("emails.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row["name"]
        email = row["email"]
        body = template.format(name=name)

        
        X_test = vectorizer.transform([body])
        prediction = model.predict(X_test)[0]

        if prediction == "spam":
            print(f"🚫 Message to {name} not sent: Detected as SPAM!")
        else:
            send_email(email, name, body, attachment_files)
            time.sleep(8)  