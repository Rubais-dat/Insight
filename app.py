"""
GMA Insight – Main Application
================================
Thin orchestrator: routes between Registration and Insights Feed.
All UI rendering lives in modules/ui_components.py.
All config/data helpers live in modules/config.py.

Run:        streamlit run app.py
Admin Panel: streamlit run pages/admin_panel.py --server.port 8502
"""

import streamlit as st
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GMA Insight",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Imports ──────────────────────────────────────────────────────────────────
from modules.config import BRAND, load_manual_insights
from modules.ui_components import (
    inject_global_css,
    render_countdown,

    render_live_seat_tracker,
    render_counselling_stage_tracker,
    render_allotment_reminder,
    render_stats_row,
    render_registration,
    render_topbar,
    render_quick_insight,
    render_manual_insights,
)
from modules.kerala_data import get_quick_insight

# ── Global CSS ────────────────────────────────────────────────────────────────
inject_global_css()

st.markdown("""
<style>
[data-testid="collapsedControl"] { display:none; }
.block-container { padding-top: 0 !important; max-width:100% !important; }
</style>
""", unsafe_allow_html=True)

# ── Session init ──────────────────────────────────────────────────────────────
DEV_AUTO_LOGIN = False

# ── Score → rank estimation table (NEET UG, approx Kerala state rank) ────────
_SCORE_RANK_MAP = [
    (720, 1),    (700, 200),  (680, 600),  (660, 1200), (640, 2200),
    (620, 3500), (600, 5500), (580, 8500), (560, 13000),(540, 19000),
    (520, 27000),(500, 37000),(480, 50000),(460, 65000),(440, 83000),
    (420, 105000),(400, 130000),(0, 200000),
]
def _score_to_rank(score: int) -> int:
    """Linearly interpolates NEET score to an approximate Kerala state rank."""
    for i, (s_hi, r_hi) in enumerate(_SCORE_RANK_MAP[:-1]):
        s_lo, r_lo = _SCORE_RANK_MAP[i + 1]
        if score >= s_lo:
            frac = (score - s_lo) / max(s_hi - s_lo, 1)
            return int(r_lo + frac * (r_hi - r_lo))
    return _SCORE_RANK_MAP[-1][1]

# ── Session restore from URL query params (survives page refresh) ────────────
if "registered" not in st.session_state:
    _qp = st.query_params
    if _qp.get("reg") == "1" and _qp.get("name"):
        try:
            _score = int(_qp.get("score", 0))
            _rank  = int(_qp.get("rank", 0)) or (_score_to_rank(_score) if _score else 0)
            st.session_state.registered = True
            st.session_state.student = {
                "name":          _qp.get("name", ""),
                "state":         _qp.get("state", "Kerala"),
                "category":      _qp.get("category", "State Merit (SM)"),
                "category_code": _qp.get("cat_code", "SM"),
                "exam":          _qp.get("exam", "NEET UG"),
                "score":         _score,
                "rank":          _rank,
                "rank_estimated": _rank > 0 and int(_qp.get("rank", 0)) == 0,
                "counsellings":  _qp.get("couns", "Kerala CEE (State Quota)").split(","),
                "courses":       _qp.get("courses", "MBBS").split(","),
            }
            st.session_state.reg_state = _qp.get("state", "Kerala")
        except Exception:
            st.session_state.registered = False
            st.session_state.student    = {}
            st.session_state.reg_state  = "Kerala"
    elif DEV_AUTO_LOGIN:
        st.session_state.registered = True
        st.session_state.student = {
            "name":          "Arjun Kumar (Test)",
            "state":         "Kerala",
            "category":      "State Merit (SM)",
            "category_code": "SM",
            "exam":          "NEET UG",
            "score":         0,
            "rank":          4500,
            "counsellings":  ["Kerala CEE (State Quota)"],
            "courses":       ["MBBS"],
        }
        st.session_state.reg_state = "Kerala"
    else:
        st.session_state.registered = False
        st.session_state.student    = {}
        st.session_state.reg_state  = "Kerala"


# ════════════════════════════════════════════════════════════════════════════
# SCREEN 1 — REGISTRATION  (only screen with user inputs)
# ════════════════════════════════════════════════════════════════════════════
def show_registration():
    from modules.ui_components import render_registration
    render_registration()
