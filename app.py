"""
GMA Insight – Main Application
================================
Frontend: Registration screen → Insights feed.
Backend:  All analysis runs server-side. Students only see the results.

Run:        streamlit run insights_app.py
Admin Panel: streamlit run admin_panel.py --server.port 8502
"""

import streamlit as st
import sys, os, json
from datetime import datetime
sys.path.insert(0, os.path.dirname(__file__))

# ── Read manual insights from runtime_config.json (admin-controlled) ──────────
def _load_manual_insights():
    """Load list of manual insights from config."""
    config_path = os.path.join(os.path.dirname(__file__), "runtime_config.json")
    try:
        with open(config_path, "r") as f:
            cfg = json.load(f)
        insights = cfg.get("manual_insights", [])
        if isinstance(insights, list):
            return insights
        return []
    except Exception:
        return []

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GMA Insight",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Imports ──────────────────────────────────────────────────────────────────
from modules.config import (
    BRAND, CATEGORIES, STATE_CATEGORIES, KERALA_CATEGORY_MAP
)
from modules.ui_components import inject_global_css
from modules.data_loader   import load_allotment_data, load_rank_distribution, score_to_rank
from modules.kerala_data       import get_quick_insight

# ── CSS ──────────────────────────────────────────────────────────────────────
inject_global_css()

# Extra overrides for full-screen registration & clean feed
st.markdown(f"""
<style>
[data-testid="collapsedControl"] {{ display:none; }}
.block-container {{ padding-top: 0 !important; max-width:100% !important; }}
</style>
""", unsafe_allow_html=True)

# ── Session init ──────────────────────────────────────────────────────────────
DEV_AUTO_LOGIN = False  # Set to False to test the real registration flow

if "registered" not in st.session_state:
    if DEV_AUTO_LOGIN:
        st.session_state.registered = True
        st.session_state.student = {
            "name": "Arjun Kumar (Test)",
            "state": "Kerala",
            "category": "State Merit (SM)",
            "category_code": "SM",
            "exam": "NEET UG",
            "score": 0,
            "rank": 4500,
        }
        st.session_state.reg_state = "Kerala"
    else:
        st.session_state.registered = False
        st.session_state.student = {}
        st.session_state.reg_state = "Kerala"


