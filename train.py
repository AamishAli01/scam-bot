import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load data
df = pd.read_csv("balanced_data.csv")

print("Before cleaning:", len(df))

# 🔥 STEP 1: REMOVE EMPTY VALUES (IMPORTANT FIX)
df = df.dropna()

# 🔥 STEP 2: REMOVE EMPTY STRINGS
df = df[df['message'].str.strip() != ""]
df = df[df['label'].str.strip() != ""]

# 🔥 STEP 3: FINAL CLEAN
df = df.reset_index(drop=True)

print("After cleaning:", len(df))

# Features & labels
X = df['message']
y = df['label']

# Convert text
vectorizer = TfidfVectorizer(ngram_range=(1,2))
X_vec = vectorizer.fit_transform(X)

# Model
model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_vec, y)

# Save
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("✅ Model trained successfully!")