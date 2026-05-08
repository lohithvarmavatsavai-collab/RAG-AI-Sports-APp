import streamlit as st
import os
import sys

# ── page config must be first ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI Sports Performance Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── make sure imports can find sibling modules ─────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))
import importlib
import retrieve as retrieve_mod
import generate as generate_mod
importlib.reload(retrieve_mod)
importlib.reload(generate_mod)
from retrieve import retrieve
from generate import get_rag_answer, get_baseline_answer

# ══════════════════════════════════════════════════════════════════════════
# PROFILE INSIGHTS — instant, zero-token data shown when profile changes
# ══════════════════════════════════════════════════════════════════════════
PROFILE_INSIGHTS = {
    "Soccer": {
        "icon": "⚽",
        "protein": "1.4–1.7 g/kg/day",
        "carbs_training": "5–7 g/kg (training day)",
        "carbs_match": "7–10 g/kg (match day)",
        "hydration": "400–600 mL pre-match; 150–250 mL every 15–20 min during",
        "sleep": "8–9 hours; nap 20–30 min on match days",
        "sessions": {"Beginner (< 1 year)": "2–3 sessions/week, 60 min each",
                     "Intermediate (1–3 years)": "4–5 sessions/week incl. 1 match",
                     "Advanced (3+ years)": "5–6 sessions/week with structured periodization"},
        "key_orgs": "FIFA, UEFA, F-MARC, ACSM, ISSN, GSSI",
        "acwr_tip": "Keep Acute:Chronic Workload Ratio between 0.8–1.3 to stay injury-free (FIFA)",
    },
    "Tennis": {
        "icon": "🎾",
        "protein": "1.5–1.8 g/kg/day",
        "carbs_training": "5–8 g/kg (training day)",
        "carbs_match": "7–10 g/kg (match day >90 min: 30–60 g/hr intra-match)",
        "hydration": "150–200 mL every changeover; ice towel in heat",
        "sleep": "8–9 hours; 20-min nap before afternoon matches",
        "sessions": {"Beginner (< 1 year)": "2–3 sessions/week, skill-focused",
                     "Intermediate (1–3 years)": "4–5 sessions/week + 1 strength session",
                     "Advanced (3+ years)": "5–6 sessions with ATP/WTA periodization"},
        "key_orgs": "ITF, USTA, ATP/WTA, USOPC, BJSM, ITF Medical Commission",
        "acwr_tip": "Split-step timing and explosive first 3 steps determine 80% of court positioning (ATP)",
    },
    "Basketball": {
        "icon": "🏀",
        "protein": "1.6–2.0 g/kg/day",
        "carbs_training": "5–7 g/kg (training day)",
        "carbs_match": "7–10 g/kg (game day)",
        "hydration": "150–250 mL every timeout; 1.5 L per kg lost post-game",
        "sleep": "8–10 hours; Stanford study: sleep extension improved free throw % by 9.2%",
        "sessions": {"Beginner (< 1 year)": "2–3 sessions/week, skill + light conditioning",
                     "Intermediate (1–3 years)": "4–5 sessions/week + 2 strength sessions",
                     "Advanced (3+ years)": "5–6 sessions with NBA-style load management"},
        "key_orgs": "FIBA, NBA Academy, NBA Performance Lab, NCAA, NBPA, ACSM, GSSI",
        "acwr_tip": "CMJ drop >5% signals incomplete recovery — reduce intensity that day (NBA Performance Lab)",
    },
    "Strength Training": {
        "icon": "🏋️",
        "protein": "1.6–2.2 g/kg/day (up to 2.4 g/kg when in caloric deficit)",
        "carbs_training": "3–5 g/kg/day; 0.5–1.0 g/kg pre-workout",
        "carbs_match": "Post-workout: 0.5–1.0 g/kg within 2 hours",
        "hydration": "Pale yellow urine daily; 500 mL pre-workout minimum",
        "sleep": "8+ hours — GH secretion during deep sleep drives muscle repair",
        "sessions": {"Beginner (< 1 year)": "2–3 full-body sessions/week (Mon/Wed/Fri)",
                     "Intermediate (1–3 years)": "3–4 sessions/week (upper/lower split)",
                     "Advanced (3+ years)": "4–5 sessions with periodized programming"},
        "key_orgs": "NSCA, ACSM, ISSN, NIH, USDA/AND, JSCR",
        "acwr_tip": "Deload every 4–8 weeks: cut volume 50%, keep intensity. Post-deload strength exceeds pre-deload (ACSM)",
    },
}

