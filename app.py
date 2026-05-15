import streamlit as st
import pandas as pd
import numpy as np
import joblib


# ── PAGE CONFIG ──
st.set_page_config(
    page_title="Mental Health AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── LOAD MODEL ──
model  = joblib.load("model.pkl")
labels = joblib.load("labels.pkl")

# ── THEME STATE ──
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# ── TOGGLE BUTTON (top-right) ──
_, _, toggle_col = st.columns([6, 1, 1])
with toggle_col:
    is_dark = st.session_state.theme == "dark"
    label   = "☀  Light" if is_dark else "🌙  Dark"
    if st.button(label, key="theme_toggle"):
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()

is_dark = st.session_state.theme == "dark"

# ── CSS VARIABLES PER THEME ──
if is_dark:
    theme_vars = """
        --gold:           #C9A84C;
        --gold-light:     #E8D5A3;
        --gold-dim:       #7a6130;
        --accent-glow:    rgba(201,168,76,0.12);
        --bg-deep:        #080C14;
        --bg-card:        #0E1420;
        --bg-card2:       #111826;
        --bg-input:       #111826;
        --bg-popover:     #141B28;
        --border:         rgba(201,168,76,0.18);
        --border-glow:    rgba(201,168,76,0.45);
        --text-main:      #E8E4DC;
        --text-muted:     #8A8F9E;
        --text-label:     #B0B8CC;
        --text-option:    #B0B8CC;
        --prob-track-bg:  rgba(255,255,255,0.06);
        --radial-1:       rgba(201,168,76,0.07);
        --radial-2:       rgba(30,60,120,0.18);
    """
else:
    theme_vars = """
        --gold:           #8B6914;
        --gold-light:     #6B4F0A;
        --gold-dim:       #A07820;
        --accent-glow:    rgba(139,105,20,0.10);
        --bg-deep:        #F5F3EE;
        --bg-card:        #FFFFFF;
        --bg-card2:       #FAF8F4;
        --bg-input:       #FAF8F4;
        --bg-popover:     #FFFFFF;
        --border:         rgba(139,105,20,0.20);
        --border-glow:    rgba(139,105,20,0.50);
        --text-main:      #1A1612;
        --text-muted:     #6B6560;
        --text-label:     #4A4540;
        --text-option:    #3A3530;
        --prob-track-bg:  rgba(0,0,0,0.07);
        --radial-1:       rgba(201,168,76,0.09);
        --radial-2:       rgba(100,140,220,0.07);
    """

# ── INJECT CSS ──
st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Sans:wght@300;400;500&display=swap');

:root {{
    {theme_vars}
}}

/* ── RESET / BASE ── */
*, *::before, *::after {{ box-sizing: border-box; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{
    padding: 0.5rem 3rem 4rem !important;
    max-width: 1320px !important;
}}

/* ── APP BG ── */
.stApp {{
    background-color: var(--bg-deep);
    background-image:
        radial-gradient(ellipse 70% 50% at 20% 0%, var(--radial-1) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 80% 100%, var(--radial-2) 0%, transparent 60%);
    font-family: 'DM Sans', sans-serif;
    color: var(--text-main);
    transition: background-color 0.4s ease, color 0.4s ease;
}}

/* ── THEME TOGGLE BUTTON ── */
div[data-testid="column"]:last-child .stButton > button {{
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--gold) !important;
    border-radius: 20px !important;
    height: 34px !important;
    font-size: 11px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    letter-spacing: 2px !important;
    padding: 0 16px !important;
    width: auto !important;
    transition: all 0.25s ease !important;
}}
div[data-testid="column"]:last-child .stButton > button:hover {{
    background: var(--accent-glow) !important;
    border-color: var(--gold) !important;
    transform: none !important;
    box-shadow: none !important;
}}

/* ── HEADER ── */
.luxury-header {{
    text-align: center;
    padding: 2rem 0 2.5rem;
}}
.luxury-header::before {{
    content: '';
    display: block;
    width: 1px;
    height: 50px;
    background: linear-gradient(to bottom, transparent, var(--gold));
    margin: 0 auto 1.6rem;
}}
.luxury-eyebrow {{
    font-family: 'DM Sans', sans-serif;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 6px;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 1rem;
}}
.luxury-title {{
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(40px, 5vw, 66px);
    font-weight: 300;
    color: var(--text-main);
    line-height: 1.1;
    letter-spacing: -1px;
    margin-bottom: 0.8rem;
}}
.luxury-title em {{
    font-style: italic;
    color: var(--gold);
}}
.luxury-subtitle {{
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    font-weight: 300;
    color: var(--text-muted);
    letter-spacing: 0.8px;
}}
.header-rule {{
    width: 80px;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--gold), transparent);
    margin: 1.4rem auto 0;
}}

/* ── SECTION DIVIDER ── */
.section-divider {{
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 2rem 0 1.5rem;
}}
.section-divider span {{
    font-family: 'DM Sans', sans-serif;
    font-size: 9px;
    font-weight: 500;
    letter-spacing: 5px;
    text-transform: uppercase;
    color: var(--gold-dim);
    white-space: nowrap;
}}
.section-divider::before,
.section-divider::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}}

