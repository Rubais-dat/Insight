"""
GMA Insight – Data Loader
--------------------------
Generates and caches all sample datasets used by insight modules.
In production, replace generate_* functions with real DB/API calls.
"""

import numpy as np
import pandas as pd
import streamlit as st
from modules.config import CATEGORIES, POLL_SUBJECTS, DIFFICULTY_LEVELS

# ─────────────────────────────────────────────
# College & Course Master Lists
# ─────────────────────────────────────────────
COLLEGES = [
    "AIIMS New Delhi", "JIPMER Puducherry", "Maulana Azad Medical College",
    "Grant Medical College Mumbai", "Seth GS Medical College",
    "KGMC Lucknow", "Madras Medical College", "Government Medical College Kozhikode",
    "Government Medical College Thiruvananthapuram", "Amrita School of Medicine",
    "Kasturba Medical College Manipal", "Sri Ramachandra Institute",
    "Jawaharlal Nehru Medical College Aligarh", "Bangalore Medical College",
    "Mysore Medical College", "Rajiv Gandhi University of Health Sciences",
    "Government Medical College Thrissur", "Government Medical College Ernakulam",
    "SRM Medical College", "Saveetha Medical College",
    "Chettinad Hospital & Research Institute", "PSG Institute of Medical Sciences",
    "Vinayaka Missions Medical College", "Sri Manakula Vinayagar Medical College",
    "Indira Gandhi Medical College Shimla", "Government Medical College Chandigarh",
    "Vardhman Mahavir Medical College", "Lady Hardinge Medical College",
    "University College of Medical Sciences Delhi", "Shyam Shah Medical College",
    "Government Medical College Nagpur", "BJ Medical College Ahmedabad",
    "Government Medical College Surat", "Pandit Bhagwat Dayal Sharma PGIMS",
    "Pt. B.D. Sharma UHS Rohtak", "Government Medical College Amritsar",
    "Government Medical College Patiala", "Osmania Medical College",
    "Gandhi Medical College Hyderabad", "Guntur Medical College",
    "Government Medical College Anantapur", "Kurnool Medical College",
    "Andhra Medical College", "Sri Venkateswara Medical College",
    "Government Medical College Baroda", "Medical College Kolkata",
    "IPGMER Kolkata", "North Bengal Medical College",
    "Gauhati Medical College", "Silchar Medical College",
    "Regional Institute of Medical Sciences Imphal",
    "Pt. JNM Medical College Raipur", "AIIMS Bhopal",
    "AIIMS Jodhpur", "AIIMS Rishikesh",
    "AIIMS Patna", "AIIMS Bhubaneswar",
    "AIIMS Raipur", "AIIMS Nagpur",
    "AIIMS Mangalagiri", "AIIMS Gorakhpur",
]

COURSES = [
    "MBBS",
    "BDS",
    "BAMS",
    "BHMS",
    "BUMS",
    "B.Sc Nursing",
    "B.Sc Allied Health Sciences",
]

QUOTA_TYPES = ["Government", "Management", "NRI"]
ROUND_LABELS = ["Round 1", "Round 2", "Round 3", "Mop-up"]


# ─────────────────────────────────────────────
# Previous Year Allotment Data
# ─────────────────────────────────────────────
@st.cache_data
def load_allotment_data() -> pd.DataFrame:
    """
    Generate realistic previous-year (2025) allotment data.
    Columns: college, course, category, quota, round, closing_rank
    """
    np.random.seed(42)
    rows = []

    for college in COLLEGES:
        # Each college has 3-6 course-category combos
        n_rows = np.random.randint(3, 7)
        for _ in range(n_rows):
            course   = np.random.choice(COURSES[:3], p=[0.70, 0.15, 0.15])
            category = np.random.choice(CATEGORIES, p=[0.40, 0.25, 0.15, 0.05, 0.10, 0.05])
            quota    = np.random.choice(QUOTA_TYPES, p=[0.60, 0.30, 0.10])
            round_   = np.random.choice(ROUND_LABELS, p=[0.55, 0.25, 0.15, 0.05])

            # Closing rank depends on college prestige tier
            if college.startswith("AIIMS"):
                base_rank = np.random.randint(1, 200)
            elif college in [
                "JIPMER Puducherry", "Maulana Azad Medical College",
                "Grant Medical College Mumbai",
            ]:
                base_rank = np.random.randint(100, 800)
            elif "Government" in college or "Govt" in college:
                base_rank = np.random.randint(500, 8000)
            else:
                base_rank = np.random.randint(3000, 25000)

            # Category adjustments
            cat_mult = {
                "General (UR)": 1.0,
                "OBC": 1.3,
                "SC": 2.5,
                "ST": 4.0,
                "EWS": 1.2,
                "PH / PWD": 6.0,
            }
            closing_rank = int(base_rank * cat_mult.get(category, 1.0))

            rows.append({
                "college":       college,
                "course":        course,
                "category":      category,
                "quota":         quota,
                "round":         round_,
                "closing_rank":  closing_rank,
            })

    df = pd.DataFrame(rows)
    df = df.sort_values("closing_rank").reset_index(drop=True)
    return df


