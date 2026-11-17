import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

from questionnaire import QUESTIONS, score_answers, band
from text_analysis import analyze_text
from risk_prediction import combine, guidance
from face_analysis import analyze_photo


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Student Wellbeing AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "result" not in st.session_state:
    st.session_state.result = None

if "history" not in st.session_state:
    st.session_state.history = []


# --------------------------------------------------
# PROFESSIONAL DARK THEME
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background: #0b1120;
    color: #e5eaf5;
}

[data-testid="stSidebar"] {
    background: #111c30;
    border-right: 1px solid #263550;
}

[data-testid="stSidebar"] * {
    color: #e5eaf5;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.hero {
    background: linear-gradient(120deg, #172554, #1e40af, #0369a1);
    padding: 32px;
    border-radius: 18px;
    margin-bottom: 25px;
    border: 1px solid #31548b;
}

.hero h1 {
    color: white;
    font-size: 32px;
    margin-bottom: 8px;
}

.hero p {
    color: #dbeafe;
    font-size: 16px;
}

.card {
    background: #162238;
    border: 1px solid #293b59;
    padding: 22px;
    border-radius: 15px;
    min-height: 135px;
    margin-bottom: 12px;
}

.card h3 {
    color: #93c5fd;
    font-size: 15px;
}

.card h2 {
    color: white;
    font-size: 27px;
}

.card p {
    color: #aabbd4;
    font-size: 13px;
}

.section-title {
    color: #bfdbfe;
    font-size: 21px;
    font-weight: 700;
    margin-top: 20px;
}

div[data-testid="stMetric"] {
    background: #162238;
    border: 1px solid #293b59;
    padding: 17px;
    border-radius: 13px;
}

div[data-testid="stMetric"] label {
    color: #aabbd4;
}

div[data-testid="stMetricValue"] {
    color: white;
}

.stButton > button {
    border-radius: 9px;
    font-weight: 600;
    min-height: 42px;
}

.stProgress > div > div {
    background-color: #38bdf8;
}

hr {
    border-color: #293b59;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# REUSABLE HEADER
# --------------------------------------------------

def show_hero(title, subtitle):
    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 🧠 Student Wellbeing AI")

    st.caption("V5.0 · AI Research Dashboard")

    st.divider()

    page = st.radio(
        "MAIN MENU",
        [
            "Dashboard",
            "Wellbeing Assessment",
            "Photo Analysis",
            "Assessment History",
            "About Project"
        ]
    )

    st.divider()

    st.markdown("### PROJECT STATUS")

    st.success("System Ready")

    st.caption("Questionnaire module")
    st.caption("NLP analysis module")
    st.caption("MediaPipe face module")

    st.divider()

    st.caption("Academic Research Prototype")
    st.caption("No medical diagnosis")


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    show_hero(
        "🧠 Student Wellbeing Dashboard",
        "A multimodal AI research prototype for exploring student wellbeing indicators."
    )

    st.warning(
        "This is an educational prototype, not a medical diagnostic tool. "
        "Its experimental indicators should not be treated as clinical results."
    )

    # SUMMARY CARDS

    total = len(st.session_state.history)

    if st.session_state.result:
        latest_score = st.session_state.result["final"]
        latest_label = st.session_state.result["label"]
    else:
        latest_score = None
        latest_label = "No assessment yet"

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="card">
                <h3>📊 Total Assessments</h3>
                <h2>{total}</h2>
                <p>Current session only</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        score_display = (
            f"{latest_score:.1f}/100"
            if latest_score is not None
            else "--"
        )

        st.markdown(
            f"""
            <div class="card">
                <h3>🎯 Latest Indicator</h3>
                <h2>{score_display}</h2>
                <p>Experimental awareness indicator</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="card">
                <h3>🧪 AI Modules</h3>
                <h2>03</h2>
                <p>Questionnaire · NLP · Computer Vision</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="section-title">Explore Project Modules</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="card">
                <h3>📝 Questionnaire</h3>
                <p>Explore student responses about sleep, stress,
                concentration and everyday wellbeing.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="card">
                <h3>💬 NLP Text Analysis</h3>
                <p>Demonstrates TF-IDF and Logistic Regression
                for written text pattern analysis.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="card">
                <h3>📷 Facial Landmarks</h3>
                <p>Uses MediaPipe Face Mesh to visualize
                facial landmark positions.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.markdown("### Quick Start")

    st.write(
        "Start a wellbeing assessment using the navigation menu. "
        "You can also explore the webcam-based facial landmark module."
    )

    if st.button("Start Wellbeing Assessment", type="primary"):
        st.session_state.navigate_to_assessment = True
        st.rerun()


# --------------------------------------------------
# WELLBEING ASSESSMENT
# --------------------------------------------------

elif page == "Wellbeing Assessment":

    show_hero(
        "📝 Wellbeing Assessment",
        "Reflect on how you have generally been feeling recently."
    )

    st.info(
        "These are custom academic questions, not a clinically validated "
        "questionnaire. Do not enter identifying information."
    )

    with st.form("assessment_form"):

        st.subheader("Part 1 — Questionnaire")

        labels = [
            "Never",
            "A few days",
            "More than a week",
            "Nearly every day"
        ]

        answers = {}

        for i, question in enumerate(QUESTIONS, start=1):

            answer = st.select_slider(
                f"{i}. {question['question']}",
                options=[0, 1, 2, 3],
                value=0,
                format_func=lambda x, l=labels: l[x]
            )

            answers[question["key"]] = answer

        st.divider()

        st.subheader("Part 2 — Text Analysis")

        reflection = st.text_area(
            "Describe how college or daily life has been feeling lately.",
            placeholder="Example: I have been feeling stressed because of assignments and exams...",
            height=130,
            max_chars=1200
        )

        consent = st.checkbox(
            "I understand that this is an educational prototype "
            "and does not provide a medical diagnosis."
        )

        submitted = st.form_submit_button(
            "Analyse My Responses",
            type="primary",
            use_container_width=True
        )

    if submitted:

        if not consent:

            st.error("Please confirm the prototype's limitations.")

        else:

            try:

                questionnaire_score = score_answers(answers)

                text_result = None
                text_score = None

                if reflection.strip():

                    text_result = analyze_text(reflection)

                    if text_result.get("score") is not None:
                        text_score = text_result["score"]
                    else:
                        text_result = None

                final_score, final_label = combine(
                    questionnaire_score,
                    text_score
                )

                new_result = {
                    "questionnaire": questionnaire_score,
                    "text": text_result,
                    "final": final_score,
                    "label": final_label
                }

                st.session_state.result = new_result

                st.session_state.history.append({
                    "time": datetime.now().strftime("%d %b %Y, %H:%M"),
                    "score": final_score,
                    "label": final_label
                })

            except Exception as error:

                st.error(f"Analysis error: {error}")

    # DISPLAY RESULTS

    if st.session_state.result is not None:

        result = st.session_state.result

        st.divider()

        st.header("📊 Assessment Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Questionnaire Indicator",
                f"{result['questionnaire']:.1f}/100",
                band(result["questionnaire"])
            )

        with col2:

            if result["text"]:

                st.metric(
                    "Language Signal",
                    f"{result['text']['score']:.1f}/100",
                    result["text"]["label"]
                )

            else:

                st.metric(
                    "Language Signal",
                    "Not available",
                    "No usable text analysis"
                )

        with col3:
            st.metric(
                "Combined Awareness Indicator",
                f"{result['final']:.1f}/100",
                result["label"]
            )

        # --------------------------------------------------
        # KAGGLE NLP PREDICTION DETAILS
        # --------------------------------------------------

        if result.get("text") and result["text"].get("probabilities"):

            text_data = result["text"]
            probabilities = text_data["probabilities"]

            st.divider()
            st.header("🤖 AI Prediction Analysis")

            prediction_col, confidence_col = st.columns(2)

            with prediction_col:
                st.markdown("#### Predicted Category")
                st.success(text_data.get("category", "Not available"))

            with confidence_col:
                st.markdown("#### Model Confidence")
                confidence = text_data.get("confidence")
                if confidence is not None:
                    st.metric("Prediction Confidence", f"{confidence:.1f}%")
                else:
                    st.metric("Prediction Confidence", "Not available")

            st.caption(
                "Confidence is the model's probability for its most likely "
                "Kaggle dataset category. It is not the probability that a "
                "student has a mental-health condition."
            )

            st.subheader("Seven-Category Probability Analysis")

            probability_df = px.data.frame if False else None
            probability_figure = px.bar(
                x=list(probabilities.keys()),
                y=list(probabilities.values()),
                labels={
                    "x": "Dataset Category",
                    "y": "Model Probability (%)"
                },
                text=[f"{value:.1f}%" for value in probabilities.values()]
            )

            probability_figure.update_traces(
                marker_color="#38bdf8",
                textposition="outside",
                cliponaxis=False
            )

            probability_figure.update_layout(
                paper_bgcolor="#0b1120",
                plot_bgcolor="#162238",
                font={"color": "white"},
                xaxis_title="Dataset Category",
                yaxis_title="Model Probability (%)",
                yaxis={
                    "range": [0, min(115, max(10, max(probabilities.values()) + 12))]
                },
                height=420,
                margin={"t": 35, "b": 80}
            )

            st.plotly_chart(
                probability_figure,
                use_container_width=True
            )

        else:
            st.info(
                "Submit a written reflection of at least 8 characters "
                "to view the NLP category prediction and probability chart."
            )

        st.subheader("Visual Analysis")

        figure = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=result["final"],
                number={"suffix": "/100"},
                title={"text": "Prototype Awareness Indicator"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#38bdf8"},
                    "bgcolor": "#162238",
                    "bordercolor": "#293b59",
                    "steps": [
                        {"range": [0, 35], "color": "#1e3a5f"},
                        {"range": [35, 70], "color": "#334155"},
                        {"range": [70, 100], "color": "#475569"}
                    ]
                }
            )
        )

        figure.update_layout(
            height=320,
            paper_bgcolor="#0b1120",
            font={"color": "white"}
        )

        st.plotly_chart(
            figure,
            use_container_width=True
        )

        st.subheader("Supportive Suggestions")

        for tip in guidance(result["label"]):
            st.write("• " + tip)

        st.warning(
            "These are experimental software indicators, not clinical "
            "scores or probabilities. If you are concerned about your "
            "wellbeing, consider speaking with a qualified professional."
        )

        if st.button("Clear Current Assessment"):
            st.session_state.result = None
            st.rerun()


# --------------------------------------------------
# PHOTO ANALYSIS
# --------------------------------------------------

elif page == "Photo Analysis":

    show_hero(
        "📷 Facial Landmark Analysis",
        "Visualize facial landmarks using MediaPipe Face Mesh."
    )

    st.warning(
        "Facial landmarks show geometric facial features only. "
        "They cannot reliably identify emotions, stress, depression, "
        "anxiety or mental-health conditions."
    )

    st.subheader("Capture Your Photograph")

    photo = st.camera_input(
        "Take a photograph using your webcam"
    )

    if photo is not None:

        try:

            with st.spinner("Detecting facial landmarks..."):

                result = analyze_photo(photo.getvalue())

            st.divider()

            st.subheader("Facial Analysis Result")

            col1, col2 = st.columns([2, 1])

            with col1:
                st.image(
                    result["image"],
                    caption="Detected Facial Landmarks",
                    use_column_width=True
                )

            with col2:

                st.metric(
                    "Faces Detected",
                    result["faces"]
                )

                if result["faces"] > 0:
                    st.success("Face landmarks detected successfully.")
                else:
                    st.warning(
                        "No face detected. Try better lighting "
                        "and face the camera."
                    )

            st.info(
                "The displayed points represent facial landmarks. "
                "They are not measurements of mental health and "
                "are not included in the wellbeing score."
            )

        except Exception as error:

            st.error(f"Face analysis error: {error}")

    st.caption(
        "Only a captured still photograph is processed. "
        "The application does not intentionally save the photo "
        "or record continuous webcam video."
    )


# --------------------------------------------------
# ASSESSMENT HISTORY
# --------------------------------------------------

elif page == "Assessment History":

    show_hero(
        "📈 Assessment History",
        "Review assessment indicators recorded during this session."
    )

    history = st.session_state.history

    if history:

        st.metric(
            "Total Assessments",
            len(history)
        )

        st.subheader("Indicator Progress")

        figure = px.line(
            x=list(range(1, len(history) + 1)),
            y=[item["score"] for item in history],
            markers=True,
            labels={
                "x": "Assessment Number",
                "y": "Awareness Indicator"
            }
        )

        figure.update_layout(
            paper_bgcolor="#0b1120",
            plot_bgcolor="#162238",
            font={"color": "white"},
            yaxis={"range": [0, 100]},
            height=350
        )

        figure.update_traces(
            line={"color": "#38bdf8", "width": 3},
            marker={"size": 9}
        )

        st.plotly_chart(
            figure,
            use_container_width=True
        )

        st.subheader("Previous Assessments")

        for i, item in enumerate(reversed(history), start=1):

            with st.expander(
                f"Assessment {len(history) - i + 1} — {item['time']}"
            ):

                st.metric(
                    "Awareness Indicator",
                    f"{item['score']:.1f}/100",
                    item["label"]
                )

        if st.button("Clear Assessment History"):
            st.session_state.history = []
            st.session_state.result = None
            st.rerun()

    else:

        st.info(
            "No assessment history is available yet. "
            "Complete a wellbeing assessment to see your progress here."
        )

    st.caption(
        "History is temporary and is cleared when the application session ends."
    )


# --------------------------------------------------
# ABOUT PROJECT
# --------------------------------------------------

elif page == "About Project":

    show_hero(
        "ℹ️ About Our Project",
        "Multimodal AI for Early Detection of Student Mental Health Disorders."
    )

    st.subheader("Technologies Used")

    technologies = [
        "Python",
        "Streamlit",
        "Pandas",
        "Scikit-learn",
        "TF-IDF",
        "Logistic Regression",
        "MediaPipe Face Mesh",
        "OpenCV",
        "Plotly"
    ]

    col1, col2, col3 = st.columns(3)

    for i, technology in enumerate(technologies):

        with [col1, col2, col3][i % 3]:
            st.markdown(
                f"""
                <div class="card">
                    <h3>✓ {technology}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    st.subheader("Project Architecture")

    st.code("""
    Questionnaire
          |
          v
    Questionnaire Indicator

    Written Text
          |
          v
    TF-IDF + Logistic Regression
          |
          v
    Language Pattern Indicator

    Webcam Photograph
          |
          v
    MediaPipe Face Mesh
          |
          v
    Facial Landmark Visualization

    Questionnaire + Text
          |
          v
    Combined Awareness Dashboard
    """, language="text")

    st.subheader("Research Limitations")

    st.write("1. The questionnaire is custom-made and not clinically validated.")

    st.write("2. The NLP model is trained on a Kaggle dataset with seven dataset labels; its classifications are not clinical diagnoses.")

    st.write("3. Facial landmarks cannot establish mental-health conditions.")

    st.write("4. Face analysis is kept separate from the wellbeing indicator.")

    st.write(
        "5. Real-world research requires informed consent, "
        "ethics approval, privacy safeguards and professional oversight."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Student Wellbeing AI · Version 5.0 · "
    "Academic Research Prototype · No Medical Diagnosis"
)
