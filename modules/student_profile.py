"""
GMA Insight – Student Profile
-------------------------------
Manages student session state: registration details, exam data, rank/score.
"""

import streamlit as st
from modules.config import CATEGORIES, BRAND


def init_profile():
    """Initialize default student profile in session state."""
    if "student" not in st.session_state:
        st.session_state.student = {
            "name":       "",
            "dob":        None,
            "state":      "Kerala",
            "category":   "General (UR)",
            "exam":       "NEET UG",
            "score":      None,
            "rank":       None,
            "percentile": None,
            "registered": False,
        }


def get_student() -> dict:
    init_profile()
    return st.session_state.student


def render_profile_sidebar():
    """Render student registration / profile form in the sidebar."""
    init_profile()
    s = st.session_state.student

    name_display  = s["name"] if s["name"] else "Not Set"
    rank_display  = str(s["rank"])  if s["rank"]  else "–"
    score_display = str(s["score"]) if s["score"] else "–"

    rank_badge  = f'<span style="background:{BRAND["primary"]}33; color:{BRAND["primary"]}; padding:2px 10px; border-radius:20px; font-size:12px; font-weight:600;">Rank: {rank_display}</span>'
    score_badge = f'<span style="background:{BRAND["accent"]}22; color:{BRAND["accent"]}; padding:2px 10px; border-radius:20px; font-size:12px; font-weight:600;">Score: {score_display}</span>'
    badges_row  = f'<div style="margin-top:8px; display:flex; gap:8px;">{rank_badge}{score_badge}</div>'

    card_html = (
        f'<div style="background:linear-gradient(135deg,{BRAND["primary"]}22,{BRAND["secondary"]}22);'
        f'border:1px solid {BRAND["primary"]}44; border-radius:12px; padding:14px 16px; margin-bottom:18px;">'
        f'<div style="font-size:11px; color:{BRAND["muted"]}; letter-spacing:2px; text-transform:uppercase; margin-bottom:4px;">Student Profile</div>'
        f'<div style="font-size:18px; font-weight:700; color:{BRAND["text"]};">{name_display}</div>'
        f'<div style="font-size:12px; color:{BRAND["muted"]}; margin-top:2px;">{s["exam"]} &nbsp;|&nbsp; {s["category"]}</div>'
        f'{badges_row}'
        f'</div>'
    )
    st.sidebar.markdown(card_html, unsafe_allow_html=True)

    with st.sidebar.expander("✏️ Edit Profile", expanded=not s["registered"]):
        s["name"]     = st.text_input("Full Name", value=s["name"], placeholder="e.g. Arjun Kumar")
        s["state"]    = st.selectbox("State", [
            "Kerala", "Tamil Nadu", "Karnataka", "Andhra Pradesh",
            "Telangana", "Maharashtra", "Delhi", "Uttar Pradesh",
            "Rajasthan", "Gujarat", "West Bengal", "Other",
        ], index=0)
        s["category"] = st.selectbox("Category", CATEGORIES)
        s["exam"]     = st.selectbox("Exam", ["NEET UG", "KEAM", "NEET PG"])

        st.markdown("##### Exam / Rank Details")
        score_col, rank_col = st.columns(2)
        with score_col:
            score_val = st.number_input("Score", min_value=0, max_value=720,
                                        value=s["score"] if s["score"] else 0, step=1)
        with rank_col:
            rank_val  = st.number_input("Rank", min_value=0, max_value=1_000_000,
                                        value=s["rank"] if s["rank"] else 0, step=1)

        if st.button("💾 Save Profile", use_container_width=True):
            s["score"] = score_val if score_val > 0 else None
            s["rank"]  = rank_val  if rank_val  > 0 else None
            s["registered"] = True
            st.success("Profile saved!")
            st.rerun()