# ════════════════════════════════════════════════════════════════════════════
# SCREEN 2 — INSIGHTS FEED  (read-only display, zero inputs)
# ════════════════════════════════════════════════════════════════════════════
def show_insights_feed():
    s = st.session_state.student

    student_exam = s.get("exam", "")
    insights = load_manual_insights()
    # Separate poll-linked insight using explicit 'type' field
    non_poll_insights = [item for item in insights if item.get("type") != "poll"]

    # ── Top bar ───────────────────────────────────────────────────────────────
    render_topbar(s)

    # ── Main content ──────────────────────────────────────────────────────────
    _, main, _ = st.columns([0.3, 9, 0.3])
    with main:
        st.markdown("<br>", unsafe_allow_html=True)

        # ── Read runtime config once ─────────────────────────────────────────
        try:
            with open(os.path.join(os.path.dirname(__file__), "runtime_config.json"), "r") as _rf:
                _rcfg = json.load(_rf)
        except Exception:
            _rcfg = {}

        # Feed module toggles — every section defaults ON if key is missing
        _fm = _rcfg.get("feed_modules", {})
        def _on(key): return _fm.get(key, True)

        _allotment = _rcfg.get("allotment_notification", {})
        _allotment_active = bool(_allotment and _allotment.get("is_active", False))

        # ════════════════════════════════════════════════════════════════════
        # ALWAYS FIRST — Quick Insight (rank review vs last cutoff)
        # ════════════════════════════════════════════════════════════════════
        if _on("quick_insight"):
            render_quick_insight(s)

        # ════════════════════════════════════════════════════════════════════
        # Shared rank context — computed once, used by both modes
        # ════════════════════════════════════════════════════════════════════
        _is_kerala  = s["state"] == "Kerala"
        _final_rank = s.get("rank") or 0
        _score      = s.get("score", 0)
        _cat_code   = s.get("category_code", "")
        # Estimate rank from score if rank absent
        if not _final_rank and _score:
            _final_rank = _score_to_rank(_score)
            s["rank"]           = _final_rank
            s["rank_estimated"] = True

        _choices = _gov_count = _priv_count = None
        if _is_kerala and _final_rank:
            _qi         = get_quick_insight(_final_rank, _cat_code)
            _choices    = _qi["better_choices"]
            
            # Filter by selected courses
            _selected_courses = s.get("courses", ["MBBS"])
            if _selected_courses:
                _choices = [c for c in _choices if any(sc in c.get("course", "") for sc in _selected_courses)]
                
            _gov_count  = len([c for c in _choices if c["college_type"] == "Government"])
            _priv_count = len([c for c in _choices if c["college_type"] != "Government"])

        # ════════════════════════════════════════════════════════════════════
        # MODE A — ALLOTMENT ACTIVE
        # Allotment card + decision-critical sections (deadline, checklist, plan)
        # ════════════════════════════════════════════════════════════════════
        if _allotment_active:
            render_allotment_reminder(_allotment)

            if _is_kerala and _final_rank:
                if _on("countdown"):
                    _dl     = _rcfg.get("countdown_deadline", "")
                    _dl_lbl = _rcfg.get("countdown_label", "Counselling Deadline")
                    _dl_ico = _rcfg.get("countdown_icon", "⏰")
                    if _dl:
                        render_countdown(_dl_lbl, _dl, _dl_ico)


        # ════════════════════════════════════════════════════════════════════
        # MODE B — NORMAL FEED
        # ════════════════════════════════════════════════════════════════════
        else:
            if _is_kerala and _final_rank:
                # Estimated rank notice
                if s.get("rank_estimated"):
                    st.markdown(
                        "<div style='background:#9E9E9E12;border:1px solid #9E9E9E33;"
                        "border-radius:10px;padding:10px 14px;margin-bottom:14px;"
                        "font-size:12px;color:#9E9E9E;'>"
                        "⚠️ Rank estimated from your NEET score. Enter your actual Kerala CEE rank for exact results."
                        "</div>", unsafe_allow_html=True)

                if _on("stats_row"):
                    render_stats_row([
                        {"icon": "🏆", "label": "Your Rank",         "value": f"{_final_rank:,}",  "color": "#E57373"},
                        {"icon": "🏛️", "label": "Govt Options",      "value": str(_gov_count),     "color": "#4CAF50", "sub": "Reachable colleges"},
                        {"icon": "🏫", "label": "Private Options",   "value": str(_priv_count),    "color": "#E57373", "sub": "Includes aided/self-fin"},
                        {"icon": "📅", "label": "2025 Cutoff Data",  "value": "Final",              "color": "#9E9E9E", "sub": "Based on 2025 final cutoffs"},
                    ])

                if _on("countdown"):
                    _deadline       = _rcfg.get("countdown_deadline", "")
                    _deadline_label = _rcfg.get("countdown_label", "Counselling Deadline")
                    _deadline_icon  = _rcfg.get("countdown_icon", "⏰")
                    if _deadline:
                        render_countdown(_deadline_label, _deadline, _deadline_icon)

                if _on("counselling_stage_tracker"):
                    counselling_stages = _fm.get("counselling_stages", {})
                    counsellings = s.get("counsellings", ["Kerala CEE (State Quota)"])
                    
                    st.markdown("<div style='font-size:14px; font-weight:700; color:#FFFFFF; margin-bottom:12px;'>🗺️ Available Counselling Journeys</div>", unsafe_allow_html=True)
                    
                    # Create a grid of square boxes
                    cols = st.columns(len(counsellings) if len(counsellings) <= 3 else 3)
                    for i, c_name in enumerate(counsellings):
                        with cols[i % len(cols)]:
                            with st.container(border=True):
                                st.markdown(f"<div style='text-align:center; padding: 10px 0;'><div style='font-size:32px; margin-bottom:10px;'>🏛️</div><div style='font-size:15px; font-weight:700; color:#FFFFFF; margin-bottom:15px; min-height:40px; display:flex; align-items:center; justify-content:center;'>{c_name}</div></div>", unsafe_allow_html=True)
                                if st.button("👁️ View Journey", key=f"btn_journey_{i}_{c_name}", use_container_width=True):
                                    st.session_state.active_journey = c_name
                                    
                    if st.session_state.get("active_journey") in counsellings:
                        st.markdown("<br>", unsafe_allow_html=True)
                        active = st.session_state.active_journey
                        _stage_idx = counselling_stages.get(active, _fm.get("counselling_current_stage", 2))
                        render_counselling_stage_tracker(_final_rank, counselling_name=active, current_stage=_stage_idx)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Admin insight cards (Global first, then active journey, then checklist)
        if _on("manual_insights"):
            student_exam = s.get("exam", "")
            global_insights = [
                item for item in non_poll_insights
                if item.get("target_exam", "All Students") in ("All Students", student_exam)
            ]
            
            # Separate out the checklist and FAQ to show them last
            checklist_insights = [item for item in global_insights if "Checklist" in item.get("title", "")]
            faq_insights = [item for item in global_insights if "FAQ" in item.get("title", "")]
            
            global_insights = [item for item in global_insights if "Checklist" not in item.get("title", "") and "FAQ" not in item.get("title", "")]
            
            if global_insights:
                render_manual_insights(global_insights)
                
            if st.session_state.get("active_journey"):
                active = st.session_state.active_journey
                journey_insights = [
                    item for item in non_poll_insights
                    if item.get("target_exam") == active
                ]
                if journey_insights:
                    st.markdown("<br>", unsafe_allow_html=True)
                    render_manual_insights(journey_insights)
                    
            if checklist_insights:
                st.markdown("<br>", unsafe_allow_html=True)
                render_manual_insights(checklist_insights)
                
            if faq_insights:
                st.markdown("<br>", unsafe_allow_html=True)
                render_manual_insights(faq_insights)

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style='text-align:center;margin-top:40px;padding:16px;
        border-top:1px solid #21262D;font-size:11px;color:{BRAND["muted"]};'>
        🔮 <b style='color:{BRAND["primary"]};'>GMA Insight</b> &nbsp;·&nbsp;
        Get My Admission &nbsp;·&nbsp; Actionable Admission Intelligence
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# ROUTER
# ════════════════════════════════════════════════════════════════════════════
if not st.session_state.registered:
    show_registration()
else:
    show_insights_feed()