/* ── STREAMLIT WIDGETS ── */
div[data-baseweb="select"] > div {{
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 3px !important;
    color: var(--text-main) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    transition: border-color 0.2s;
}}
div[data-baseweb="select"] > div:focus-within {{
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.12) !important;
}}
div[data-baseweb="popover"] {{
    background: var(--bg-popover) !important;
    border: 1px solid var(--border) !important;
}}
li[role="option"] {{
    color: var(--text-option) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    background: var(--bg-popover) !important;
}}
li[role="option"]:hover {{
    background: var(--accent-glow) !important;
    color: var(--gold) !important;
}}

.stSelectbox label,
.stSlider label {{
    font-family: 'DM Sans', sans-serif !important;
    font-size: 12px !important;
    font-weight: 400 !important;
    color: var(--text-label) !important;
    letter-spacing: 0.3px !important;
}}

div[data-testid="stSlider"] div[role="slider"] {{
    background: var(--gold) !important;
    border: none !important;
    width: 14px !important;
    height: 14px !important;
    box-shadow: 0 0 8px var(--accent-glow) !important;
}}
div[data-testid="stSlider"] > div > div > div {{
    background: var(--border) !important;
}}
div[data-testid="stSlider"] > div > div > div > div {{
    background: var(--gold) !important;
}}

h3 {{
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 22px !important;
    font-weight: 400 !important;
    color: var(--text-main) !important;
    letter-spacing: 0.2px !important;
    margin-bottom: 1.2rem !important;
    padding-bottom: 0.6rem !important;
    border-bottom: 1px solid var(--border) !important;
}}

/* ── PREDICT BUTTON (main) ── */
div[data-testid="column"].predict-col .stButton > button,
.predict-wrap .stButton > button {{
    width: 100%;
    background: transparent;
    color: var(--gold);
    border: 1px solid var(--gold-dim);
    border-radius: 3px;
    height: 54px;
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 5px;
    text-transform: uppercase;
    transition: all 0.3s ease;
    margin-top: 0.5rem;
}}

/* generic fallback for predict button — applied by key targeting */
button[kind="secondary"] {{
    background: transparent !important;
    color: var(--gold) !important;
    border: 1px solid var(--gold-dim) !important;
    border-radius: 3px !important;
    height: 54px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 5px !important;
    text-transform: uppercase !important;
}}
button[kind="secondary"]:hover {{
    background: var(--accent-glow) !important;
    border-color: var(--gold) !important;
    color: var(--gold-light) !important;
}}

/* ── RESULT BOX ── */
.result-luxury {{
    background: var(--bg-card);
    border: 1px solid var(--border-glow);
    border-radius: 4px;
    padding: 3rem 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin: 1.5rem 0;
    transition: background 0.4s, border-color 0.4s;
}}
.result-luxury::before {{
    content: '';
    position: absolute;
    top: -80px; left: 50%;
    transform: translateX(-50%);
    width: 300px; height: 160px;
    background: radial-gradient(ellipse, var(--accent-glow) 0%, transparent 70%);
    pointer-events: none;
}}
.result-luxury::after {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--gold), transparent);
}}
.result-eyebrow {{
    font-family: 'DM Sans', sans-serif;
    font-size: 9px;
    letter-spacing: 6px;
    text-transform: uppercase;
    color: var(--gold-dim);
    margin-bottom: 1rem;
}}
.result-diagnosis {{
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(30px, 4vw, 50px);
    font-weight: 300;
    color: var(--gold-light);
    letter-spacing: -0.5px;
    line-height: 1.2;
    margin-bottom: 0.5rem;
}}
.result-rule {{
    width: 50px;
    height: 1px;
    background: var(--gold-dim);
    margin: 1.2rem auto 0;
}}

/* ── PROBABILITY BARS ── */
.prob-row {{ margin: 1rem 0; }}
.prob-meta {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 6px;
}}
.prob-name {{
    font-family: 'DM Sans', sans-serif;
    font-size: 12px;
    font-weight: 400;
    color: var(--text-label);
    letter-spacing: 0.2px;
}}
.prob-pct {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 16px;
    font-weight: 300;
    color: var(--gold);
}}
.prob-track {{
    height: 3px;
    background: var(--prob-track-bg);
    border-radius: 2px;
    overflow: hidden;
}}
.prob-fill {{
    height: 100%;
    border-radius: 2px;
    background: linear-gradient(to right, var(--gold-dim), var(--gold));
}}

/* ── FOOTER ── */
.footer-luxury {{
    text-align: center;
    margin-top: 4rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border);
}}
.footer-luxury::before {{
    content: '⚕';
    display: block;
    font-size: 18px;
    color: var(--gold-dim);
    margin-bottom: 0.8rem;
}}
.footer-luxury p {{
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    color: var(--text-muted);
    letter-spacing: 0.5px;
    line-height: 1.8;
}}

</style>
""", unsafe_allow_html=True)

# ── HEADER ──
st.markdown("""
<div class="luxury-header">
    <div class="luxury-eyebrow">Clinical Intelligence System</div>
    <div class="luxury-title">Mental Health <em>Diagnostics</em></div>
    <div class="luxury-subtitle">AI-powered psychiatric disorder classification — for research & educational use</div>
    <div class="header-rule"></div>
