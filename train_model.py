from pathlib import Path
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "Combined Data.csv"
MODEL_DIR = ROOT / "models"
MODEL_FILE = MODEL_DIR / "language_model.joblib"


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}\n"
            "Place the Kaggle CSV inside the project's data folder "
            "and name it exactly: Combined Data.csv"
        )

    print("Loading Kaggle dataset...")
    df = pd.read_csv(DATA_FILE)

    required_columns = {"statement", "status"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(
            "Dataset is missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    # Keep only the columns needed for text classification.
    df = df[["statement", "status"]].copy()

    # Clean missing/blank rows and remove duplicate examples.
    df["statement"] = df["statement"].fillna("").astype(str).str.strip()
    df["status"] = df["status"].fillna("").astype(str).str.strip()
    df = df[(df["statement"] != "") & (df["status"] != "")]
    df = df.drop_duplicates(subset=["statement", "status"])

    if df["status"].nunique() < 2:
        raise ValueError("At least two different status labels are required.")

    print(f"Usable records: {len(df):,}")
    print("\nClass distribution:")
    print(df["status"].value_counts().to_string())

    X_train, X_test, y_train, y_test = train_test_split(
        df["statement"],
        df["status"],
        test_size=0.20,
        random_state=42,
        stratify=df["status"]
    )

    model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                ngram_range=(1, 2),
                stop_words="english",
                max_features=50000,
                min_df=2
            )
        ),
        (
            "clf",
            LogisticRegression(
                max_iter=1500,
                class_weight="balanced",
                random_state=42
            )
        )
    ])

    print("\nTraining TF-IDF + Logistic Regression...")
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print(f"\nTest accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print("\nClassification report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_FILE)

    print(f"\nTrained model saved to: {MODEL_FILE}")
    print(
        "Note: These are dataset-label text classifications, "
        "not clinical diagnoses or validated mental-health assessments."
    )


if __name__ == "__main__":
    main()
