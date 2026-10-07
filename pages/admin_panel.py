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

/* ── Base ── */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: #0A0C0A !important;
    color: #FFFFFF !important;
}
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main { background-color: #0A0C0A !important; }
.block-container { padding-top: 0 !important; max-width: 100% !important; background: #0A0C0A !important; }
[data-testid="collapsedControl"] { display: none; }
section[data-testid="stSidebar"] { display: none; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }

/* ── All text ── */
p, span, label, div, h1, h2, h3, h4, h5, li { color: #FFFFFF !important; }
.stMarkdown p, .stMarkdown span { color: #FFFFFF !important; }

/* ── Text inputs ── */
.stTextInput input,
.stTextInput > div > div > input {
    background: #181D18 !important;
    color: #FFFFFF !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 10px !important;
    font-size: 14px !important;
}
.stTextInput label { color: #B0BEC5 !important; font-size: 13px !important; font-weight: 600 !important; }
.stTextInput input:focus { border-color: #C0392B !important; box-shadow: 0 0 0 2px rgba(192,57,43,0.2) !important; outline: none !important; }

/* ── Text areas ── */
.stTextArea textarea {
    background: #181D18 !important;
    color: #FFFFFF !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 10px !important;
    font-size: 14px !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextArea label { color: #B0BEC5 !important; font-size: 13px !important; font-weight: 600 !important; }
.stTextArea textarea:focus { border-color: #C0392B !important; box-shadow: 0 0 0 2px rgba(192,57,43,0.2) !important; outline: none !important; }

/* ── Selectbox ── */
.stSelectbox > div > div,
.stSelectbox [data-baseweb="select"] > div {
    background: #181D18 !important;
    color: #FFFFFF !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 10px !important;
}
.stSelectbox label { color: #B0BEC5 !important; font-size: 13px !important; font-weight: 600 !important; }
[data-baseweb="popover"] { background: #181D18 !important; border: 1px solid #2A2A2A !important; border-radius: 10px !important; }
[data-baseweb="option"] { background: #181D18 !important; color: #FFFFFF !important; }
[data-baseweb="option"]:hover { background: #222A22 !important; }
[data-baseweb="select"] svg { fill: #B0BEC5 !important; }

/* ── Radio ── */
.stRadio label { color: #B0BEC5 !important; font-size: 13px !important; }
.stRadio [data-testid="stWidgetLabel"] { color: #FFFFFF !important; font-weight: 600 !important; }
.stRadio > div { gap: 8px !important; }
.stRadio > div > label {
    background: #181D18 !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 8px !important;
    padding: 6px 14px !important;
    color: #B0BEC5 !important;
}
.stRadio > div > label[data-checked="true"],
.stRadio > div > label:has(input:checked) {
    background: rgba(192,57,43,0.15) !important;
    border-color: #C0392B !important;
    color: #FFFFFF !important;
}

/* ── Checkboxes ── */
.stCheckbox label { color: #B0BEC5 !important; }

/* ── Number input ── */
.stNumberInput input {
    background: #181D18 !important;
    color: #FFFFFF !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 10px !important;
}
.stNumberInput label { color: #B0BEC5 !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #121512 !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 12px !important;
    margin-bottom: 8px !important;
}
[data-testid="stExpander"] summary {
    background: #121512 !important;
    color: #FFFFFF !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
}
[data-testid="stExpander"] summary:hover { background: #181D18 !important; }
[data-testid="stExpander"] summary p { color: #FFFFFF !important; font-weight: 600 !important; }
[data-testid="stExpanderDetails"] { background: #121512 !important; padding: 12px 16px !important; }

/* ── Forms ── */
[data-testid="stForm"] {
    background: #121512 !important;
    border: 1px solid #1E1E1E !important;
    border-radius: 14px !important;
    padding: 20px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #C0392B, #1B5E20) !important;
    color: #FFFFFF !important;
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
        
        mode = st.radio("Navigate", ["✍️ Content Management (CMS)", "🎛️ Feed Controls"], horizontal=True, label_visibility="collapsed")

        if mode == "🎛️ Feed Controls":
            st.markdown(
                f"<div style='font-size:18px; font-weight:700; color:{TX}; margin-bottom:6px; margin-top:16px;'>🎛️ Feed Controls</div>"
                f"<div style='font-size:13px; color:{MU}; margin-bottom:24px;'>"
                f"Turn individual sections of the student feed on or off instantly. Changes take effect on the next page load — no restart needed.</div>",
                unsafe_allow_html=True,
            )

            fm = cfg.get("feed_modules", {})
            def fget(k, default=True): return fm.get(k, default)

            SECTIONS = [
                ("quick_insight",             "⚡ Quick Insight",                    "AI-generated rank insight card shown first"),
                ("stats_row",                 "📊 Stats Row",                        "Rank, Govt Options, Private Options tiles"),
                ("countdown",                 "⏰ Countdown Timer",                  "Live deadline countdown (uses Countdown Settings below)"),
                ("counselling_stage_tracker", "🗺️ Counselling Stage Tracker",       "Kerala CEE journey progress bar"),
                ("manual_insights",           "📌 Admin Insight Cards",              "Manual insight paragraphs published via CMS"),
            ]

            with st.form("feed_controls_form"):
                st.markdown(f"<div style='font-size:13px;font-weight:700;color:{TX};margin-bottom:14px;'>Toggle Sections</div>", unsafe_allow_html=True)

                new_fm = {}
                col_a, col_b = st.columns(2)
                for i, (key, label, desc) in enumerate(SECTIONS):
                    col = col_a if i % 2 == 0 else col_b
                    with col:
                        st.markdown(
                            f"<div style='background:#181D18;border:1px solid #2A2A2A;border-radius:10px;"
                            f"padding:10px 14px;margin-bottom:8px;'>"
                            f"<div style='font-size:13px;font-weight:700;color:#FFFFFF;margin-bottom:2px;'>{label}</div>"
                            f"<div style='font-size:11px;color:{MU};'>{desc}</div></div>",
                            unsafe_allow_html=True,
                        )
                        new_fm[key] = st.checkbox(f"Enable", value=fget(key), key=f"fm_{key}")

                st.markdown("<hr style='border-color:#30363D;margin:16px 0;'>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:13px;font-weight:700;color:{TX};margin-bottom:8px;'>🗺️ Counselling Stage Tracker — Current Active Stage</div>", unsafe_allow_html=True)

                STAGE_LABELS = [
                    "0 — 📋 NEET Result (Rank received)",
                    "1 — 📝 CEE Registration (Online reg open)",
                    "2 — 🎯 Choice Filling (Add & lock choices)",
                    "3 — 🔵 Round 1 Allotment (Results published)",
                    "4 — 🟣 Round 2 / Mop-up (Upgrade round)",
                    "5 — 🎓 Final Admission (Report to college)",
                ]
                COUNSELLINGS = ["MCC (AIQ & Deemed)", "Kerala CEE (State Quota)", "KEA (Karnataka)", "TN Medical", "AYUSH (AACCC)"]
                counselling_stages = fget("counselling_stages", {})
                new_counselling_stages = {}
                
                for c_name in COUNSELLINGS:
                    cur_stage = counselling_stages.get(c_name, fget("counselling_current_stage", 2))
                    if not isinstance(cur_stage, int): cur_stage = 2
                    
                    st.markdown(f"<div style='font-size:12px;font-weight:600;color:{TX};margin-bottom:4px;margin-top:10px;'>{c_name}</div>", unsafe_allow_html=True)
                    new_stage_label = st.selectbox(
                        f"Active Stage for {c_name}",
                        STAGE_LABELS,
                        index=cur_stage,
                        label_visibility="collapsed",
                        key=f"stage_{c_name}"
                    )
                    new_counselling_stages[c_name] = STAGE_LABELS.index(new_stage_label)
                
                new_fm["counselling_stages"] = new_counselling_stages


                if st.form_submit_button("💾 Save Feed Controls", use_container_width=True):
                    cfg["feed_modules"] = new_fm
                    save_full_cfg(cfg)
                    st.session_state.flash = "✅ Feed controls saved. Student feed updated immediately."
                    st.rerun()

        elif mode == "✍️ Content Management (CMS)":
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

            # ── Quick Publish Templates ───────────────────────────────────────────
            st.markdown("<br><hr style='border-color:#30363D;'><br>", unsafe_allow_html=True)
            st.markdown(
                f"<div style='font-size:14px; font-weight:600; color:#E57373; margin-bottom:4px;'>⚡ Quick Publish — Kerala Counselling Templates</div>"
                f"<div style='font-size:12px; color:{MU}; margin-bottom:16px;'>Pre-written checklists for Round 1 and Round 2. Click to publish instantly to all NEET UG students.</div>",
                unsafe_allow_html=True,
            )

            TEMPLATES = [
                {
                    "label": "📋 Round 1 Allotment — Document Checklist",
                    "title": "📋 Round 1 Allotment: Document Checklist for Joining",
                    "target_exam": "NEET UG",
                    "content": (
                        "Congratulations on your Round 1 allotment! 🎉 You **must report to your allotted college** within the joining deadline to secure your seat. Bring the following documents in **original + 3 sets of photocopies**:\n\n"
                        "**Identity & Address**\n"
                        "- Aadhaar Card (original + copy)\n"
                        "- Passport-size photographs (minimum 6)\n\n"
                        "**Academic Certificates**\n"
                        "- 10th Standard Marksheet & Certificate\n"
                        "- 12th Standard Marksheet & Certificate (Pass Certificate if available)\n\n"
                        "**NEET Documents**\n"
                        "- NEET UG 2025 Admit Card\n"
                        "- NEET UG 2025 Scorecard / Rank Letter\n\n"
                        "**Kerala CEE Documents**\n"
                        "- Kerala CEE 2025 Allotment Order (printed)\n"
                        "- Kerala CEE 2025 Registration / Application printout\n\n"
                        "**Category Certificates (if applicable)**\n"
                        "- Community / Caste Certificate (SC/ST/OBC/EZ/BH etc.)\n"
                        "- Income Certificate (if applying under EW / EZ category)\n"
                        "- Non-Creamy Layer Certificate (if applicable)\n\n"
                        "**Other**\n"
                        "- Transfer Certificate (TC) from your school/college\n"
                        "- Conduct Certificate\n"
                        "- Migration Certificate (if from outside Kerala Board)\n"
                        "- Medical Fitness Certificate (from a registered medical officer)\n\n"
                        "> ⚠️ **Important:** Failure to report within the deadline will result in **cancellation of your allotment**. Carry all originals — photocopies alone will not be accepted."
                    ),
                },
                {
                    "label": "🔄 Round 2 Upgradation — How It Works + Checklist",
                    "title": "🔄 Round 2 Upgradation: What You Must Do",
                    "target_exam": "NEET UG",
                    "content": (
                        "Round 2 allotment is your chance to **upgrade to a better college**. Here is exactly what you need to know and do:\n\n"
                        "**Step 1 — Arrange Your College Preferences**\n"
                        "Log in to the Kerala CEE portal and **re-order your college choices** with your most preferred college at the top. The system will try to allot you a college higher on your list than your current allotment.\n\n"
                        "**Step 2 — Check Your Round 2 Allotment**\n"
                        "When Round 2 results are published, check if you have received an upgrade. If yes, you **must physically go to the newly allotted college** — you cannot accept it online alone.\n\n"
                        "**Step 3 — Visit the New College in Person**\n"
                        "Go to your **Round 2 allotted college** with all original documents and complete the admission process there. This is mandatory — your Round 1 seat is automatically vacated when you join Round 2.\n\n"
                        "**Step 4 — Documents to Carry for Round 2 Joining**\n"
                        "Bring the following in **original + 3 sets of photocopies**:\n\n"
                        "- Aadhaar Card\n"
                        "- Passport-size photographs (minimum 6)\n"
                        "- 10th & 12th Marksheets and Certificates\n"
                        "- NEET UG 2025 Admit Card & Scorecard\n"
                        "- **Round 2 Allotment Order** (printed from CEE portal)\n"
                        "- Kerala CEE Application printout\n"
                        "- Category / Community Certificate (if applicable)\n"
                        "- Transfer Certificate (TC)\n"
                        "- Conduct Certificate\n"
                        "- Medical Fitness Certificate\n"
                        "- Migration Certificate (if applicable)\n\n"
                        "> ⚠️ **Remember:** If you do not report to your Round 2 college within the deadline, you will **lose both your Round 1 and Round 2 seats**. Do not skip this step.\n\n"
                        "> 💡 **Tip:** If you are satisfied with your Round 1 college, you can choose not to participate in upgradation. Speak to a GMA counsellor if you are unsure."
                    ),
                },
            ]

            t_col1, t_col2 = st.columns(2)
            for i, tmpl in enumerate(TEMPLATES):
                col = t_col1 if i % 2 == 0 else t_col2
                with col:
                    st.markdown(
                        f"<div style='background:#181D18; border:1px solid #30363D; border-left:3px solid #C0392B;"
                        f"border-radius:12px; padding:14px 16px; margin-bottom:12px;'>"
                        f"<div style='font-size:13px; font-weight:700; color:#FFFFFF; margin-bottom:4px;'>{tmpl['label']}</div>"
                        f"<div style='font-size:11px; color:{MU}; margin-bottom:10px;'>Target: {tmpl['target_exam']}</div>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                    if st.button(f"⚡ Publish: {tmpl['label']}", key=f"tmpl_{i}", use_container_width=True):
                        # Avoid duplicates by title
                        existing_titles = [item.get("title", "") for item in insights]
                        if tmpl["title"] in existing_titles:
                            st.warning(f"'{tmpl['title']}' is already published. Edit it from the Published Insights section above.")
                        else:
                            insights.append({
                                "title":       tmpl["title"],
                                "content":     tmpl["content"],
                                "target_exam": tmpl["target_exam"],
                            })
                            save_cfg(insights, st.session_state.admin_name)
                            st.session_state.flash = f"✅ Published: {tmpl['title']}"
                            st.rerun()


            # ── College-Specific Checklist Builder ───────────────────────────────
            st.markdown("<br><hr style='border-color:#30363D;'><br>", unsafe_allow_html=True)
            st.markdown(
                f"<div style='font-size:14px; font-weight:600; color:#4CAF50; margin-bottom:4px;'>🏛️ College-Specific Checklist Builder</div>"
                f"<div style='font-size:12px; color:{MU}; margin-bottom:16px;'>"
                f"Each college in Kerala may have additional document requirements. Enter the college name, the round, "
                f"and any extra documents they specifically ask for — the system will build the complete checklist automatically.</div>",
                unsafe_allow_html=True,
            )

            BASE_DOCS = [
                ("Identity & Address", [
                    "Aadhaar Card (original + copy)",
                    "Passport-size photographs (minimum 6)",
                ]),
                ("Academic Certificates", [
                    "10th Standard Marksheet & Certificate",
                    "12th Standard Marksheet & Certificate (Pass Certificate if available)",
                ]),
                ("NEET Documents", [
                    "NEET UG 2025 Admit Card",
                    "NEET UG 2025 Scorecard / Rank Letter",
                ]),
                ("Kerala CEE Documents", [
                    "Kerala CEE 2025 Allotment Order (printed)",
                    "Kerala CEE 2025 Registration / Application printout",
                ]),
                ("Category Certificates (if applicable)", [
                    "Community / Caste Certificate (SC/ST/OBC/EZ/BH etc.)",
                    "Income Certificate (if applying under EW / EZ category)",
                    "Non-Creamy Layer Certificate (if applicable)",
                ]),
                ("Other", [
                    "Transfer Certificate (TC) from your school/college",
                    "Conduct Certificate",
                    "Migration Certificate (if from outside Kerala Board)",
                    "Medical Fitness Certificate (from a registered medical officer)",
                ]),
            ]

            with st.form("college_checklist_builder"):
                cb_col1, cb_col2 = st.columns(2)
                with cb_col1:
                    college_name = st.text_input(
                        "College Name *",
                        placeholder="e.g. Govt. Medical College, Thrissur",
                    )
                with cb_col2:
                    round_choice = st.selectbox(
                        "Counselling Round *",
                        ["Round 1 Joining", "Round 2 Upgradation Joining", "Mop-up Round Joining"],
                    )

                st.markdown(
                    f"<div style='font-size:12px; color:{MU}; margin:12px 0 6px 0; font-weight:600;'>"
                    f"➕ Additional Documents Required by This College</div>"
                    f"<div style='font-size:11px; color:{MU}; margin-bottom:8px;'>"
                    f"Enter one document per line (e.g. Original Nativity Certificate, Domicile Certificate, Anti-Ragging Affidavit). "
                    f"Leave blank if no extras.</div>",
                    unsafe_allow_html=True,
                )
                extra_docs_raw = st.text_area(
                    "Extra documents",
                    placeholder="Original Nativity Certificate\nAnti-Ragging Affidavit (signed by student and parent)\nIncome Certificate from Village Officer\nCaste Validity Certificate",
                    height=120,
                    label_visibility="collapsed",
                )

                cb_note = st.text_input(
                    "⚠️ Special Note for this college (optional)",
                    placeholder="e.g. Report between 9 AM – 1 PM only. Hostel registration on same day.",
                )

                build_btn = st.form_submit_button("🏗️ Build & Publish Checklist", use_container_width=True)

                if build_btn:
                    if not college_name.strip():
                        st.error("Please enter the college name.")
                    else:
                        # Build content
                        extra_lines = [l.strip() for l in extra_docs_raw.strip().splitlines() if l.strip()]
                        round_emoji = {"Round 1 Joining": "📋", "Round 2 Upgradation Joining": "🔄", "Mop-up Round Joining": "🎯"}.get(round_choice, "📋")
                        pub_title = f"{round_emoji} {college_name.strip()} — {round_choice} Checklist"

                        lines = [
                            f"You have been allotted to **{college_name.strip()}** in **{round_choice}**. "
                            f"Report within the deadline with the following documents in **original + 3 sets of photocopies**:\n"
                        ]
                        for section, docs in BASE_DOCS:
                            lines.append(f"**{section}**")
                            for d in docs:
                                lines.append(f"- {d}")
                            lines.append("")

                        if extra_lines:
                            lines.append(f"**Additional Documents Required by {college_name.strip()}**")
                            for d in extra_lines:
                                lines.append(f"- {d}")
                            lines.append("")

                        lines.append("> ⚠️ **Important:** Carry all originals — photocopies alone will not be accepted. Failure to report within the deadline will result in cancellation of your allotment.")

                        if cb_note.strip():
                            lines.append(f"\n> 📌 **College Note:** {cb_note.strip()}")

                        full_content = "\n".join(lines)

                        existing_titles = [item.get("title", "") for item in insights]
                        if pub_title in existing_titles:
                            st.warning(f"A checklist for '{college_name.strip()}' ({round_choice}) is already published. Edit it from the Published Insights section above.")
                        else:
                            insights.append({
                                "title":       pub_title,
                                "content":     full_content,
                                "target_exam": "NEET UG",
                            })
                            save_cfg(insights, st.session_state.admin_name)
                            st.session_state.flash = f"✅ Published checklist for {college_name.strip()}"
                            st.rerun()

            # ── Allotment Notification Manager ───────────────────────────────────
            st.markdown("<br><hr style='border-color:#30363D;'><br>", unsafe_allow_html=True)
            st.markdown(
                f"<div style='font-size:14px; font-weight:600; color:#4CAF50; margin-bottom:4px;'>🎓 Allotment Notification Card</div>"
                f"<div style='font-size:12px; color:{MU}; margin-bottom:16px;'>"
                f"Publish a live allotment flash card on the student feed. When active, every student sees their allotted college name, "
                f"urgent document reminders, the 2-day memo/data-sheet notice, and a full document checklist at the top of their insight feed.</div>",
                unsafe_allow_html=True,
            )

            cur_allotment = cfg.get("allotment_notification", {})
            is_allotment_active = cur_allotment.get("is_active", False)

            if is_allotment_active:
                cur_college = cur_allotment.get("college_name", "")
                cur_round   = cur_allotment.get("round", "Round 1")
                st.markdown(
                    f"<div style='background:rgba(76,175,80,0.1);border:1px solid rgba(76,175,80,0.35);"
                    f"border-radius:12px;padding:12px 16px;margin-bottom:14px;'>"
                    f"<div style='font-size:12px;font-weight:800;color:#4CAF50;margin-bottom:4px;'>● ACTIVE — Allotment Card is LIVE on Student Feed</div>"
                    f"<div style='font-size:13px;color:#FFFFFF;'>College: <b>{cur_college}</b> &nbsp;·&nbsp; Round: <b>{cur_round}</b></div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
                if st.button("🗑️ Clear Allotment Notification (Hide from Feed)", use_container_width=True, key="clear_allotment"):
                    cfg["allotment_notification"] = {"is_active": False}
                    save_full_cfg(cfg)
                    st.session_state.flash = "Allotment notification cleared from student feed."
                    st.rerun()
                st.markdown("<hr style='border-color:#30363D;'>", unsafe_allow_html=True)

            ROUND_OPTIONS = ["Round 1", "Round 2", "Mop-up Round", "Stray Vacancy Round"]
            ROUND_EMOJIS  = {"Round 1": "📋", "Round 2": "🔄", "Mop-up Round": "🎯", "Stray Vacancy Round": "🃏"}

            with st.form("allotment_notification_form"):
                an_col1, an_col2 = st.columns(2)
                with an_col1:
                    an_college = st.text_input(
                        "Allotted College Name *",
                        value=cur_allotment.get("college_name", ""),
                        placeholder="e.g. Govt. Medical College, Thrissur",
                    )
                with an_col2:
                    default_round_idx = ROUND_OPTIONS.index(cur_allotment.get("round", "Round 1")) if cur_allotment.get("round") in ROUND_OPTIONS else 0
                    an_round = st.selectbox("Counselling Round *", ROUND_OPTIONS, index=default_round_idx)

                st.markdown(
                    f"<div style='font-size:12px; color:{MU}; margin:10px 0 6px 0; font-weight:600;'>"
                    f"➕ College-Specific Extra Documents (one per line)</div>"
                    f"<div style='font-size:11px; color:{MU}; margin-bottom:8px;'>"
                    f"Leave blank to use only the standard document checklist.</div>",
                    unsafe_allow_html=True,
                )
                an_extra_docs = st.text_area(
                    "Extra Documents",
                    value="\n".join(cur_allotment.get("extra_docs", [])),
                    placeholder="Original Nativity Certificate\nAnti-Ragging Affidavit (signed by student and parent)\nIncome Certificate from Village Officer",
                    height=100,
                    label_visibility="collapsed",
                )
                an_note = st.text_input(
                    "📌 Special Note for This College (optional)",
                    value=cur_allotment.get("college_note", ""),
                    placeholder="e.g. Report between 9 AM – 1 PM only. Hostel registration on same day.",
                )

                an_submit = st.form_submit_button("🚀 Publish Allotment Notification to Student Feed", use_container_width=True)
                if an_submit:
                    if not an_college.strip():
                        st.error("Please enter the college name.")
                    else:
                        extra_docs_list = [l.strip() for l in an_extra_docs.strip().splitlines() if l.strip()]
                        cfg["allotment_notification"] = {
                            "is_active":    True,
                            "college_name": an_college.strip(),
                            "round":        an_round,
                            "extra_docs":   extra_docs_list,
                            "college_note": an_note.strip(),
                            "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "published_by": st.session_state.admin_name,
                        }
                        save_full_cfg(cfg)
                        st.session_state.flash = f"✅ Allotment card published — {an_college.strip()} ({an_round})"
                        st.rerun()

            # ── Countdown Deadline Editor ─────────────────────────────────────────
            st.markdown("<br><hr style='border-color:#30363D;'><br>", unsafe_allow_html=True)
            st.markdown(
                f"<div style='font-size:14px; font-weight:600; color:{W}; margin-bottom:8px;'>⏰ Countdown Timer Settings</div>"
                f"<div style='font-size:12px; color:{MU}; margin-bottom:12px;'>Set a deadline that displays a live countdown on the student feed. Leave blank to hide the timer.</div>",
                unsafe_allow_html=True,
            )
            cur_deadline = cfg.get("countdown_deadline", "")
            cur_label    = cfg.get("countdown_label", "Upcoming Deadline")
            cur_icon     = cfg.get("countdown_icon", "⏰")
            with st.form("countdown_form"):
                cd_label = st.text_input("Event Name", value=cur_label, placeholder="e.g. Kerala CEE Round 1 Closes")
                cd_icon  = st.text_input("Icon (emoji)", value=cur_icon, placeholder="⏰")
                cd_deadline = st.text_input("Deadline (YYYY-MM-DD HH:MM:SS)", value=cur_deadline, placeholder="2026-09-30 09:00:00")
                cd_col1, cd_col2 = st.columns(2)
                with cd_col1:
                    cd_save = st.form_submit_button("💾 Save Countdown", use_container_width=True)
                with cd_col2:
                    cd_clear = st.form_submit_button("🗑️ Clear Countdown", use_container_width=True)
                if cd_save:
                    cfg["countdown_deadline"] = cd_deadline.strip()
                    cfg["countdown_label"]    = cd_label.strip()
                    cfg["countdown_icon"]     = cd_icon.strip()
                    save_full_cfg(cfg)
                    st.session_state.flash = "Countdown updated successfully."
                    st.rerun()
                if cd_clear:
                    cfg["countdown_deadline"] = ""
                    save_full_cfg(cfg)
                    st.session_state.flash = "Countdown cleared."
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