GOAL_TIPS = {
    "Improve Performance": "Focus on sport-specific conditioning and progressive overload in training.",
    "Build Strength": "Prioritize compound lifts (squat, hinge, press, pull) 2–3x/week with linear progression.",
    "Improve Endurance": "Build aerobic base first (Zone 2, 65–75% HRmax), then add intervals.",
    "Lose Weight / Lean Out": "Maintain protein at 2.0–2.4 g/kg to preserve muscle. Max 500 kcal/day deficit.",
    "General Fitness": "3 days/week of mixed training (2 strength + 1 conditioning) is sufficient for health.",
    "Faster Recovery": "Sleep is #1. Add: cold water immersion post-session, 25 g protein within 2 hrs, active recovery next day.",
}


# ══════════════════════════════════════════════════════════════════════════
# STYLING
# ══════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Dark gradient background ── */
.stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    min-height: 100vh;
}
/* Force text in main area to be readable light gray */
[data-testid="stMainBlockContainer"] p,
[data-testid="stMainBlockContainer"] li,
[data-testid="stMainBlockContainer"] h1,
[data-testid="stMainBlockContainer"] h2,
[data-testid="stMainBlockContainer"] h3,
[data-testid="stMainBlockContainer"] h4,
[data-testid="stMainBlockContainer"] span,
[data-testid="stMainBlockContainer"] strong,
[data-testid="stMainBlockContainer"] blockquote {
    color: #e2e8f0 !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebar"] * { color: #e0e0f0 !important; }

/* ── Header hero ── */
.hero-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(102,126,234,0.35);
}
.hero-header h1 {
    font-size: 2.2rem;
    font-weight: 700;
    color: white;
    margin: 0;
    text-shadow: 0 2px 8px rgba(0,0,0,0.3);
}
.hero-header p {
    color: rgba(255,255,255,0.85);
    margin: 0.5rem 0 0 0;
    font-size: 1rem;
}

/* ── Cards ── */
.card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 14px;
    padding: 1.4rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
    transition: border-color 0.2s ease;
}
.card:hover { border-color: rgba(102,126,234,0.5); }

