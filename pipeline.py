import re
import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ==============================
# TEXT CLEAN FUNCTION
# ==============================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text

# ==============================
# LOAD DATA
# ==============================
df1 = pd.read_csv("data.csv", sep="\t", names=["label", "message"], header=None)
df2 = pd.read_csv("SMSSpamCollection.csv", sep="\t", names=["label", "message"], header=None)

df = pd.concat([df1, df2], ignore_index=True)

print("Before cleaning:", len(df))

# ==============================
# CLEAN DATA
# ==============================
df = df[['label', 'message']].dropna()
df = df[df['message'].astype(str).str.strip() != ""]

df['message'] = df['message'].apply(clean_text)

df['label'] = df['label'].astype(str).str.lower()
df['label'] = df['label'].replace({
    'ham': 'safe',
    'spam': 'scam'
})

df = df[df['label'].isin(['safe', 'scam'])]
df = df.drop_duplicates()

print("After cleaning:", len(df))

# ==============================
# BALANCE DATA
# ==============================
min_size = df['label'].value_counts().min()
df = df.groupby('label').sample(n=min_size, random_state=42)

print("Balanced:")
print(df['label'].value_counts())

# ==============================
# SPLIT DATA
# ==============================
X = df['message']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ==============================
# VECTORIZER (UPGRADED)
# ==============================
vectorizer = TfidfVectorizer(
    ngram_range=(1,3),
    max_features=10000,
    stop_words='english'
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# ==============================
# MODEL
# ==============================
model = LogisticRegression(max_iter=2000)
model.fit(X_train_vec, y_train)

# ==============================
# EVALUATION
# ==============================
y_pred = model.predict(X_test_vec)
print("Accuracy:", accuracy_score(y_test, y_pred))

# ==============================
# SAVE MODEL
# ==============================
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("✅ FINAL MODEL READY")