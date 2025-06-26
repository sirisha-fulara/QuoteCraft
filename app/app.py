from flask import Flask, render_template, request,send_from_directory
import joblib
import numpy as np
import re
from scipy.sparse import hstack, csr_matrix
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")
CORS(app)

model = joblib.load("../models/model.pkl")
vectorizer = joblib.load("../models/vectorizer.pkl")

skill_map = {"Beginner": 0, "Intermediate": 1, "Expert": 2}

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.strip()

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        desc_raw = data.get("description", "")
        skill_raw = data.get("skill", "Intermediate")
        desc = clean_text(desc_raw)
        skill_encoded = skill_map.get(skill_raw, 1)

        if not desc:
            return {"error": "Description cannot be empty."}, 400

        X_tfidf = vectorizer.transform([desc])
        skill_feature = csr_matrix(np.array([skill_encoded]).reshape(1, 1))
        X_final = hstack([X_tfidf, skill_feature])

        log_prediction = model.predict(X_final)[0]
        prediction = int(np.clip(np.expm1(log_prediction), 5, 2000))

        return {"prediction": f"${prediction:,}"}

    except Exception as e:
        return {"error": str(e)}, 500

# Serve React frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True)