import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from scipy.sparse import hstack
import joblib
import os

# Load dataset
df = pd.read_csv('../data/processed/cleaned_data_with_skills.csv')
df = df[(df['budget_cleaned'] > 0) & (df['budget_cleaned'] <= 5000)]

# Assign skill levels based on market-based price ranges
def assign_skill(price):
    if price < 50:
        return "Beginner"
    elif 50 <= price <= 300:
        return "Intermediate"
    else:
        return "Expert"

df['skill'] = df['budget_cleaned'].apply(assign_skill)

# Map skills to numeric labels
skill_map = {"Beginner": 0, "Intermediate": 1, "Expert": 2}
df['skill_encoded'] = df['skill'].map(skill_map)

# Log transform the target variable
df['log_budget'] = np.log1p(df['budget_cleaned'])

# TF-IDF Vectorization - limit to 99 features
vectorizer = TfidfVectorizer(max_features=99)
X_tfidf = vectorizer.fit_transform(df["description_cleaned"])

# Combine TF-IDF features with skill feature (reshape skill column)
skill_feature = np.array(df["skill_encoded"]).reshape(-1, 1)
X_combined = hstack([X_tfidf, skill_feature])

# Target variable
y = df["log_budget"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.2, random_state=42)

# Train RandomForest Regressor
model = RandomForestRegressor(n_estimators=100, max_depth=20, random_state=42)
model.fit(X_train, y_train)

# Evaluate model performance
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"Model trained! RMSE: {rmse:.4f}")

# Save model and vectorizer for later use
os.makedirs('../models', exist_ok=True)
joblib.dump(model, '../models/model.pkl')
joblib.dump(vectorizer, '../models/vectorizer.pkl')

print("Model & vectorizer saved!")
print("Vectorizer vocabulary size:", len(vectorizer.vocabulary_))
