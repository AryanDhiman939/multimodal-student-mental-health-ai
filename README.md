# Student Wellbeing AI V4.0 — Photo Analysis

## New feature
Capture one still photograph with Streamlit camera input. MediaPipe Face Mesh detects facial landmarks and draws their positions over the image. The photo is processed in memory and this project does not save it to a database.

## Run (Windows / IntelliJ)
Open this folder in IntelliJ. In its terminal run:
```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
Open http://localhost:8501, choose **Photo analysis**, allow camera permission and capture one photograph.

## Optional NLP model training
```powershell
python train_model.py
```

## Project structure
app.py, questionnaire.py, text_analysis.py, risk_prediction.py, face_analysis.py, train_model.py, requirements.txt, data/demo_text_dataset.csv, models/ (generated model).

## Limitations
This is an academic prototype, not a medical device or diagnosis. Face Mesh detects geometric landmarks only; it does not classify emotions or infer stress, depression, anxiety, or mental-health status. Facial appearance cannot reliably reveal mental health. Photo analysis is not used in the wellbeing score. The questionnaire is custom-made and unvalidated; the small text dataset is synthetic. Real research requires supervisor/ethics approval, informed consent, privacy review and professional oversight. Run locally and do not use real student data in a public deployment.
