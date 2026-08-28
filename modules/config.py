"""
GMA Insight – Configuration & Constants
----------------------------------------
Central config: brand colors, admission stages, chance thresholds.
"""

from enum import Enum

# ─────────────────────────────────────────────
# Brand & Theme
# ─────────────────────────────────────────────
BRAND = {
    "name":      "GMA Insight",
    "tagline":   "Actionable Admission Intelligence",
    "primary":   "#C0392B",   # volcano red
    "secondary": "#1B5E20",   # deep forest green
    "accent":    "#4CAF50",   # forest green (light)
    "danger":    "#C0392B",   # volcano red
    "warn":      "#E57373",   # soft warm red
    "bg_dark":   "#0A0C0A",
    "bg_card":   "#121512",
    "bg_card2":  "#181D18",
    "text":      "#FFFFFF",   # bright white
    "muted":     "#B0BEC5",   # dim white
}

CHANCE_COLORS = {
    "High":     "#4CAF50",   # forest green
    "Moderate": "#E57373",   # soft warm red
    "Low":      "#C0392B",   # volcano red
}

CHANCE_ICONS = {
    "High":     "✅",
    "Moderate": "🟡",
    "Low":      "🔴",
}

# ─────────────────────────────────────────────
# Admission Stages (Event Engine)
# ─────────────────────────────────────────────
class AdmissionStage(Enum):
    REGISTRATION      = "registration"
    EXAM              = "exam"
    POST_EXAM_POLL    = "post_exam_poll"
    RESULT            = "result"
    RANK_ANALYSIS     = "rank_analysis"
    COUNSELLING_REG   = "counselling_reg"
    ROUND_1           = "round_1"
    ROUND_2           = "round_2"
    FINAL_ALLOTMENT   = "final_allotment"

STAGE_LABELS = {
    AdmissionStage.REGISTRATION:    "📋 Registration",
    AdmissionStage.EXAM:            "✏️  Exam",
    AdmissionStage.POST_EXAM_POLL:  "📊 Post-Exam Poll",
    AdmissionStage.RESULT:          "📜 Result",
    AdmissionStage.RANK_ANALYSIS:   "🏆 Rank Analysis",
    AdmissionStage.COUNSELLING_REG: "📝 Counselling Registration",
    AdmissionStage.ROUND_1:         "🔵 Round 1 Allotment",
    AdmissionStage.ROUND_2:         "🟣 Round 2 Allotment",
    AdmissionStage.FINAL_ALLOTMENT: "🎓 Final Allotment",
}

STAGE_ORDER = list(AdmissionStage)

# ─────────────────────────────────────────────
# ACTIVE STAGE  ← Admin sets this
# ─────────────────────────────────────────────
# Change this value to control which insights are shown to ALL students.
# Students never see or change this — it is backend-controlled.
ACTIVE_STAGE = AdmissionStage.RANK_ANALYSIS


# ─────────────────────────────────────────────
# Rank / Chance Thresholds
# ─────────────────────────────────────────────
# Buffer around student rank to include colleges
RANK_BUFFER_PERCENT = 0.20   # ±20% of rank

# Chance classification relative to previous year closing rank
CHANCE_HIGH_BELOW    = 0.90  # student rank < 90% of closing rank → High
CHANCE_MODERATE_BELOW = 1.10 # student rank < 110% of closing rank → Moderate
# else → Low

# ─────────────────────────────────────────────
# Categories (NEET – General)
# ─────────────────────────────────────────────
CATEGORIES = [
    "General (UR)",
    "OBC",
    "SC",
    "ST",
    "EWS",
    "PH / PWD",
]

# ─────────────────────────────────────────────
# Kerala-specific counselling categories
# Extracted from 2025_Rank.xlsx actual allotment data
# ─────────────────────────────────────────────

# Full label shown to student → code stored internally
KERALA_CATEGORY_MAP = {
    "SM – State Merit (General)":               "SM",
    "EZ – Economically Backward (Forward Comm.)":"EZ",
    "EW – Economically Weaker Section":          "EW",
    "MU – Muslim OBC":                           "MU",
    "BH – OBC Hindu (Ezhava/Thiyya)":            "BH",
    "BX – OBC Christian":                        "BX",
    "LA – Latin Catholic / Anglo-Indian":        "LA",
    "VK – Viswakarma / OBC":                     "VK",
    "KN – Kudumbi (OBC)":                        "KN",
    "SC – Scheduled Caste":                      "SC",
    "ST – Scheduled Tribe":                      "ST",
    "PD – Persons with Disability":              "PD",
    "MM – Management Quota":                     "MM",
    "NR – NRI Quota":                            "NR",
    "AC – Armed Forces / Ex-Serviceman":         "AC",
    "AM – Anglo-Indian / Minority":              "AM",
    "DV – Differently Abled / Visually Imp.":   "DV",
    "NC – Non-Creamy Layer OBC":                 "NC",
    "KU – Kudumbi":                              "KU",
}

KERALA_CATEGORIES = list(KERALA_CATEGORY_MAP.keys())

# State → categories map
STATE_CATEGORIES: dict[str, list[str]] = {
    "Kerala": KERALA_CATEGORIES,
}
# All other states fall back to CATEGORIES

# ─────────────────────────────────────────────
# Exam subjects for poll
# ─────────────────────────────────────────────
POLL_SUBJECTS = ["Biology", "Chemistry", "Physics"]
DIFFICULTY_LEVELS = ["Very Easy", "Easy", "Moderate", "Difficult", "Very Difficult"]
