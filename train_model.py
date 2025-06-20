# -*- coding: utf-8 -*-
"""train_model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1b5XLCySZETOh9UeDvRi2VC0ioT-97CTt
"""

# 📌 BACKEND: train_model.ipynb

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import joblib

# 1. Load the Excel file
df = pd.read_excel("cityscopedata.xlsx")  # Make sure it's uploaded in Colab

# 2. Extract questions and answers
questions = df['Question'].astype(str)
answers = df['Answer'].astype(str)

# 3. Vectorize the questions using TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

# 4. Train Nearest Neighbors model
model = NearestNeighbors(n_neighbors=1, metric='cosine')
model.fit(X)

# 5. Save the model and vectorizer
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("✅ Model and Vectorizer saved successfully!")