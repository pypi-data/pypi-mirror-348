import os
import requests
import joblib

MODEL_URL = "https://huggingface.co/yash-ingle/langid-indian-model/resolve/main/model.pkl"
VECTORIZER_URL = "https://huggingface.co/yash-ingle/langid-indian-model/resolve/main/vectorizer.pkl"

CACHE_DIR = os.path.expanduser("~/.langid_indian_cache")

def download_file(url: str, local_path: str):
    if not os.path.exists(local_path):
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        print(f"Downloading {url} ...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(local_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    else:
        print(f"Using cached file {local_path}")

def load_model():
    model_path = os.path.join(CACHE_DIR, "model.pkl")
    vectorizer_path = os.path.join(CACHE_DIR, "vectorizer.pkl")

    download_file(MODEL_URL, model_path)
    download_file(VECTORIZER_URL, vectorizer_path)

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    return model, vectorizer
