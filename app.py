import streamlit as st
import pandas as pd
import numpy as np
import joblib


# PAGE CONFIG
st.set_page_config(
    page_title="Mental Health AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# LOAD MODEL
model = joblib.load("model.pkl")
labels = joblib.load("labels.pkl")

# CUSTOM CSS
st.markdown("""
<style>

/* Main Background */

.stApp {
    background: linear-gradient(to right, #f4f7fb, #e9f0ff);
    font-family: 'Segoe UI', sans-serif;
}

/* Header */

.main-title {
    font-size: 52px;
    font-weight: 700;
    color: #0b3d91;
    text-align: center;
    margin-bottom: 10px;
}

.sub-title {
    text-align: center;
    color: #4a5568;
    font-size: 18px;
    margin-bottom: 40px;
}


/* Prediction Box */

.result-box {
    padding: 30px;
    border-radius: 20px;
    background: linear-gradient(135deg, #0b3d91, #2563eb);
    color: white;
    text-align: center;
    box-shadow: 0px 5px 25px rgba(0,0,0,0.15);
}

/* Button */

.stButton > button {
    width: 100%;
    background: linear-gradient(to right, #0b3d91, #2563eb);
    color: white;
    border-radius: 12px;
    height: 55px;
    font-size: 18px;
    border: none;
    font-weight: bold;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.02);
    background: linear-gradient(to right, #2563eb, #0b3d91);
}

/* Slider */

.stSlider {
    padding-top: 10px;
}

/* Footer */

.footer {
    text-align: center;
    margin-top: 50px;
    color: gray;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown(
    '<div class="main-title"> Mental Health Disorder Prediction</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">AI-powered psychiatric disorder classification system</div>',
    unsafe_allow_html=True
)

# INPUT MAPPINGS
freq_map = {
    "Seldom": 0,
    "Sometimes": 1,
    "Usually": 2,
    "Most-Often": 3
}

yes_no_map = {
    "No": 0,
    "Yes": 1
}

# LAYOUT
col1, col2, col3 = st.columns(3)


# COLUMN 1
with col1:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Emotional Symptoms")

    sadness = st.selectbox(
        "Sadness: الحزن",
        list(freq_map.keys())
    )

    euphoric = st.selectbox(
        "Euphoric Mood: المزاج الابتهاجي",
        list(freq_map.keys())
    )

    exhausted = st.selectbox(
        "Exhaustion: الإرهاق",
        list(freq_map.keys())
    )

    sleep = st.selectbox(
        "Sleep Disorder: اضطراب النوم",
        list(freq_map.keys())
    )

    st.markdown('</div>', unsafe_allow_html=True)


# COLUMN 2
with col2:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Behavioral Symptoms")

    mood = st.selectbox(
        "Mood Swing: تقلبات المزاج",
        list(yes_no_map.keys())
    )

    suicidal = st.selectbox(
        "Suicidal Thoughts: أفكار انتحارية",
        list(yes_no_map.keys())
    )

    anorexia = st.selectbox(
        "Anorexia: فقدان الشهية",
        list(yes_no_map.keys())
    )

    nervous = st.selectbox(
        "Nervous Breakdown: انهيار عصبي",
        list(yes_no_map.keys())
    )

    overthinking = st.selectbox(
        "Overthinking: التفكير المفرط",
        list(yes_no_map.keys())
    )

    st.markdown('</div>', unsafe_allow_html=True)

# COLUMN 3
with col3:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Cognitive Scores")

    concentration = st.slider(
        "Concentration: التركيز",
        1, 10, 5
    )

    optimism = st.slider(
        "Optimism: الأمل",
        1, 10, 5
    )

    sexual = st.slider(
        "Sexual Activity: النشاط الجنسي",
        1, 10, 5
    )

    st.markdown('</div>', unsafe_allow_html=True)


# PREDICTION BUTTON
predict_button = st.button("Predict Diagnosis")


# PREDICTION
if predict_button:

    data = {

        "Sadness":
            freq_map[sadness],

        "Euphoric":
            freq_map[euphoric],

        "Exhausted":
            freq_map[exhausted],

        "Sleep Disorder":
            freq_map[sleep],

        "Mood Swing":
            yes_no_map[mood],

        "Suicidal thoughts":
            yes_no_map[suicidal],

        "Anorexia":
            yes_no_map[anorexia],

        "Authority Respect":
            1,

        "Try-Explanation":
            1,

        "Aggressive Response":
            0,

        "Ignore & Move-On":
            1,

        "Nervous Break-down":
            yes_no_map[nervous],

        "Admit Mistakes":
            1,

        "Overthinking":
            yes_no_map[overthinking],

        "Sexual Activity":
            sexual,

        "Concentration":
            concentration,

        "Optimism":
            optimism
    }

    input_df = pd.DataFrame([data])

    # FEATURE ENGINEERING
    cols_freq = [
        "Sadness",
        "Euphoric",
        "Exhausted",
        "Sleep Disorder"
    ]

    cols_binary = [
        "Mood Swing",
        "Suicidal thoughts",
        "Anorexia",
        "Authority Respect",
        "Try-Explanation",
        "Aggressive Response",
        "Ignore & Move-On",
        "Nervous Break-down",
        "Admit Mistakes",
        "Overthinking"
    ]

    score_cols = [
        "Sexual Activity",
        "Concentration",
        "Optimism"
    ]

    input_df["Mental_scr"] = input_df[cols_freq].sum(axis=1)

    input_df["Emotional_scr"] = input_df[cols_binary].sum(axis=1)

    input_df["Behavior_scr"] = input_df[score_cols].sum(axis=1)

    # PREDICTION
    prediction = model.predict(input_df)[0]

    probabilities = model.predict_proba(input_df)[0]

    predicted_label = labels[prediction]

    # RESULT DISPLAY
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="result-box">
            <h2>Prediction Result</h2>
            <h1>{predicted_label}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # PROBABILITIES
    st.subheader("Prediction Probabilities")

    for i, prob in enumerate(probabilities):

        label = labels[i]

    # labels médicaux
        if i == 0:
            name = "Trouble bipolaire de type 1"
        elif i == 1:
            name = "Trouble bipolaire de type 2"
        elif i == 2:
            name = "Dépression"
        else:
            name = "Normal"

        # ligne style flex (nom + barre)
        col_a, col_b = st.columns([3, 7])

        with col_a:
            st.markdown(f"**{name}**")

        with col_b:
            st.progress(float(prob))
            st.caption(f"{prob*100:.2f}%")


# DISCLAIMER
st.markdown("""
<div class="footer">

 This AI system is intended for educational and research purposes only.
It does not replace professional psychiatric diagnosis.

</div>
""", unsafe_allow_html=True)