/* ── Section label badges ── */
.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.badge-rag   { background: rgba(102,126,234,0.25); color: #a5b4fc; border: 1px solid rgba(102,126,234,0.4); }
.badge-base  { background: rgba(249,115,22,0.20);  color: #fb923c; border: 1px solid rgba(249,115,22,0.4); }
.badge-src   { background: rgba(16,185,129,0.20);  color: #6ee7b7; border: 1px solid rgba(16,185,129,0.4); }
.badge-warn  { background: rgba(239,68,68,0.15);   color: #fca5a5; border: 1px solid rgba(239,68,68,0.35); }

/* ── Source chips ── */
.source-chip {
    display: inline-block;
    background: rgba(16,185,129,0.15);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 0.78rem;
    color: #6ee7b7;
    margin: 4px 4px 4px 0;
    line-height: 1.4;
}

/* ── Answer text ── */
.answer-box {
    background: rgba(255,255,255,0.03);
    border-left: 3px solid #667eea;
    border-radius: 0 10px 10px 0;
    padding: 1.2rem 1.4rem;
    color: #d1d5db;
    line-height: 1.7;
    font-size: 0.92rem;
}
.answer-box-base {
    background: rgba(255,255,255,0.03);
    border-left: 3px solid #f97316;
    border-radius: 0 10px 10px 0;
    padding: 1.2rem 1.4rem;
    color: #d1d5db;
    line-height: 1.7;
    font-size: 0.92rem;
}

/* ── Warning box ── */
.warning-box {
    background: rgba(239,68,68,0.10);
    border: 1px solid rgba(239,68,68,0.30);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: #fca5a5;
    font-size: 0.87rem;
    margin-top: 1rem;
}

/* ── Step label ── */
.step-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #9ca3af;
    margin-bottom: 0.3rem;
}

/* ── Metric boxes ── */
.metric-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
}
.metric-box {
    flex: 1;
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
}
.metric-box .num { font-size: 1.8rem; font-weight: 700; color: #a5b4fc; }
.metric-box .lbl { font-size: 0.75rem; color: #9ca3af; margin-top: 2px; }

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.08) !important; }

/* ── Profile stat cards ── */
.stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 6px 0 10px 0; }
.stat-card {
    background: rgba(102,126,234,0.12);
    border: 1px solid rgba(102,126,234,0.25);
    border-radius: 10px;
    padding: 8px 10px;
    text-align: center;
}
.stat-card .sc-label { font-size: 0.65rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 3px; }
.stat-card .sc-value { font-size: 0.82rem; color: #c7d2fe; font-weight: 600; line-height: 1.3; }
.stat-card-wide {
    background: rgba(16,185,129,0.10);
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 10px;
    padding: 8px 10px;
    margin-bottom: 6px;
}
.stat-card-wide .sc-label { font-size: 0.65rem; color: #6ee7b7; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px; }
.stat-card-wide .sc-value { font-size: 0.80rem; color: #a7f3d0; font-weight: 500; line-height: 1.4; }
.protein-pill {
    background: linear-gradient(135deg, rgba(102,126,234,0.3), rgba(118,75,162,0.3));
    border: 1px solid rgba(165,180,252,0.4);
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 8px;
    text-align: center;
}
.protein-pill .pp-label { font-size: 0.65rem; color: #a5b4fc; text-transform: uppercase; letter-spacing: 0.08em; }
.protein-pill .pp-value { font-size: 1.1rem; color: #e0e7ff; font-weight: 700; margin-top: 2px; }

/* ── Answer container — use st.markdown, style the wrapper ── */
.answer-wrapper-rag {
    border-left: 3px solid #667eea;
    padding-left: 1rem;
    margin-top: 0.5rem;
}
.answer-wrapper-base {
    border-left: 3px solid #f97316;
    padding-left: 1rem;
    margin-top: 0.5rem;
}

/* ── Streamlit widget overrides ── */
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stTextArea"] label { color: #d1d5db !important; font-size: 0.88rem !important; }

/* Dark text for sidebar inputs to be readable on their white backgrounds */
[data-testid="stSidebar"] div[data-baseweb="select"] *,
[data-testid="stSidebar"] div[data-baseweb="base-input"] *,
[data-testid="stSidebar"] input {
    color: #111827 !important;
}


/* ── Sport card radio selector ── */
div[data-testid="stRadio"]:has(div[aria-label="Sport"]) > label {
    color: #d1d5db !important;
    font-size: 0.80rem !important;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
div[data-testid="stRadio"]:has(div[aria-label="Sport"]) div[role="radiogroup"] {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 8px !important;
    margin-top: 4px;
}
div[data-testid="stRadio"]:has(div[aria-label="Sport"]) div[role="radiogroup"] label {
    background: rgba(255,255,255,0.04) !important;
    border: 1.5px solid rgba(102,126,234,0.20) !important;
    border-radius: 12px !important;
    padding: 10px 4px !important;
    text-align: center !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    color: #9ca3af !important;
    font-size: 0.68rem !important;
    font-weight: 500 !important;
    text-transform: none !important;
    letter-spacing: normal !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    gap: 4px !important;
    height: 70px !important;
    justify-content: center !important;
}
div[data-testid="stRadio"]:has(div[aria-label="Sport"]) div[role="radiogroup"] label:hover {
    border-color: rgba(102,126,234,0.55) !important;
    background: rgba(102,126,234,0.12) !important;
    color: #c7d2fe !important;
}
div[data-testid="stRadio"]:has(div[aria-label="Sport"]) div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(135deg, rgba(102,126,234,0.28), rgba(118,75,162,0.28)) !important;
    border-color: #818cf8 !important;
    color: #e0e7ff !important;
    box-shadow: 0 0 12px rgba(102,126,234,0.25) !important;
}
div[data-testid="stRadio"]:has(div[aria-label="Sport"]) div[role="radiogroup"] label p {
    margin: 0 !important;
    line-height: 1.2 !important;
    font-size: 0.78rem !important;
    color: inherit !important;
}
/* Hide the radio dot ── */
div[data-testid="stRadio"]:has(div[aria-label="Sport"]) div[data-baseweb="radio"] { display: none !important; }
div[data-testid="stRadio"]:has(div[aria-label="Sport"]) div[role="radio"] { display: none !important; }
div[data-testid="stRadio"]:has(div[aria-label="Sport"]) svg { display: none !important; }
/* Larger emoji in sport cards */
div[data-testid="stRadio"]:has(div[aria-label="Sport"]) div[role="radiogroup"] label p:first-child { font-size: 1.4rem !important; line-height: 1 !important; margin-bottom: 2px !important; }

/* Horizontal radio generic styling (Experience/Category) */
div[data-testid="stRadio"]:not(:has(div[aria-label="Sport"])) div[role="radiogroup"] {
    gap: 12px !important;
}
div[data-testid="stRadio"]:not(:has(div[aria-label="Sport"])) > label {
    color: #d1d5db !important;
    font-size: 0.88rem !important;
}


div.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.8rem;
    font-weight: 600;
    font-size: 0.95rem;
    width: 100%;
    transition: opacity 0.2s;
}
div.stButton > button:hover { opacity: 0.88; }

.stSpinner > div { border-top-color: #667eea !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# SIDEBAR — ATHLETE PROFILE
# ══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### ⚡ AI Sports Assistant")
    st.markdown("<small style='color:#9ca3af'>SJSU Graduate Project — RAG System</small>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("#### 👤 Athlete Profile")

    # Sport selector as 2×2 icon cards
    st.markdown('<p style="color:#d1d5db;font-size:0.80rem;font-weight:600;letter-spacing:0.05em;text-transform:uppercase;margin-bottom:4px">Sport</p>', unsafe_allow_html=True)
    sport_raw = st.radio(
        "Sport",
        ["⚽\nSoccer", "🎾\nTennis", "🏀\nBasketball", "🏋️\nStrength"],
        key="sport_radio",
        label_visibility="collapsed",
        horizontal=False,
    )
    # Map radio label back to full sport name
    sport_map = {
        "⚽\nSoccer": "Soccer",
        "🎾\nTennis": "Tennis",
        "🏀\nBasketball": "Basketball",
        "🏋️\nStrength": "Strength Training",
    }
    sport = sport_map.get(sport_raw, "Soccer")

    goal = st.selectbox(
        "Primary Goal",
        ["Improve Performance", "Build Strength", "Improve Endurance",
         "Lose Weight / Lean Out", "General Fitness", "Faster Recovery"],
        key="goal"
    )

    experience = st.radio(
        "Experience Level",
        ["Beginner", "Intermediate", "Advanced"],
        key="experience",
        horizontal=True
    )

    col1, col2 = st.columns(2)
    with col1:
        training_days = st.number_input("Days/Week", min_value=1, max_value=7, value=3, key="training_days")
    with col2:
        body_weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70, step=1, key="body_weight")

    col3, col4 = st.columns(2)
    with col3:
        age = st.number_input("Age", min_value=14, max_value=75, value=25, step=1, key="age")
    with col4:
        st.empty()

    category = st.radio(
        "Guidance Category",
        ["Training", "Nutrition", "Recovery"],
        key="category",
        horizontal=True
    )

    st.markdown("---")
    st.markdown("#### ⚙️ Settings")
    show_baseline = st.toggle("Show Baseline vs RAG Comparison", value=True, key="show_baseline")
    num_sources = st.slider("Sources to Retrieve", 2, 8, 6, key="num_sources")

    # ── Live Profile Snapshot ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📊 Profile Snapshot")
    ins = PROFILE_INSIGHTS.get(sport, {})
    
    if ins:
        # ── 7-Factor Readiness Score ──────────────────────────────────

        # F1: Experience baseline
        exp_base = {"Beginner": 68, "Intermediate": 75, "Advanced": 82}
        f1 = exp_base.get(experience, 75)
        f1_label = "Experience Base"

        # F2: Training load vs optimal for experience level
        optimal = {"Beginner": 3, "Intermediate": 4, "Advanced": 5}
        load_diff = int(training_days) - optimal.get(experience, 4)
        if load_diff > 0:
            f2 = -load_diff * 7
            f2_label = f"Load ↑ ({'+' if f2>0 else ''}{f2})"
        elif load_diff < 0:
            f2 = load_diff * 2
            f2_label = f"Load ↓ ({'+' if f2>0 else ''}{f2})"
        else:
            f2 = +5
            f2_label = f"Load Optimal (+{f2})"

        # F3: Goal type
        goal_mods = {
            "Improve Performance":    (+4, "Goal: Performance"),
            "Build Strength":         (+3, "Goal: Strength"),
            "Improve Endurance":      (+2, "Goal: Endurance"),
            "General Fitness":        (+2, "Goal: Fitness"),
            "Lose Weight / Lean Out": (-4, "Goal: Cut ⚠️"),
            "Faster Recovery":        (-6, "Goal: Recovery ⚠️"),
        }
        f3, f3_label = goal_mods.get(goal, (0, "Goal: Neutral"))
        f3_label += f" ({'+' if f3>=0 else ''}{f3})"

        # F4: Body weight demand
        bw = float(body_weight)
        if bw < 65:   f4, f4_label = +3, "Weight: Light (+3)"
        elif bw > 95: f4, f4_label = -4, "Weight: Heavy (–4)"
        else:         f4, f4_label =  0, "Weight: Normal"

        # F5: Sport metabolic intensity
        sport_mods = {
            "Soccer":          (0,  "Sport: High Impact"),
            "Basketball":      (0,  "Sport: High Impact"),
            "Tennis":          (+2, "Sport: Moderate (+2)"),
            "Strength Training":(+1, "Sport: Low-Impact (+1)"),
        }
        f5, f5_label = sport_mods.get(sport, (0, "Sport: Neutral"))

        # F6: Age recovery factor
        age_v = int(age)
        if age_v < 22:   f6, f6_label = +4, "Age: Young (+4)"
        elif age_v < 30: f6, f6_label = +2, "Age: Prime (+2)"
        elif age_v < 40: f6, f6_label =  0, "Age: Mature"
        elif age_v < 50: f6, f6_label = -3, "Age: Vet (–3)"
        else:            f6, f6_label = -6, "Age: Senior (–6)"

        score = max(10, min(100, f1 + f2 + f3 + f4 + f5 + f6))
        color = "#10b981" if score >= 80 else "#f59e0b" if score >= 55 else "#ef4444"
        label = "Peak" if score >= 80 else "Moderate" if score >= 55 else "High Load"

        # ── Gauge ────────────────────────────────────────────────
        st.markdown(f"""
<div style="display:flex; flex-direction:column; align-items:center; margin-bottom:10px; padding:14px; background:rgba(0,0,0,0.18); border-radius:14px; border:1px solid rgba(255,255,255,0.06);">
  <div style="position:relative; width:110px; height:110px;">
    <svg viewBox="0 0 36 36" style="width:110px; height:110px; transform:rotate(-90deg);">
      <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
            fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="3"/>
      <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
            fill="none" stroke="{color}" stroke-width="3"
            stroke-dasharray="{score}, 100" stroke-linecap="round"
            style="filter:drop-shadow(0 0 6px {color});"/>
    </svg>
    <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center;">
      <span style="font-size:1.8rem;font-weight:800;color:#fff;display:block;line-height:1;">{score}</span>
      <span style="font-size:0.48rem;color:{color};text-transform:uppercase;letter-spacing:0.08em;font-weight:700;">{label}</span>
    </div>
  </div>
  <div style="font-size:0.58rem;color:#6b7280;text-align:center;margin-top:5px;">6-Factor Readiness · {experience} · {age}y · {int(bw)}kg</div>
</div>""", unsafe_allow_html=True)

        # ── Factor Breakdown (Whoop-style) ───────────────────────────
        factors = [
            ("Experience", f1 - 68, f"{experience}"),
            ("Training Load", f2, f2_label.split('(')[0].strip()),
            ("Goal", f3, goal.split('/')[0].strip()),
            ("Body Weight", f4, f4_label.split(':')[1].split('(')[0].strip()),
            ("Sport", f5, sport),
            ("Age", f6, f"{age}y"),
        ]

        rows = ""
        for name, val, detail in factors:
            bar_color = "#10b981" if val > 0 else "#ef4444" if val < 0 else "#6b7280"
            symbol = f"+{val}" if val >= 0 else str(val)
            pct = min(abs(val) / 10 * 100, 100)
            rows += f"""
<div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
  <div style="width:62px;font-size:0.6rem;color:#9ca3af;text-align:right;flex-shrink:0;">{name}</div>
  <div style="flex:1;background:rgba(255,255,255,0.05);border-radius:3px;height:7px;">
    <div style="width:{pct}%;background:{bar_color};height:100%;border-radius:3px;"></div>
  </div>
  <div style="width:28px;font-size:0.6rem;font-weight:700;color:{bar_color};">{symbol}</div>
  <div style="font-size:0.58rem;color:#6b7280;flex:1;">{detail}</div>
</div>"""

        st.markdown(f"""
<div style="background:rgba(0,0,0,0.15);border-radius:10px;padding:10px 12px;border:1px solid rgba(255,255,255,0.05);margin-bottom:12px;">
  <div style="font-size:0.65rem;color:#9ca3af;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:8px;">Score Breakdown</div>
  {rows}
</div>""", unsafe_allow_html=True)

        # Personalized protein pill
        try:
            bw = float(body_weight)
            lo = round(1.6 * bw, 1)
            hi = round(2.0 * bw, 1)
            st.markdown(f"""
<div class="protein-pill">
  <div class="pp-label">🥩 Daily Protein Target</div>
  <div class="pp-value">{lo}–{hi} g/day</div>
  <div class="pp-label" style="margin-top:3px">{ins['protein']}</div>
</div>""", unsafe_allow_html=True)
        except Exception:
            pass

        # 2-column stat cards
        freq = ins['sessions'].get(experience, list(ins['sessions'].values())[0])
        st.markdown(f"""
<div class="stat-grid">
  <div class="stat-card">
    <div class="sc-label">🍚 Carbs Training</div>
    <div class="sc-value">{ins['carbs_training'].split('(')[0].strip()}</div>
  </div>
  <div class="stat-card">
    <div class="sc-label">⚡ Carbs Match</div>
    <div class="sc-value">{ins['carbs_match'].split('(')[0].strip()}</div>
  </div>
  <div class="stat-card">
    <div class="sc-label">😴 Sleep</div>
    <div class="sc-value">{ins['sleep'].split(';')[0].strip()}</div>
  </div>
  <div class="stat-card">
    <div class="sc-label">📅 Frequency</div>
    <div class="sc-value">{freq.split('(')[0].strip()}</div>
  </div>
</div>""", unsafe_allow_html=True)

        # Hydration wide card
        st.markdown(f"""
<div class="stat-card-wide">
  <div class="sc-label">💧 Hydration Protocol</div>
  <div class="sc-value">{ins['hydration']}</div>
</div>""", unsafe_allow_html=True)

        # Goal tip
        goal_tip = GOAL_TIPS.get(goal, "")
        if goal_tip:
            st.markdown(f"""
<div class="stat-card-wide" style="background:rgba(245,158,11,0.10);border-color:rgba(245,158,11,0.3)">
  <div class="sc-label" style="color:#fcd34d">🎯 {goal}</div>
  <div class="sc-value" style="color:#fde68a">{goal_tip}</div>
</div>""", unsafe_allow_html=True)

        st.caption(f"Sources: {ins['key_orgs']}")
        st.caption(f"💡 {ins['acwr_tip'][:80]}...")

    st.markdown("---")
    st.markdown('<small style="color:#6b7280">Powered by SentenceTransformers + FAISS + Gemini 2.5 Flash</small>',
                unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# HERO HEADER
# ══════════════════════════════════════════════════════════════════════════
sport_icons = {"Soccer": "⚽", "Tennis": "🎾", "Basketball": "🏀", "Strength Training": "🏋️"}
icon = sport_icons.get(sport, "⚡")

st.markdown(f"""
<div class="hero-header">
    <h1>{icon} AI Sports Performance Assistant</h1>
    <p>Evidence-based training, nutrition & recovery guidance powered by Retrieval-Augmented Generation</p>
</div>
""", unsafe_allow_html=True)

# Quick stat row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-box"><div class="num">36</div><div class="lbl">Trusted Sources</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-box"><div class="num">4</div><div class="lbl">Sports Covered</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-box"><div class="num">123</div><div class="lbl">Knowledge Chunks</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-box"><div class="num">RAG</div><div class="lbl">Evidence-Grounded</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# QUESTION INPUT
# ══════════════════════════════════════════════════════════════════════════
st.markdown('<div class="step-label">Ask Your Question</div>', unsafe_allow_html=True)

example_questions = {
    "Soccer":           "What are effective interval training methods for a beginner soccer player?",
    "Tennis":           "What recovery strategies are recommended after a 2-hour tennis match?",
    "Basketball":       "What hydration strategies should basketball players follow during games?",
    "Strength Training":"How much protein does a strength training athlete need per day?"
}

question = st.text_area(
    "Your Question",
    value=example_questions.get(sport, ""),
    height=100,
    placeholder="Ask anything about training, nutrition, or recovery...",
    label_visibility="collapsed"
)

run_btn = st.button("🔍 Generate Evidence-Based Answer", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# MAIN LOGIC
# ══════════════════════════════════════════════════════════════════════════
if run_btn:
    if not question.strip():
        st.warning("Please enter a question before generating an answer.")
    elif not os.getenv("GOOGLE_API_KEY"):
        st.error("⚠️ No Google API key found. Please add GOOGLE_API_KEY to your `.env` file. Get one free at https://aistudio.google.com/app/apikey")
    else:
        user_profile = {
            "sport": sport,
            "goal": goal,
            "category": category,
            "experience": experience,
            "training_days": str(training_days),
            "body_weight": str(body_weight)
        }

        # ── Retrieve relevant chunks ───────────────────────────────────────
        with st.spinner("🔎 Searching knowledge base..."):
            chunks = retrieve(
                question,
                sport_filter=sport,
                category_filter=category,
                top_k=num_sources
            )
            # Fallback: no filter if no sport-specific results
            if not chunks:
                chunks = retrieve(question, top_k=num_sources)

        # streaming handles generation in place now

        # ══════════════════════════════════════════════════════════════════
        # DISPLAY RESULTS
        # ══════════════════════════════════════════════════════════════════

        if show_baseline:
            left_col, right_col = st.columns(2)
        else:
            left_col = st.container()
            right_col = None

        # ── RAG Answer ────────────────────────────────────────────────────
        with left_col:
            st.markdown('<span class="badge badge-rag">🔬 RAG Answer — Evidence Grounded</span>', unsafe_allow_html=True)
            with st.spinner("🧠 Generating RAG answer..."):
                rag_generator = get_rag_answer(question, chunks, user_profile)
                st.markdown('<div class="answer-wrapper-rag">', unsafe_allow_html=True)
                rag_answer = st.write_stream(rag_generator)
                st.markdown('</div>', unsafe_allow_html=True)

        # ── Baseline Answer ───────────────────────────────────────────────
        if right_col is not None:
            with right_col:
                st.markdown('<span class="badge badge-base">💬 Baseline LLM — No Retrieved Context</span>', unsafe_allow_html=True)
                with st.spinner("📝 Generating baseline answer for comparison..."):
                    baseline_generator = get_baseline_answer(question, user_profile)
                    st.markdown('<div class="answer-wrapper-base">', unsafe_allow_html=True)
                    baseline_answer = st.write_stream(baseline_generator)
                    st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Retrieved Sources ─────────────────────────────────────────────
        if chunks:
            st.markdown('<span class="badge badge-src">📚 Retrieved Evidence Sources</span>', unsafe_allow_html=True)
            with st.expander("View Retrieved Source Chunks", expanded=True):
                for i, chunk in enumerate(chunks):
                    st.markdown(f"""
<div class="card">
<span class="source-chip">📖 {chunk['source_id']}</span>
<span class="source-chip">🏷️ {chunk['sport']} · {chunk['category']}</span>
<span class="source-chip">🏛️ {chunk['organization']}</span>
<br><br>
<strong style="color:#e2e8f0">{chunk['title']}</strong>
<p style="color:#9ca3af;font-size:0.83rem;margin-top:4px"><em>Relevance Score (L2): {chunk['score']:.4f}</em></p>
<p style="color:#c4cad4;font-size:0.88rem;line-height:1.6;margin-top:8px">{chunk['text']}</p>
</div>
                    """, unsafe_allow_html=True)

        # ── Limitations / Safety ──────────────────────────────────────────
        st.markdown("""
<div class="warning-box">
⚠️ <strong>Important Limitations:</strong> This tool provides general, evidence-based sports performance guidance only.
It does <strong>not</strong> provide medical diagnoses, injury treatment advice, or personalized supplement prescriptions.
Always consult a qualified physician, registered dietitian, or certified coach before making significant changes to
your training or nutrition, especially if you have any existing health conditions.
</div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# FOOTER — ABOUT / METHODOLOGY
# ══════════════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("ℹ️ About This System — Methodology & Sources"):
    st.markdown("""
**AI Sports Performance Assistant** is a graduate research project built at San Jose State University.

### How It Works (RAG Pipeline)
1. **36 curated source documents** from trusted sports science organizations (FIFA, UEFA, ITF, USTA, ATP/WTA, USOPC, FIBA, NBA Performance Lab, NCAA, NBPA, NSCA, ACSM, ISSN, NIH, USDA/AND, GSSI, BJSM, JSCR) were collected and cleaned.
2. Documents were **chunked** into overlapping 150-word segments with 30-word overlap → **123 total chunks**.
3. Each chunk was **embedded** using `SentenceTransformers (all-MiniLM-L6-v2)` into a 384-dimensional vector.
4. Vectors are stored in a **FAISS IndexFlatL2** for exact nearest-neighbor retrieval.
5. At query time, the user's question is embedded and the **top-k most relevant chunks** are retrieved with sport/category pre-filtering.
6. Retrieved chunks + the athlete profile are passed to **Gemini 2.5 Flash** with a structured prompt requesting a Sample Plan section.
7. The **Baseline** mode generates an answer without any retrieved context for direct comparison.

### Scope & Boundaries
- **Sports supported:** Soccer, Tennis, Basketball, Strength Training
- **Categories:** Training, Nutrition, Recovery/Hydration
- **Target users:** Beginner to intermediate athletes
- **Not supported:** Medical diagnoses, injury treatment, supplement prescriptions, live data
    """)
