
from pathlib import Path
import subprocess
import sys
import joblib

ROOT = Path(__file__).resolve().parent
MODEL = ROOT / "models" / "language_model.joblib"


def load_model():

    if not MODEL.exists():

        print("Model not found. Training Kaggle dataset...")

        subprocess.run(
            [sys.executable, str(ROOT / "train_model.py")],
            check=True,
            cwd=str(ROOT)
        )

    return joblib.load(MODEL)


def analyze_text(text):

    text = (text or "").strip()

    if len(text) < 8:

        return {
            "score": None,
            "label": "Insufficient text",
            "category": None,
            "confidence": None,
            "probabilities": {}
        }

    model = load_model()

    probabilities = model.predict_proba([text])[0]

    classes = list(model.classes_)

    probability_by_class = {
        category: float(probability) * 100
        for category, probability in zip(classes, probabilities)
    }

    predicted_category = max(
        probability_by_class,
        key=probability_by_class.get
    )

    confidence = probability_by_class[predicted_category]

    normal_probability = probability_by_class.get("Normal", 0.0)

    indicator_score = 100.0 - normal_probability

    return {
        "score": round(float(indicator_score), 1),
        "label": f"Dataset category: {predicted_category}",
        "category": predicted_category,
        "confidence": round(confidence, 1),
        "probabilities": {
            category: round(probability, 2)
            for category, probability in probability_by_class.items()
        }
    }
