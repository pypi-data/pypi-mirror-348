from langid_indian import LanguageIdentifier

def test_prediction():
    identifier = LanguageIdentifier()
    text = "यह एक परीक्षण है"  # Sample Hindi text
    lang = identifier.predict(text)
    print(f"Predicted language: {lang}")

if __name__ == "__main__":
    test_prediction()
