from .model_loader import load_model

class LanguageIdentifier:
    def __init__(self):
        self.model, self.vectorizer = load_model()

    def predict(self, text: str) -> str:
        X = self.vectorizer.transform([text])
        pred = self.model.predict(X)
        return pred[0]