# ════════════════════════════════════════════════════════════════════════════
# SCREEN 1 — REGISTRATION
# ════════════════════════════════════════════════════════════════════════════
def show_registration():
    # Full-screen centered layout
    _, center, _ = st.columns([1, 2.2, 1])
    with center:
        # Header
        st.markdown(f"""
        <div style='text-align:center; padding:40px 0 30px 0;'>
            <div style='font-size:52px; margin-bottom:8px;'>🔮</div>
            <div style='font-size:32px; font-weight:800; color:#C0392B;
                margin-bottom:6px;'>GMA Insight</div>
            <div style='font-size:14px; color:{BRAND["muted"]}; letter-spacing:.5px;'>
                Personalised Admission Intelligence — powered by Get My Admission
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Registration card
        st.markdown(f"""
        <div style='
            background:{BRAND["bg_card"]};
            border:1px solid #1E1E1E;
            border-left:4px solid #C0392B;
            border-radius:20px;
            padding:32px 36px;
            margin-bottom:24px;
        '>
            <div style='font-size:18px; font-weight:700; color:#FFFFFF; margin-bottom:4px;'>
                Register to Get Your Insights
            </div>
            <div style='font-size:13px; color:{BRAND["muted"]}; margin-bottom:24px;'>
                Enter your details once — GMA Insight will personalise everything for you.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Step 1: State picker (outside form so category reacts instantly) ──
        st.markdown(
            f"<div style='font-size:12px; color:{BRAND['muted']}; text-transform:uppercase;"
            f"letter-spacing:1.5px; margin-bottom:8px;'>Personal Details</div>",
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns(2)
        with col1:
            name_pre = st.text_input("Full Name *", placeholder="e.g. Arjun Kumar",
                                     key="pre_name")
        with col2:
            state_pre = st.selectbox(
                "State *",
                ["Kerala", "Tamil Nadu", "Karnataka", "Andhra Pradesh",
                 "Telangana", "Maharashtra", "Delhi", "Uttar Pradesh",
                 "Rajasthan", "Gujarat", "West Bengal", "Other"],
                key="reg_state",
            )

        # Dynamic category list based on chosen state
        cat_options = STATE_CATEGORIES.get(st.session_state.reg_state, CATEGORIES)

        with st.form("registration_form"):
            col3, col4 = st.columns(2)
            with col3:
                category = st.selectbox(
                    f"Category * {'(Kerala CEE)' if st.session_state.reg_state == 'Kerala' else ''}",
                    cat_options,
                )
            with col4:
                exam = st.selectbox("Exam *", ["NEET UG", "KEAM", "NEET PG"])

            st.markdown("<br>", unsafe_allow_html=True)

            # Exam / Rank details
            st.markdown(
                f"<div style='font-size:12px; color:{BRAND['muted']}; text-transform:uppercase;"
                f"letter-spacing:1.5px; margin-bottom:10px;'>Exam &amp; Rank Details</div>",
                unsafe_allow_html=True,
            )
            if st.session_state.reg_state == "Kerala":
                score = 0
                rank = st.number_input("Rank *", min_value=0, max_value=1_000_000, value=0, step=1)
            else:
                col5, col6 = st.columns(2)
                with col5:
                    score = st.number_input("Score (out of 720)", min_value=0, max_value=720, value=0, step=1)
                with col6:
                    rank  = st.number_input("Rank", min_value=0, max_value=1_000_000, value=0, step=1)

            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🔮 Get My Insights →", use_container_width=True)

        if submitted:
            name = st.session_state.get("pre_name", "").strip()
            if not name:
                st.error("Please enter your full name.")
            elif rank <= 0 and score <= 0:
                st.error("Please enter your Rank or Score to get insights.")
            else:
                final_rank  = rank  if rank  > 0 else None
                final_score = score if score > 0 else None
                if not final_rank and final_score:
                    rd = load_rank_distribution()
                    final_rank = score_to_rank(final_score, rd)

                is_kerala = st.session_state.reg_state == "Kerala"
                cat_code  = KERALA_CATEGORY_MAP.get(category, category) if is_kerala else category

                st.session_state.student = {
                    "name":          name,
                    "state":         st.session_state.reg_state,
                    "category":      category,
                    "category_code": cat_code,
                    "exam":          exam,
                    "score":         final_score,
                    "rank":          final_rank,
                }
                st.session_state.registered = True
                st.rerun()

        # Info footer
        st.markdown(
            f"<div style='text-align:center; margin-top:16px; font-size:11px; color:{BRAND['muted']};'>"
            f"🔒 <b>Privacy & Security:</b> Your data is processed securely and is used exclusively to generate your personalised admission insights. We do not store your data permanently, and it will never be shared with or sold to any third parties."
            f"</div>",
            unsafe_allow_html=True,
        )



# ════════════════════════════════════════════════════════════════════════════
# SCREEN 2 — INSIGHTS FEED
# ════════════════════════════════════════════════════════════════════════════
def show_insights_feed():
    s        = st.session_state.student
    insights = _load_manual_insights()   # ← admin panel controlled (runtime_config.json)

    # ── Exam-based Audience Filtering ────────────────────────────────────────
    # Each insight carries a `target_exam` field set by the admin.
    # "All Students" → visible to everyone.
    # Any other value (e.g. "KEAM", "NEET UG") → visible only to students
    # who registered with that exact exam.
    student_exam = s.get("exam", "")   # e.g. "NEET UG", "KEAM", "NEET PG"
    insights = [
        item for item in insights
        if item.get("target_exam", "All Students") in ("All Students", student_exam)
    ]

    # ── Extract Backend Published Poll Insight ──
    # We extract it globally so it doesn't render in the generic insights loop if the poll is deleted!
    poll_insight = None
    remaining_insights = []
    if insights:
        for item in insights:
            if "Poll" in item.get("title", ""):
                poll_insight = item
            else:
                remaining_insights.append(item)
        
        insights.clear()
        insights.extend(remaining_insights)


    # ── Computed display values ───────────────────────────────────────────────
    rank_display  = f"{s['rank']:,}" if s.get("rank")  else "–"
    score_display = str(s["score"])  if s.get("score") else "–"

    # ── Top bar ───────────────────────────────────────────────────────────────
    st.markdown(
        f"<div style='background:{BRAND['bg_card']};"
        f"border-bottom:2px solid #C0392B44; padding:16px 20px;"
        f"display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:16px;"
        f"position:sticky; top:0; z-index:100;'>"
        
        f"<div style='display:flex; align-items:center; gap:12px;'>"
        f"<div style='font-size:26px;'>🔮</div>"
        f"<div>"
        f"<div style='font-size:18px; font-weight:800; color:#C0392B;'>GMA Insight</div>"
        f"<div style='font-size:11px; color:{BRAND['muted']};'>Get My Admission</div>"
        f"</div></div>"
        
        f"<div style='display:flex; align-items:center; gap:12px; flex-wrap:wrap;'>"
        f"<div style='text-align:left;'>"
        f"<div style='font-size:14px; font-weight:700; color:#FFFFFF;'>{s['name']}</div>"
        f"<div style='font-size:11px; color:{BRAND['muted']};'>{s['exam']} &nbsp;·&nbsp; {s['category']} &nbsp;·&nbsp; {s['state']}</div>"
        f"</div>"
        f"<div style='display:flex; gap:6px;'>"
        f"<span style='background:rgba(76,175,80,0.12); color:#4CAF50;"
        f"padding:4px 10px; border-radius:20px; font-size:12px; font-weight:700;"
        f"border:1px solid rgba(76,175,80,0.35);'>Rank {rank_display}</span>"
        f"<span style='background:rgba(76,175,80,0.12); color:#4CAF50;"
        f"padding:4px 10px; border-radius:20px; font-size:12px; font-weight:700;"
        f"border:1px solid rgba(76,175,80,0.35);'>Score {score_display}</span>"
        f"</div></div></div>",
        unsafe_allow_html=True,
    )

    # ── Main content ──────────────────────────────────────────────────────────
    _, main, _ = st.columns([0.3, 9, 0.3])
    with main:
        st.markdown("<br>", unsafe_allow_html=True)

        # ── Quick Insight (Conversational Header) ─────────────────────────
        is_kerala  = s["state"] == "Kerala"
        final_rank = s.get("rank")
        cat_code   = s.get("category_code", "")

        if is_kerala and final_rank:
            import re as _re
            qi      = get_quick_insight(final_rank, cat_code)
            choices = qi["better_choices"]
            gov     = [c for c in choices if c["college_type"] == "Government"]
            priv    = [c for c in choices if c["college_type"] == "Private"]

            def _clean(n):
                return _re.sub(r"^[A-Z]{2,4}[-:\s]+", "", n).strip()

            if gov:
                g_names = " and ".join(f"<b style='color:#C0392B;'>{_clean(c['college'])}</b>" for c in gov[:2])
                g_fee   = f"₹{gov[0]['total_fee']:,.0f}" if gov[0]["total_fee"] else "very low fees"
                para1 = (
                    f"Based on your rank of <b style='color:#C0392B;'>{final_rank:,}</b>, "
                    f"you have a solid chance at securing a seat in government institutions like {g_names}. "
                    f"These colleges offer excellent infrastructure and faculty, with total course fees structured as low as "
                    f"<b style='color:#C0392B;'>{g_fee}</b>. "
                    f"This is a genuinely strong and achievable option that you should prioritize during your choice filling."
                )
            else:
                para1 = (
                    f"With a rank of <b style='color:#C0392B;'>{final_rank:,}</b>, "
                    f"securing a government college seat in the general quotas will be highly competitive. "
                    f"However, there are still excellent pathways available. Your strategy should shift towards identifying "
                    f"the right private colleges that balance strong academics with a budget you are comfortable with."
                )

            if priv:
                p_names = " and ".join(f"<b style='color:#C0392B;'>{_clean(c['college'])}</b>" for c in priv[:2])
                p_fee   = f"₹{priv[0]['total_fee']:,.0f}" if priv[0]["total_fee"] else "fees vary by college"
                para2 = (
                    f"Looking at the private sector, colleges such as {p_names} recorded "
                    f"allotments at ranks very close to yours during the 2025 Kerala counselling rounds. "
                    f"If you decide to pursue a seat in a private medical college, you should plan for a total investment of approximately "
                    f"<b style='color:#C0392B;'>{p_fee}</b> for the full duration of your MBBS course."
                )
            else:
                para2 = ""

            para3 = (
                f"Below, you'll find the latest updates and insights posted by the GMA team. "
                f"Check back often as the admission process progresses."
            )

            hist = qi.get("historical_match")
            if hist:
                h_rank = hist["historical_rank"]
                h_col = _clean(hist["college"])
                h_cat = hist["category"]
                para_hist = (
                    f"<b>Historic Match</b>: Last year, a student with a highly similar rank of "
                    f"<b style='color:#C0392B;'>{h_rank:,}</b> (in the {h_cat} category) secured a seat at "
                    f"<b style='color:#C0392B;'>{h_col}</b>. This is a strong indicator of what you might expect."
                )
                para_hist_html = f"<p style='font-size:15px; color:{BRAND['muted']}; line-height:2; margin-bottom:20px;'>{para_hist}</p>"
            else:
                para_hist_html = ""

            para2_html = f"<p style='font-size:15px; color:{BRAND['muted']}; line-height:2; margin-bottom:20px;'>{para2}</p>" if para2 else ""
            para3_html = f"<p style='font-size:15px; color:{BRAND['muted']}; line-height:2; margin:0;'>{para3}</p>"

            st.markdown(
                f"<div style='background:{BRAND['bg_card']}; border:1px solid #1E1E1E;"
                f"border-left:4px solid #C0392B; border-radius:16px;"
                f"padding:30px 36px; margin-bottom:24px;'>"
                f"<div style='font-size:20px; font-weight:800; color:#FFFFFF; margin-bottom:16px;'>"
                f"⚡ Quick Insight</div>"
                f"<p style='font-size:15px; color:{BRAND['muted']}; line-height:2; margin-bottom:20px;'>{para1}</p>"
                f"{para2_html}"
                f"{para_hist_html}"
                f"{para3_html}"
                f"</div>",
                unsafe_allow_html=True,
            )

        # ── Exam-Based Community Poll ─────────────────────────────────────────
        poll_file = os.path.join(os.path.dirname(__file__), "poll_responses.json")
        poll_data = []
        if os.path.exists(poll_file):
            try:
                with open(poll_file, "r") as f:
                    poll_data = json.load(f)
            except:
                pass
        
        has_voted = any(p.get("name") == s["name"] for p in poll_data)
        
        # Read poll settings from config
        config_path = os.path.join(os.path.dirname(__file__), "runtime_config.json")
        is_poll_active = False
        try:
            with open(config_path, "r") as f:
                cfg = json.load(f)
                poll_settings = cfg.get("poll_settings", {})
                is_active = poll_settings.get("is_active", False)
                expires_at_str = poll_settings.get("expires_at", "")
                
                if is_active and expires_at_str:
                    expires_dt = datetime.strptime(expires_at_str, "%Y-%m-%d %H:%M:%S")
                    if datetime.now() < expires_dt:
                        is_poll_active = True
        except:
            pass

        p_title = poll_settings.get("title", "📊 Community Poll")
        p_intro = poll_settings.get("intro_content", "Please share your feedback.")
        p_qs = poll_settings.get("questions", ["Overall Exam", "Biology", "Chemistry", "Physics"])
        p_opts = poll_settings.get("options", ["Easy", "Medium", "Difficult"])
        
        has_poll_settings = bool(poll_settings.get("title"))
        
        if is_poll_active and not has_voted:
            # STATE 1: Poll is active, student hasn't voted yet
            st.markdown(
                f"""<style>
                /* ── Poll card wrapper ── */
                @keyframes pollBorderFlow {{
                    0%   {{ background-position: 0%   50%; }}
                    50%  {{ background-position: 100% 50%; }}
                    100% {{ background-position: 0%   50%; }}
                }}
                @keyframes pollGlow {{
                    0%,100% {{ box-shadow: 0 0 24px rgba(192,57,43,0.15), 0 16px 60px rgba(0,0,0,0.5); }}
                    50%     {{ box-shadow: 0 0 48px rgba(192,57,43,0.35), 0 20px 80px rgba(0,0,0,0.6); }}
                }}
                .poll-outer {{
                    position: relative;
                    padding: 2px;
                    border-radius: 28px;
                    background: linear-gradient(120deg, #96201A, #C0392B, #E55347, #C0392B, #96201A);
                    background-size: 300% 300%;
                    animation: pollBorderFlow 5s linear infinite, pollGlow 5s ease-in-out infinite;
                    margin-bottom: 32px;
                }}
                .poll-inner {{
                    background: linear-gradient(150deg, #121512 60%, #0A0C0A 100%);
                    border-radius: 26px;
                    padding: 40px 44px;
                    position: relative;
                    overflow: hidden;
                }}
                .poll-orb {{
                    position: absolute; top: -80px; right: -80px;
                    width: 300px; height: 300px;
                    background: radial-gradient(circle, rgba(192,57,43,0.12) 0%, transparent 70%);
                    border-radius: 50%; pointer-events: none;
                }}

                /* ── Form reset ── */
                [data-testid="stForm"] {{
                    background: transparent !important;
                    border: none !important;
                    padding: 0 !important;
                    box-shadow: none !important;
                }}
                [data-testid="stFormSubmitButton"] > button {{
                    background: linear-gradient(135deg, #96201A, #C0392B, #E55347) !important;
                    color: #FFFFFF !important;
                    border: none !important;
                    border-radius: 14px !important;
                    font-weight: 800 !important;
                    font-size: 15px !important;
                    letter-spacing: 0.5px !important;
                    padding: 14px 28px !important;
                    transition: all 0.3s ease !important;
                    box-shadow: 0 6px 24px rgba(192,57,43,0.4) !important;
                }}
                [data-testid="stFormSubmitButton"] > button:hover {{
                    border: 1px solid rgba(255,255,255,0.05) !important; 
                }}
                </style>""",
                unsafe_allow_html=True
            )

            st.markdown(f"""
            <div class="poll-outer">
              <div class="poll-inner">
                <div class="poll-orb"></div>
                <div style="position:relative;z-index:5;">
                  <div style="display:flex;align-items:center;gap:16px;margin-bottom:10px;">
                    <div style="width:52px;height:52px;border-radius:16px;flex-shrink:0;
                        background:linear-gradient(135deg,#96201A,#C0392B);
                        display:flex;align-items:center;justify-content:center;font-size:26px;
                        box-shadow:0 8px 24px rgba(192,57,43,0.5);">📊</div>
                    <div>
                      <div style="font-size:11px;font-weight:800;letter-spacing:2.5px;
                          color:#C0392B;text-transform:uppercase;margin-bottom:4px;">
                        <span style="display:inline-block;width:7px;height:7px;border-radius:50%;
                            background:#C0392B;box-shadow:0 0 8px #C0392B;margin-right:7px;
                            vertical-align:middle;"></span>Live Community Poll
                      </div>
                      <div style="font-size:22px;font-weight:900;color:#FFFFFF;line-height:1.2;">
                        {p_title}
                      </div>
                    </div>
                  </div>
                  <div style="height:1px;background:linear-gradient(90deg,rgba(192,57,43,0.5),transparent);
                      margin:20px 0 24px 0;"></div>
                  <div style="font-size:15px;color:#FFFFFF;line-height:1.75;margin-bottom:8px;">
                    {p_intro}
                  </div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            with st.form("exam_poll_form"):
                responses = {}
                ICONS = ["🧬","⚗️","⚡","📐","📝","🔬","📊","🎯"]
                for qi_idx, q in enumerate(p_qs):
                    icon = ICONS[qi_idx % len(ICONS)]
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:12px;
                        margin-bottom:14px;margin-top:{'0' if qi_idx==0 else '12px'};">
                      <div style="width:36px;height:36px;border-radius:10px;flex-shrink:0;
                          background:rgba(192,57,43,0.15);border:1px solid rgba(192,57,43,0.4);
                          display:flex;align-items:center;justify-content:center;font-size:18px;">{icon}</div>
                      <div style="font-size:15px;font-weight:700;color:#FFFFFF;">{q}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    responses[q] = st.radio(f"Rate {q}:", p_opts, horizontal=True, label_visibility="collapsed")
                    st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

                st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("🗳️  Cast My Vote", use_container_width=True)
                if submitted:
                    responses["name"] = s["name"]
                    poll_data.append(responses)
                    with open(poll_file, "w") as f:
                        json.dump(poll_data, f, indent=4)
                    st.success("✅ Your vote has been recorded. Thank you!")
                    st.rerun()

        elif has_voted or (not is_poll_active and has_poll_settings and len(poll_data) > 0):
            # STATE 2: Show results (either live because they voted, or final because it's closed)
            status_msg = "Thank you for voting! Here is how the community is currently voting." if is_poll_active else f"The poll has officially closed. Here is how the community voted based on {len(poll_data)} responses."
            
            # Calculate metrics
            total_votes = len(poll_data)
            metrics = {q: {opt: 0 for opt in p_opts} for q in p_qs}
            for p in poll_data:
                for q in p_qs:
                    vote = p.get(q, p_opts[0] if p_opts else "N/A")
                    if vote in metrics[q]:
                        metrics[q][vote] += 1
                    else:
                        metrics[q][vote] = 1
            
            # Build the ENTIRE card as one HTML string so it renders inside the dark container
            html = f"""<div style='background: linear-gradient(145deg, #121512, #0A0C0A); border: 1px solid rgba(255,255,255,0.08); border-radius: 24px; padding: 40px; margin-bottom: 30px; box-shadow: 0 10px 50px rgba(0,0,0,0.5); position: relative; overflow: hidden;'>
<div style='position: absolute; top: -80px; left: -80px; width: 250px; height: 250px; background: radial-gradient(circle, rgba(192,57,43,0.15) 0%, transparent 70%); border-radius: 50%; pointer-events: none;'></div>
<div style='position: absolute; bottom: -80px; right: -80px; width: 300px; height: 300px; background: radial-gradient(circle, rgba(76,175,80,0.1) 0%, transparent 70%); border-radius: 50%; pointer-events: none;'></div>
<div style='position: relative; z-index: 10;'>
<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;'>
<div style='font-size:14px; font-weight:800; letter-spacing:2px; color:#C0392B; text-transform:uppercase;'>📊 {'Live Polling Data' if is_poll_active else 'Final Polling Data'}</div>
<div style='background: rgba(192,57,43,0.15); border: 1px solid rgba(192,57,43,0.3); padding: 6px 14px; border-radius: 20px; color: #FFFFFF; font-size: 13px; font-weight: 700; box-shadow: 0 4px 12px rgba(192,57,43,0.2);'>🗳️ {total_votes} Response{'s' if total_votes != 1 else ''}</div>
</div>
<div style='font-size:32px; font-weight:800; color:#FFFFFF; margin-bottom:10px; line-height: 1.2;'>📌 Community Poll Results</div>
<div style='font-size:16px; color:{BRAND['muted']}; margin-bottom:36px;'>{status_msg}</div>
"""
            
            for q in p_qs:
                html += f"""<div style='margin-bottom:32px;'>
<div style='display: flex; align-items: center; margin-bottom: 16px;'>
<div style='background: rgba(255,255,255,0.05); width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 12px; font-size: 18px; border: 1px solid rgba(255,255,255,0.1);'>📋</div>
<div style='font-size:18px; font-weight:700; color:#FFFFFF;'>{q}</div>
</div>
"""
                for opt in p_opts:
                    count = metrics[q].get(opt, 0)
                    pct = (count / total_votes * 100) if total_votes > 0 else 0
                    is_majority = count == max(metrics[q].values()) and count > 0
                    
                    if is_majority:
                        bar_bg = "linear-gradient(90deg, #96201A, #C0392B, #E55347)"
                        label_color = "#FFFFFF"
                        pct_color = "#FFFFFF"
                        row_bg = "rgba(192,57,43,0.1)"
                        row_border = "1px solid rgba(192,57,43,0.4)"
                        icon = "🏆 "
                        fw = "700"
                    else:
                        bar_bg = "#2A2A2A"
                        label_color = "#B0BEC5"
                        pct_color = "#B0BEC5"
                        row_bg = "transparent"
                        row_border = "1px solid transparent"
                        icon = ""
                        fw = "500"
                    
                    html += f"""<div style='background:{row_bg}; border:{row_border}; border-radius:10px; padding:12px 14px; margin-bottom:10px;'>
<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
<span style='font-size:14px; font-weight:{fw}; color:{label_color};'>{icon}{opt}</span>
<span style='font-size:14px; font-weight:700; color:{pct_color};'>{pct:.1f}%&nbsp;<span style='font-size:12px; color:{BRAND['muted']}; font-weight:400;'>({count})</span></span>
</div>
<div style='background:#0A0C0A; border-radius:6px; height:8px; overflow:hidden;'>
<div style='background:{bar_bg}; width:{pct}%; height:100%; border-radius:6px; transition:width 1.2s ease-in-out;'></div>
</div>
</div>
"""
                
                html += "</div>"  # close question block
                
            # ── Inject Backend Published Poll Insight ──
            # We use the globally extracted poll_insight from the top of the function.
            
            if poll_insight:
                raw_content = poll_insight.get("content", "")
                import re
                # Convert Markdown to HTML for the div
                raw_content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', raw_content)
                raw_content = raw_content.replace('\n', '<br>')
                
                html += f"""
                <style>
                @keyframes insightPulse {{
                    0% {{ box-shadow: 0 0 15px rgba(192,57,43,0.1), inset 0 0 20px rgba(192,57,43,0.05); }}
                    50% {{ box-shadow: 0 0 30px rgba(192,57,43,0.3), inset 0 0 40px rgba(192,57,43,0.1); }}
                    100% {{ box-shadow: 0 0 15px rgba(192,57,43,0.1), inset 0 0 20px rgba(192,57,43,0.05); }}
                }}
                @keyframes borderFlow {{
                    0% {{ background-position: 0% 50%; }}
                    50% {{ background-position: 100% 50%; }}
                    100% {{ background-position: 0% 50%; }}
                }}
                </style>
                
                <div style='margin-top: 48px; position: relative; padding: 2px; border-radius: 24px; background: linear-gradient(90deg, #96201A, #C0392B, #E55347, #C0392B, #96201A); background-size: 300% auto; animation: borderFlow 4s linear infinite, insightPulse 4s ease-in-out infinite;'>
                    <div style='background: rgba(10,12,10,0.97); backdrop-filter: blur(24px); border-radius: 22px; padding: 36px 40px; position: relative; overflow: hidden;'>
                        
                        <!-- Glowing Orb Background -->
                        <div style='position: absolute; top: -50px; right: -50px; width: 200px; height: 200px; background: radial-gradient(circle, rgba(192,57,43,0.15) 0%, transparent 70%); border-radius: 50%; pointer-events: none;'></div>
                        
                        <!-- Header Section -->
                        <div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px;'>
                            <div style='display: flex; align-items: center;'>
                                <div style='background: linear-gradient(135deg, #C0392B, #1B5E20); width: 48px; height: 48px; border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 8px 24px rgba(192,57,43,0.4); margin-right: 20px;'>
                                    ✨
                                </div>
                                <div>
                                    <div style='font-size: 12px; font-weight: 800; letter-spacing: 2.5px; text-transform: uppercase; color: #C0392B; margin-bottom: 6px; display: flex; align-items: center;'>
                                        <span style='display: inline-block; width: 6px; height: 6px; background: #C0392B; border-radius: 50%; margin-right: 8px; box-shadow: 0 0 10px #C0392B;'></span>
                                        Verified GMA Insight
                                    </div>
                                    <div style='font-size: 24px; font-weight: 800; color: #FFFFFF; line-height: 1.2;'>
                                        {poll_insight.get('title', 'Community Insight')}
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Content Section -->
                        <div style='font-size: 16px; color: #FFFFFF; line-height: 1.9; font-weight: 500; background: rgba(255,255,255,0.02); padding: 28px 32px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); position: relative;'>
                            <div style='position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: linear-gradient(180deg, #96201A, #C0392B, #E55347); border-radius: 4px 0 0 4px;'></div>
                            {raw_content}
                        </div>
                        
                    </div>
                </div>
                """
            
            html += "</div>"  # close card
            
            # Minify HTML: remove all newlines and leading spaces so Streamlit doesn't parse it as markdown code blocks!
            import re
            minified_html = re.sub(r'\n\s*', ' ', html)
            
            st.markdown(minified_html, unsafe_allow_html=True)


        # ── Render Custom Manual Insights ─────────────────────────────────────
        # Inject keyframe animations once
        st.markdown("""
        <style>
        @keyframes borderFlow {
            0%   { background-position: 0%   50%; }
            50%  { background-position: 100% 50%; }
            100% { background-position: 0%   50%; }
        }
        @keyframes insightGlow {
            0%   { box-shadow: 0 0 20px rgba(79,142,247,0.08), 0 8px 40px rgba(0,0,0,0.4); }
            50%  { box-shadow: 0 0 40px rgba(79,142,247,0.22), 0 12px 60px rgba(0,0,0,0.5); }
            100% { box-shadow: 0 0 20px rgba(79,142,247,0.08), 0 8px 40px rgba(0,0,0,0.4); }
        }
        @keyframes badgePulse {
            0%,100% { opacity:1; transform:scale(1); }
            50%     { opacity:0.75; transform:scale(1.08); }
        }
        @keyframes shimmer {
            0%   { transform: translateX(-100%) skewX(-15deg); }
            100% { transform: translateX(250%)  skewX(-15deg); }
        }
        @keyframes fadeInUp {
            from { opacity:0; transform:translateY(22px); }
            to   { opacity:1; transform:translateY(0);    }
        }
        .gma-insight-card {
            animation: fadeInUp 0.55s cubic-bezier(0.22,1,0.36,1) both,
                       insightGlow 5s ease-in-out infinite;
        }
        .gma-insight-card:hover .gma-shimmer {
            animation: shimmer 0.9s ease forwards !important;
        }
        </style>
        """, unsafe_allow_html=True)

        if not insights:
            st.markdown("""
            <div style='text-align:center;padding:60px 24px;background:linear-gradient(145deg,#121512,#0A0C0A);
                border:1px dashed #2A2A2A;border-radius:24px;color:#B0BEC5;
                box-shadow:inset 0 4px 20px rgba(0,0,0,0.3);'>
                <div style='font-size:44px;margin-bottom:14px;'>⏳</div>
                <div style='font-size:17px;font-weight:800;color:#FFFFFF;margin-bottom:8px;'>
                    More Insights Coming Soon
                </div>
                <div style='font-size:14px;line-height:1.7;max-width:340px;margin:0 auto;'>
                    GMA's expert team is actively analysing the data.<br>
                    Stay tuned — updates drop in real time.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            import re

            # Per-card type palette — all borders pure volcano red shades
            TYPE_MAP = {
                "poll":        {"grad":"#96201A,#C0392B,#E55347", "badge":"🗳️ POLL RESULT",   "badge_bg":"rgba(192,57,43,0.18)",  "badge_color":"#E57373", "orb1":"rgba(192,57,43,0.18)",  "orb2":"rgba(150,32,26,0.10)",  "accent":"#C0392B"},
                "result":      {"grad":"#96201A,#C0392B,#E55347", "badge":"📜 RESULT UPDATE",  "badge_bg":"rgba(192,57,43,0.15)",  "badge_color":"#C0392B", "orb1":"rgba(192,57,43,0.15)",  "orb2":"rgba(150,32,26,0.10)",  "accent":"#C0392B"},
                "counselling": {"grad":"#96201A,#C0392B,#E55347", "badge":"📝 COUNSELLING",    "badge_bg":"rgba(192,57,43,0.15)",  "badge_color":"#E57373", "orb1":"rgba(192,57,43,0.18)",  "orb2":"rgba(150,32,26,0.10)",  "accent":"#C0392B"},
                "rank":        {"grad":"#96201A,#C0392B,#E55347", "badge":"🏆 RANK INSIGHT",   "badge_bg":"rgba(192,57,43,0.15)",  "badge_color":"#E57373", "orb1":"rgba(192,57,43,0.18)",  "orb2":"rgba(150,32,26,0.10)",  "accent":"#E57373"},
                "default":     {"grad":"#96201A,#C0392B,#E55347", "badge":"✦ GMA INSIGHT",    "badge_bg":"rgba(192,57,43,0.15)",  "badge_color":"#C0392B", "orb1":"rgba(192,57,43,0.18)",  "orb2":"rgba(150,32,26,0.10)",  "accent":"#C0392B"},
            }

            def _card_type(title_str):
                t = title_str.lower()
                if "poll" in t:       return "poll"
                if "result" in t:     return "result"
                if "counsel" in t:    return "counselling"
                if "rank" in t:       return "rank"
                return "default"

            for card_idx, item in enumerate(insights):
                raw_content = item.get('content', '')
                raw_content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', raw_content)
                raw_content = raw_content.replace('\n', '<br>')

                title       = item.get('title', 'GMA Insight Update')
                target_exam = item.get('target_exam', 'All Students')
                ctype       = _card_type(title)
                P           = TYPE_MAP[ctype]
                grad        = P["grad"]
                anim_delay  = f"{card_idx * 0.12:.2f}s"

                # "For You" badge when insight is exam-specific
                EXAM_PILL_COLORS = {
                    "NEET UG": ("#4CAF50", "rgba(76,175,80,0.18)"),
                    "KEAM":    ("#E57373", "rgba(229,115,115,0.18)"),
                    "NEET PG": ("#C0392B", "rgba(192,57,43,0.18)"),
                }
                if target_exam != "All Students" and target_exam in EXAM_PILL_COLORS:
                    pill_c, pill_bg = EXAM_PILL_COLORS[target_exam]
                    top_right_badge = (
                        f"<div style='display:inline-flex;align-items:center;gap:7px;"
                        f"background:{pill_bg};border:1px solid {pill_c}55;"
                        f"border-radius:30px;padding:5px 14px;'>"
                        f"<span style='font-size:13px;'>🎯</span>"
                        f"<span style='font-size:11px;font-weight:800;letter-spacing:1.5px;"
                        f"color:{pill_c};text-transform:uppercase;'>For You &nbsp;·&nbsp; {target_exam}</span>"
                        f"</div>"
                    )
                else:
                    top_right_badge = (
                        f"<div style='display:inline-flex;align-items:center;gap:7px;"
                        f"background:rgba(76,175,80,0.15);border:1px solid rgba(76,175,80,0.45);"
                        f"border-radius:30px;padding:5px 16px;"
                        f"box-shadow:0 0 12px rgba(76,175,80,0.35);'"
                        f">"
                        f"<span style='width:7px;height:7px;border-radius:50%;background:#4CAF50;"
                        f"box-shadow:0 0 8px #4CAF50, 0 0 16px #4CAF50;display:inline-block;"
                        f"animation:badgePulse 2s ease-in-out infinite;'></span>"
                        f"<span style='font-size:11px;font-weight:800;letter-spacing:2.5px;"
                        f"color:#4CAF50;text-transform:uppercase;"
                        f"text-shadow:0 0 10px rgba(76,175,80,0.8);'>&#10022; NEW</span>"
                        f"</div>"
                    )

                # Truncate a teaser from raw content (first ~160 chars, plain text)
                plain_teaser = re.sub(r'<[^>]+>', '', raw_content)[:155].strip()
                if len(plain_teaser) == 155:
                    plain_teaser += "…"

                card_html = f"""
<div class="gma-insight-card" style="
    position:relative; margin-bottom:36px;
    padding:2px; border-radius:26px;
    background:linear-gradient(120deg,{grad},{grad.split(',')[0]});
    background-size:300% 300%;
    animation: borderFlow 6s linear infinite, insightGlow 5s ease-in-out infinite;
    animation-delay:{anim_delay};
">
  <!-- Inner card -->
  <div style="
    position:relative; overflow:hidden;
    background:linear-gradient(150deg,#161B22 60%,#0D1117 100%);
    border-radius:24px; padding:36px 40px;
  ">

    <!-- Glowing orbs -->
    <div style="position:absolute;top:-70px;left:-70px;width:260px;height:260px;
        background:radial-gradient(circle,{P['orb1']} 0%,transparent 70%);
        border-radius:50%;pointer-events:none;"></div>
    <div style="position:absolute;bottom:-80px;right:-60px;width:300px;height:300px;
        background:radial-gradient(circle,{P['orb2']} 0%,transparent 70%);
        border-radius:50%;pointer-events:none;"></div>

    <!-- Shimmer sweep (activates on hover via CSS) -->
    <div class="gma-shimmer" style="
        position:absolute;top:0;left:0;width:60px;height:100%;
        background:linear-gradient(90deg,transparent,rgba(255,255,255,0.06),transparent);
        pointer-events:none;
        animation:none;
    "></div>

    <!-- Content layer -->
    <div style="position:relative;z-index:5;">

      <!-- Top row: badge + targeted/NEW pill -->
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:22px;flex-wrap:wrap;gap:10px;">
        <div style="
          display:inline-flex;align-items:center;gap:8px;
          background:{P['badge_bg']};
          border:1px solid {P['badge_color']}44;
          border-radius:30px;padding:5px 14px;
        ">
          <span style="width:7px;height:7px;border-radius:50%;background:{P['badge_color']};
              box-shadow:0 0 8px {P['badge_color']};display:inline-block;
              animation:badgePulse 2s ease-in-out infinite;"></span>
          <span style="font-size:11px;font-weight:800;letter-spacing:2px;
              color:{P['badge_color']};text-transform:uppercase;">{P['badge']}</span>
        </div>
        {top_right_badge}
      </div>

      <!-- Title -->
      <div style="font-size:26px;font-weight:900;color:#FFFFFF;
          line-height:1.25;margin-bottom:14px;letter-spacing:-0.3px;">
        {title}
      </div>


      <!-- Full content -->
      <div style="font-size:15.5px;color:#D1D9E0;line-height:1.95;
          font-weight:500;letter-spacing:0.15px;">
        {raw_content}
      </div>

      <!-- Footer ribbon -->
      <div style="display:flex;align-items:center;gap:10px;margin-top:32px;padding-top:20px;
          border-top:1px solid rgba(255,255,255,0.05);">
        <div style="width:32px;height:32px;border-radius:10px;
            background:linear-gradient(135deg,{grad});
            display:flex;align-items:center;justify-content:center;font-size:15px;
            box-shadow:0 4px 14px {P['accent']}44;">🔮</div>
        <div>
          <div style="font-size:12px;font-weight:700;color:#E6EDF3;">GMA Intelligence Team</div>
          <div style="font-size:11px;color:#8B949E;">Verified Admission Insight · Get My Admission</div>
        </div>
        <div style="margin-left:auto;
            background:rgba(76,175,80,0.15);border:1px solid rgba(76,175,80,0.45);
            border-radius:20px;padding:4px 14px;
            font-size:11px;font-weight:800;color:#4CAF50;
            box-shadow:0 0 10px rgba(76,175,80,0.3), 0 0 20px rgba(76,175,80,0.15);
            text-shadow:0 0 8px rgba(76,175,80,0.9);
            animation:badgePulse 2.5s ease-in-out infinite;">&#9679; Live</div>
      </div>

    </div><!-- /content layer -->
  </div><!-- /inner card -->
</div><!-- /gradient border wrapper -->
"""
                minified = re.sub(r'\n\s*', ' ', card_html)
                st.markdown(minified, unsafe_allow_html=True)

        # ── Edit profile link ─────────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        col_l, col_mid, col_r = st.columns([3, 1, 3])
        with col_mid:
            if st.button("✏️ Edit Profile", use_container_width=True):
                st.session_state.registered = False
                st.rerun()

    # Footer
    st.markdown(f"""
    <div style='text-align:center;margin-top:40px;padding:16px;
        border-top:1px solid #21262D;font-size:11px;color:{BRAND["muted"]};'>
        🔮 <b style='color:{BRAND["primary"]};'>GMA Insight</b> &nbsp;·&nbsp;
        Get My Admission &nbsp;·&nbsp; Actionable Admission Intelligence
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# ROUTER — show the right screen
# ════════════════════════════════════════════════════════════════════════════
if not st.session_state.registered:
    show_registration()
else:
    show_insights_feed()