</div>
""", unsafe_allow_html=True)

# INPUT MAPPINGS
freq_map   = {"Seldom": 0, "Sometimes": 1, "Usually": 2, "Most-Often": 3}
yes_no_map = {"No": 0, "Yes": 1}

# ── 3-COLUMN FORM ──
col1, col2, col3 = st.columns([1, 1, 1], gap="large")

with col1:
    st.subheader("Emotional Symptoms")
    sadness      = st.selectbox("Sadness · الحزن",                      list(freq_map.keys()))
    euphoric     = st.selectbox("Euphoric Mood · المزاج الابتهاجي",     list(freq_map.keys()))
    exhausted    = st.selectbox("Exhaustion · الإرهاق",                  list(freq_map.keys()))
    sleep        = st.selectbox("Sleep Disorder · اضطراب النوم",         list(freq_map.keys()))

with col2:
    st.subheader("Behavioral Symptoms")
    mood         = st.selectbox("Mood Swing · تقلبات المزاج",            list(yes_no_map.keys()))
    suicidal     = st.selectbox("Suicidal Thoughts · أفكار انتحارية",    list(yes_no_map.keys()))
    anorexia     = st.selectbox("Anorexia · فقدان الشهية",               list(yes_no_map.keys()))
    nervous      = st.selectbox("Nervous Breakdown · انهيار عصبي",       list(yes_no_map.keys()))
    overthinking = st.selectbox("Overthinking · التفكير المفرط",         list(yes_no_map.keys()))

with col3:
    st.subheader("Cognitive Scores")
    concentration = st.slider("Concentration · التركيز",         1, 10, 5)
    optimism      = st.slider("Optimism · الأمل",                1, 10, 5)
    sexual        = st.slider("Sexual Activity · النشاط الجنسي", 1, 10, 5)

# ── PREDICT BUTTON ──
st.markdown("<br>", unsafe_allow_html=True)
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    predict_button = st.button("◆  Run Diagnostic Analysis", key="predict_btn", type="secondary")

# ── PREDICTION ──
if predict_button:

    data = {
        "Sadness":             freq_map[sadness],
        "Euphoric":            freq_map[euphoric],
        "Exhausted":           freq_map[exhausted],
        "Sleep Disorder":      freq_map[sleep],
        "Mood Swing":          yes_no_map[mood],
        "Suicidal thoughts":   yes_no_map[suicidal],
        "Anorexia":            yes_no_map[anorexia],
        "Authority Respect":   1,
        "Try-Explanation":     1,
        "Aggressive Response": 0,
        "Ignore & Move-On":    1,
        "Nervous Break-down":  yes_no_map[nervous],
        "Admit Mistakes":      1,
        "Overthinking":        yes_no_map[overthinking],
        "Sexual Activity":     sexual,
        "Concentration":       concentration,
        "Optimism":            optimism,
    }

    input_df = pd.DataFrame([data])

    cols_freq   = ["Sadness","Euphoric","Exhausted","Sleep Disorder"]
    cols_binary = ["Mood Swing","Suicidal thoughts","Anorexia","Authority Respect",
                   "Try-Explanation","Aggressive Response","Ignore & Move-On",
                   "Nervous Break-down","Admit Mistakes","Overthinking"]
    score_cols  = ["Sexual Activity","Concentration","Optimism"]

    input_df["Mental_scr"]    = input_df[cols_freq].sum(axis=1)
    input_df["Emotional_scr"] = input_df[cols_binary].sum(axis=1)
    input_df["Behavior_scr"]  = input_df[score_cols].sum(axis=1)

    prediction      = model.predict(input_df)[0]
    probabilities   = model.predict_proba(input_df)[0]
    predicted_label = labels[prediction]

    # ── RESULT ──
    st.markdown(f"""
    <div class="result-luxury">
        <div class="result-eyebrow">Diagnostic Result</div>
        <div class="result-diagnosis">{predicted_label}</div>
        <div class="result-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    # ── PROBABILITY BARS ──
    st.markdown('<div class="section-divider"><span>Probability Distribution</span></div>', unsafe_allow_html=True)

    disorder_names = [
        "Bipolar Disorder — Type I",
        "Bipolar Disorder — Type II",
        "Clinical Depression",
        "Within Normal Range",
    ]

    for i, prob in enumerate(probabilities):
        name = disorder_names[i] if i < len(disorder_names) else labels[i]
        pct  = prob * 100
        st.markdown(f"""
        <div class="prob-row">
            <div class="prob-meta">
                <span class="prob-name">{name}</span>
                <span class="prob-pct">{pct:.1f}%</span>
            </div>
            <div class="prob-track">
                <div class="prob-fill" style="width:{pct}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("""
<div class="footer-luxury">
    <p>
        This system is designed strictly for educational and research purposes.<br>
        It does not constitute, replace, or supplement professional psychiatric evaluation or diagnosis.
    </p>
</div>
""", unsafe_allow_html=True)