# ─────────────────────────────────────────────
# Rank Distribution Data
# ─────────────────────────────────────────────
@st.cache_data
def load_rank_distribution() -> pd.DataFrame:
    """
    Simulated NEET 2025 rank vs score distribution for ~60,000 students.
    Columns: rank, score
    """
    np.random.seed(7)
    total_students = 60_000
    # Score distribution: mostly 300-600, bell-ish
    scores = np.clip(
        np.random.normal(loc=450, scale=100, size=total_students),
        100, 720
    ).astype(int)
    # Rank = sorted position (rank 1 = highest score)
    scores_sorted = np.sort(scores)[::-1]
    ranks = np.arange(1, total_students + 1)
    df = pd.DataFrame({"rank": ranks, "score": scores_sorted})
    return df


# ─────────────────────────────────────────────
# Community Poll Data
# ─────────────────────────────────────────────
@st.cache_data
def load_poll_data() -> dict:
    """
    Simulated GMA poll responses from 1,400 students.
    Returns aggregated counts per question.
    """
    np.random.seed(21)
    n = 1_400

    def weighted_choices(options, weights, size):
        return list(np.random.choice(options, p=weights, size=size))

    poll = {
        "total_respondents": n,
        "overall_difficulty": {
            level: int(count)
            for level, count in zip(
                DIFFICULTY_LEVELS,
                np.random.multinomial(n, [0.05, 0.15, 0.35, 0.30, 0.15])
            )
        },
        "subject_difficulty": {
            subj: {
                level: int(count)
                for level, count in zip(
                    DIFFICULTY_LEVELS,
                    np.random.multinomial(n, probs)
                )
            }
            for subj, probs in {
                "Biology":   [0.08, 0.20, 0.30, 0.27, 0.15],
                "Chemistry": [0.05, 0.12, 0.28, 0.35, 0.20],
                "Physics":   [0.04, 0.10, 0.22, 0.38, 0.26],
            }.items()
        },
        "hardest_subject": {
            subj: int(count)
            for subj, count in zip(
                POLL_SUBJECTS,
                np.random.multinomial(n, [0.28, 0.35, 0.37])
            )
        },
        "attempts_100_plus": int(np.random.randint(700, 1000)),
        "attempts_150_plus": int(np.random.randint(300, 600)),
        "attempts_170_plus": int(np.random.randint(80, 250)),
    }
    return poll


# ─────────────────────────────────────────────
# Counselling Round Data
# ─────────────────────────────────────────────
@st.cache_data
def load_counselling_data() -> pd.DataFrame:
    """
    Simulated round-wise closing rank shifts for colleges.
    Columns: college, course, category, round1_cr, round2_cr, round3_cr
    """
    np.random.seed(55)
    allotment = load_allotment_data()
    # Take Round 1 base
    r1 = allotment[allotment["round"] == "Round 1"].copy()
    r1 = r1.rename(columns={"closing_rank": "round1_cr"})

    # Simulate Round 2 & Round 3 closing ranks (generally increase)
    r1["round2_cr"] = (
        r1["round1_cr"] * np.random.uniform(1.02, 1.12, len(r1))
    ).astype(int)
    r1["round3_cr"] = (
        r1["round2_cr"] * np.random.uniform(1.01, 1.08, len(r1))
    ).astype(int)

    r1["trend"] = r1.apply(
        lambda row: "📈 Increasing" if row["round2_cr"] > row["round1_cr"] * 1.05
        else "📉 Decreasing" if row["round2_cr"] < row["round1_cr"] * 0.97
        else "➡️ Stable",
        axis=1,
    )
    return r1.reset_index(drop=True)


# ─────────────────────────────────────────────
# Helper: Get rank from score
# ─────────────────────────────────────────────
def score_to_rank(score: int, rank_dist: pd.DataFrame) -> int:
    """Return the approximate rank for a given score."""
    close = rank_dist.iloc[(rank_dist["score"] - score).abs().argsort()[:1]]
    return int(close["rank"].values[0])
