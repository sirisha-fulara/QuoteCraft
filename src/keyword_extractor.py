import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

def extract_keywords(texts, top_n=5):
    cv= CountVectorizer(max_features=1000, stop_words='english')
    bow_matrix= cv.fit_transform(texts)
    feature_names=cv.get_feature_names_out()

    keywords=[]
    for row in bow_matrix:
        row_data= row.toarray()[0]
        top_indices = row_data.argsort()[::-1][:top_n]
        top_keywords = [feature_names[i] for i in top_indices]
        keywords.append(', '.join(top_keywords))

    return keywords

if __name__=="__main__":
    df = pd.read_csv("../data/processed/cleaned_data.csv")

    df['extracted_skills'] = extract_keywords(df['description_cleaned'])

    df.to_csv("../data/processed/cleaned_data_with_skills.csv", index=False)
    print("✅ BoW-based keywords extracted and saved!")