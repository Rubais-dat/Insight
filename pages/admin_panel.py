"""
GMA Insight – Admin Panel
==========================
Password-protected admin dashboard.
Run: streamlit run admin_panel.py --server.port 8502
"""

import streamlit as st
import json, os
from datetime import datetime, timedelta

st.set_page_config(
    page_title="GMA Admin Panel",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR    = os.path.dirname(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "runtime_config.json")
ADMIN_PASSWORD = "gma@admin2026"

# ── Brand palette ─────────────────────────────────────────────────────────────
P  = "#C0392B"   # volcano red
S  = "#1B5E20"   # deep forest green
A  = "#4CAF50"   # forest green (light)
D  = "#C0392B"   # volcano red (danger)
W  = "#E57373"   # soft warm red (warn)
BG = "#0A0C0A"
C1 = "#121512"
C2 = "#181D18"
TX = "#FFFFFF"   # bright white
MU = "#B0BEC5"   # dim white

AVAILABLE_MODULES = [
    ("community",   "📊", "Community Poll Insight",   "Live data from the student post-exam poll."),
    ("result",      "📜", "Result Insight",           "Rank and score distribution analysis."),
    ("rank",        "🏆", "Rank Analysis Insight",    "College possibilities based on 2025 cutoff data."),
    ("counselling", "📝", "Counselling Insight",      "Shortlist and previous round analysis.")
]

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
[data-testid="collapsedControl"] { display: none; }
[data-testid="stAppViewContainer"] { background: #0A0C0A; }
.block-container { padding-top: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }

/* metric cards */
[data-testid="metric-container"] {
    background: #121512 !important;
    border: 1px solid #1E1E1E !important;
    border-left: 3px solid #C0392B !important;
    border-radius: 14px !important;
    padding: 18px 20px !important;
}
[data-testid="stMetricLabel"] { color: #B0BEC5 !important; font-size: 12px !important; }
[data-testid="stMetricValue"] { color: #4CAF50 !important; font-size: 22px !important; font-weight: 800 !important; }

/* inputs */
.stTextInput input {
    background: #181D18 !important;
    color: #FFFFFF !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 10px !important;
    font-size: 14px !important;
}

/* primary button */
.stButton > button {
    background: linear-gradient(135deg, #C0392B, #1B5E20) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(192,57,43,0.4) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def load_cfg():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                return json.load(f)
        except:
            pass
    return {"manual_insights": [], "stage_updated_at": "—", "updated_by": "admin"}

def save_cfg(insights_list, admin):
    # Backward compatibility
    cfg = load_cfg()
    cfg["manual_insights"] = insights_list
    cfg["stage_updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cfg["updated_by"] = admin
    save_full_cfg(cfg)

def save_full_cfg(cfg):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=4)

# ── Session defaults ──────────────────────────────────────────────────────────
for k, v in [("logged_in", False), ("admin_name", ""), ("flash", None)]:
    if k not in st.session_state:
        st.session_state[k] = v


# ════════════════════════════════════════════════════════════════════════════
# LOGIN PAGE
# ════════════════════════════════════════════════════════════════════════════
def page_login():
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='text-align:center; margin-bottom:32px;'>"
            f"<div style='font-size:52px; margin-bottom:10px;'>⚙️</div>"
            f"<div style='font-size:28px; font-weight:800; background:linear-gradient(90deg,{P},{S});"
            f"-webkit-background-clip:text; -webkit-text-fill-color:transparent;'>GMA Insight</div>"
            f"<div style='font-size:13px; color:{MU}; margin-top:4px;'>Admin Content Manager</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
        st.markdown(f"<div style='background:{C1}; border:1px solid #30363D; border-radius:20px; padding:32px 36px;'>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='font-size:17px; font-weight:700; color:{TX}; margin-bottom:4px;'>🔐 Admin Sign In</div>"
            f"<div style='font-size:12px; color:{MU}; margin-bottom:24px;'>Only authorised GMA operators can access this panel.</div>",
            unsafe_allow_html=True,
        )

        with st.form("login_form"):
            name = st.text_input("Your Name", placeholder="e.g. Rubais")
            pwd  = st.text_input("Admin Password", type="password", placeholder="Enter admin password")
            ok   = st.form_submit_button("🔓 Sign In", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        if ok:
            if not name.strip():
                st.error("Please enter your name.")
            elif pwd != ADMIN_PASSWORD:
                st.error("❌ Incorrect password.")
            else:
                st.session_state.logged_in  = True
                st.session_state.admin_name = name.strip()
                st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# DASHBOARD PAGE
# ════════════════════════════════════════════════════════════════════════════
def page_dashboard():
    cfg = load_cfg()
    # Support migration from old config formats safely
    insights = cfg.get("manual_insights")
    if not isinstance(insights, list):
        insights = []

    if st.session_state.flash:
        st.success(st.session_state.flash)
        st.session_state.flash = None

    # Top Nav
    st.markdown(
        f"<div style='background:linear-gradient(135deg,{C1},{C2}); border-bottom:1px solid #21262D;"
        f"padding:14px 32px; display:flex; align-items:center; justify-content:space-between;"
        f"position:sticky; top:0; z-index:100;'>"
        f"<div style='display:flex; align-items:center; gap:12px;'>"
        f"<div style='font-size:24px;'>⚙️</div>"
        f"<div>"
        f"<div style='font-size:17px; font-weight:800; background:linear-gradient(90deg,{P},{S});"
        f"-webkit-background-clip:text; -webkit-text-fill-color:transparent;'>GMA Content Manager</div>"
        f"<div style='font-size:11px; color:{MU};'>Operator: <b style='color:{TX};'>"
        f"{st.session_state.admin_name}</b> &nbsp;·&nbsp; Session active</div>"
        f"</div></div>"
        f"<div style='display:flex; align-items:center; gap:10px;'>"
        f"<span style='background:{A}22; color:{A}; padding:4px 14px; border-radius:20px;"
        f"font-size:12px; font-weight:600; border:1px solid {A}44;'>● Live Sync</span>"
        f"</div></div>",
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    _, body, _ = st.columns([1, 8, 1])
    with body:
        
        mode = st.radio("Navigate", ["✍️ Content Management (CMS)", "📊 Live Poll Analytics"], horizontal=True, label_visibility="collapsed")
        
        if mode == "✍️ Content Management (CMS)":
            st.markdown(
                f"<div style='font-size:18px; font-weight:700; color:{TX}; margin-bottom:6px; margin-top:16px;'>✍️ Manage Manual Insights</div>"
                f"<div style='font-size:13px; color:{MU}; margin-bottom:24px;'>"
                f"Add or edit custom insight paragraphs here. They will appear immediately on the student frontend below the rank prediction.</div>",
                unsafe_allow_html=True,
            )

            # ── Existing Insights ─────────────────────────────────────────────────
            EXAM_OPTIONS = ["All Students", "NEET UG", "KEAM", "NEET PG"]
            EXAM_COLORS  = {
                "All Students": ("#C0392B",  "rgba(192,57,43,0.15)"),
                "NEET UG":      ("#4CAF50",  "rgba(76,175,80,0.15)"),
                "KEAM":         ("#E57373",  "rgba(229,115,115,0.15)"),
                "NEET PG":      ("#C0392B",  "rgba(192,57,43,0.15)"),
            }
            if insights:
                st.markdown(f"<div style='font-size:14px; font-weight:600; color:{TX}; margin-bottom:12px;'>Currently Published Insights</div>", unsafe_allow_html=True)
                for idx, item in enumerate(insights):
                    cur_target = item.get("target_exam", "All Students")
                    ec, ebg    = EXAM_COLORS.get(cur_target, EXAM_COLORS["All Students"])
                    audience_tag = (
                        f"<span style='background:{ebg};color:{ec};border:1px solid {ec}44;"
                        f"border-radius:20px;padding:2px 10px;font-size:11px;font-weight:700;"
                        f"margin-left:8px;'>{cur_target}</span>"
                    )
                    with st.expander(f"📌 {item.get('title', 'Untitled')}  ·  {cur_target}", expanded=False):
                        with st.form(f"edit_form_{idx}"):
                            new_title   = st.text_input("Section Title", value=item.get("title", ""))
                            new_content = st.text_area("Content (Supports Markdown)", value=item.get("content", ""), height=150)

                            st.markdown(
                                f"<div style='font-size:12px;color:{MU};margin-bottom:4px;font-weight:600;'"
                                f">🎯 Target Audience — who should see this insight?</div>",
                                unsafe_allow_html=True,
                            )
                            cur_idx     = EXAM_OPTIONS.index(cur_target) if cur_target in EXAM_OPTIONS else 0
                            new_target  = st.selectbox(
                                "Target Exam",
                                EXAM_OPTIONS,
                                index=cur_idx,
                                key=f"target_{idx}",
                                label_visibility="collapsed",
                            )

                            col1, col2 = st.columns(2)
                            with col1:
                                update_btn = st.form_submit_button("💾 Save Changes", use_container_width=True)
                            with col2:
                                delete_btn = st.form_submit_button("🗑️ Delete Section", use_container_width=True)

                            if update_btn:
                                insights[idx] = {
                                    "title":       new_title.strip(),
                                    "content":     new_content.strip(),
                                    "target_exam": new_target,
                                }
                                save_cfg(insights, st.session_state.admin_name)
                                st.session_state.flash = f"Updated '{new_title}' → visible to: {new_target}"
                                st.rerun()
                            if delete_btn:
                                insights.pop(idx)
                                save_cfg(insights, st.session_state.admin_name)
                                st.session_state.flash = "Insight section removed."
                                st.rerun()
            else:
                st.info("No manual insights published yet.")

            st.markdown("<br><hr style='border-color:#30363D;'><br>", unsafe_allow_html=True)

            # ── Add New Insight ───────────────────────────────────────────────────
            st.markdown(f"<div style='font-size:14px; font-weight:600; color:{A}; margin-bottom:12px;'>➕ Add New Insight Section</div>", unsafe_allow_html=True)
            with st.form("new_insight_form", clear_on_submit=True):
                add_title   = st.text_input("Section Title", placeholder="e.g. Important Update for KEAM Counselling")
                add_content = st.text_area("Content (Supports Markdown)", placeholder="Type your custom insight paragraph here...", height=150)

                st.markdown(
                    f"<div style='font-size:12px;color:{MU};margin-top:8px;margin-bottom:4px;font-weight:600;'"
                    f">🎯 Target Audience — who should see this insight?</div>"
                    f"<div style='font-size:11px;color:{MU};margin-bottom:8px;'>"
                    f"Select <b style='color:#E6EDF3;'>All Students</b> to broadcast to everyone, "
                    f"or pick a specific exam to show it only to those students.</div>",
                    unsafe_allow_html=True,
                )
                add_target = st.selectbox(
                    "Target Exam",
                    ["All Students", "NEET UG", "KEAM", "NEET PG"],
                    index=0,
                    label_visibility="collapsed",
                )

                submitted = st.form_submit_button("🚀 Publish New Insight", use_container_width=True)

                if submitted:
                    if add_title.strip() and add_content.strip():
                        insights.append({
                            "title":       add_title.strip(),
                            "content":     add_content.strip(),
                            "target_exam": add_target,
                        })
                        save_cfg(insights, st.session_state.admin_name)
                        st.session_state.flash = f"New insight published → visible to: {add_target}"
                        st.rerun()
                    else:
                        st.error("Title and Content cannot be empty.")
        
        elif mode == "📊 Live Poll Analytics":
            st.markdown(
                f"<div style='font-size:18px; font-weight:700; color:{TX}; margin-bottom:6px; margin-top:16px;'>📊 Live Poll Analytics</div>"
                f"<div style='font-size:13px; color:{MU}; margin-bottom:24px;'>"
                f"View aggregated data from the student post-exam poll and publish a smart cutoff insight.</div>",
                unsafe_allow_html=True,
            )
            
            # ── Poll Control Panel ────────────────────────────────────────────────
            poll_settings = cfg.get("poll_settings", {})
            is_active = poll_settings.get("is_active", False)
            expires_at_str = poll_settings.get("expires_at", "")
            
            # Check if automatically expired
            if is_active and expires_at_str:
                try:
                    expires_dt = datetime.strptime(expires_at_str, "%Y-%m-%d %H:%M:%S")
                    if datetime.now() >= expires_dt:
                        is_active = False
                        cfg["poll_settings"]["is_active"] = False
                        save_full_cfg(cfg)
                except:
                    pass
            
            st.markdown(f"<div style='font-size:16px; font-weight:700; color:{TX}; margin-bottom:12px;'>Poll Master Switch</div>", unsafe_allow_html=True)
            if not is_active:
                st.info("The poll is currently INACTIVE. Design your poll below and launch it.")
                if poll_settings.get("title"):
                    if st.button("🗑️ Delete Poll Data & Hide Results from Frontend", type="primary", use_container_width=True):
                        cfg["poll_settings"] = {}
                        save_full_cfg(cfg)
                        
                        poll_file_path = os.path.join(BASE_DIR, "poll_responses.json")
                        with open(poll_file_path, "w") as f:
                            json.dump([], f)
                        st.session_state.flash = "Poll data wiped and hidden from frontend."
                        st.rerun()
                        
                with st.form("poll_designer"):
                    poll_title = st.text_input("Poll Title", value=poll_settings.get("title", "Community Poll"))
                    poll_intro = st.text_area("Intro Content (Markdown)", value=poll_settings.get("intro_content", "Happy to hear your exam is finished! What do you think about the exam overall?"), height=80)
                    
                    st.markdown("**(Optional) Comma-separated list of questions/subjects to ask:**")
                    poll_questions_str = st.text_input("Questions", value=",".join(poll_settings.get("questions", ["Overall Exam", "Biology", "Chemistry", "Physics"])))
                    poll_options_str = st.text_input("Options for all questions", value=",".join(poll_settings.get("options", ["Easy", "Medium", "Difficult"])))
                    
                    if st.form_submit_button("🚀 Launch Dynamic Poll (24 Hrs)", use_container_width=True):
                        cfg["poll_settings"] = {
                            "is_active": True,
                            "expires_at": (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S"),
                            "title": poll_title.strip(),
                            "intro_content": poll_intro.strip(),
                            "questions": [q.strip() for q in poll_questions_str.split(",") if q.strip()],
                            "options": [o.strip() for o in poll_options_str.split(",") if o.strip()]
                        }
                        # Clear old poll responses since schema changed
                        poll_file_path = os.path.join(BASE_DIR, "poll_responses.json")
                        with open(poll_file_path, "w") as f:
                            json.dump([], f)
                        
                        save_full_cfg(cfg)
                        st.rerun()
            else:
                st.success(f"The poll is currently LIVE! It will automatically close at {expires_at_str}.")
                if st.button("🛑 Force Close Poll Now", use_container_width=True):
                    if "poll_settings" not in cfg:
                        cfg["poll_settings"] = {}
                    cfg["poll_settings"]["is_active"] = False
                    cfg["poll_settings"]["expires_at"] = ""
                    save_full_cfg(cfg)
                    st.rerun()            
            st.markdown("<br><hr style='border-color:#30363D;'><br>", unsafe_allow_html=True)
            
            poll_file = os.path.join(BASE_DIR, "poll_responses.json")
            poll_data = []
            if os.path.exists(poll_file):
                try:
                    with open(poll_file, "r") as f:
                        poll_data = json.load(f)
                except:
                    pass
            
            if not poll_data:
                st.info("No poll responses received yet. Refresh to check for new votes.")
                if st.button("🔄 Refresh Data", use_container_width=True):
                    st.rerun()
            else:
                total_votes = len(poll_data)
                
                colA, colB = st.columns([8, 2])
                with colA:
                    st.markdown(f"<div style='font-size:15px; font-weight:700; color:{A};'>Total Responses: {total_votes}</div><br>", unsafe_allow_html=True)
                with colB:
                    if st.button("🔄 Refresh", use_container_width=True):
                        st.rerun()
                
                # Dynamic Metrics Calculation
                poll_questions = poll_settings.get("questions", ["Overall Exam", "Biology", "Chemistry", "Physics"])
                poll_options = poll_settings.get("options", ["Easy", "Medium", "Difficult"])
                
                # Initialize counters for each question and option
                metrics = {q: {opt: 0 for opt in poll_options} for q in poll_questions}
                
                for p in poll_data:
                    for q in poll_questions:
                        # get the user's vote for this question, fallback to first option if missing
                        vote = p.get(q, poll_options[0] if poll_options else "N/A")
                        if vote in metrics[q]:
                            metrics[q][vote] += 1
                        else:
                            # In case option was changed mid-flight
                            metrics[q][vote] = 1
                
                # Render Metric Bars
                for q in poll_questions:
                    st.markdown(f"<div style='font-size:14px; font-weight:600; color:{TX}; margin-bottom:8px;'>{q}</div>", unsafe_allow_html=True)
                    cols = st.columns(len(poll_options) or 1)
                    for idx, opt in enumerate(poll_options):
                        count = metrics[q].get(opt, 0)
                        pct = (count / total_votes * 100) if total_votes > 0 else 0
                        cols[idx].metric(opt, f"{pct:.1f}%")
                    st.markdown("<hr style='border-color:#30363D;'>", unsafe_allow_html=True)
                
                # Generate Conversational Smart Template
                default_template = f"Hey everyone! 🌟 We've just analyzed the live poll responses from **{total_votes} GMA students**, and here is what the community is saying:\n\n"
                
                if poll_questions:
                    first_q = poll_questions[0]
                    first_opt = max(metrics[first_q], key=metrics[first_q].get) if metrics[first_q] else "N/A"
                    default_template += f"When it came to the **{first_q}**, most of you voted for **{first_opt}**. "
                    
                    if len(poll_questions) > 1:
                        default_template += "Breaking it down further: "
                        for idx, q in enumerate(poll_questions[1:]):
                            q_counts = metrics[q]
                            if q_counts:
                                majority_opt = max(q_counts, key=q_counts.get)
                                if idx == len(poll_questions[1:]) - 1 and len(poll_questions) > 2:
                                    default_template += f"and finally, the majority found **{q}** to be **{majority_opt}**."
                                else:
                                    default_template += f"most found **{q}** to be **{majority_opt}**, "
                                    
                    default_template += "\n\nDoes this match your experience?"
                
                default_template += (
                    f"\n\n> **Note:** Kindly calculate your score using the final official answer key. "
                    f"This data is based on GMA user polls and does not claim to represent the entire exam population."
                )
                
                st.markdown(f"<div style='font-size:16px; font-weight:700; color:{A}; margin-top:24px; margin-bottom:12px;'>🚀 Publish Poll Insight</div>", unsafe_allow_html=True)
                with st.form("publish_poll_insight"):
                    poll_title = st.text_input("Insight Title", value=f"Community Poll Results ({total_votes} Responses)")
                    poll_content = st.text_area("Insight Content (Edit as needed)", value=default_template, height=200)
                    if st.form_submit_button("Publish to Student Feed", use_container_width=True):
                        insights.append({"title": poll_title.strip(), "content": poll_content.strip()})
                        save_cfg(insights, st.session_state.admin_name)
                        st.session_state.flash = "Poll insight published to frontend!"
                        st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Sign Out", use_container_width=True):
            st.session_state.logged_in  = False
            st.session_state.admin_name = ""
            st.rerun()

# ── Router ────────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    page_login()
else:
    page_dashboard()
