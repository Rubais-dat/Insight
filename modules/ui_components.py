"""
GMA Insight – UI Components  (Streamlit-safe version)
------------------------------------------------------
All st.markdown calls use single-line string concatenation to avoid
Streamlit's Markdown parser treating CSS `>` or `#` as Markdown syntax.
"""

import streamlit as st
from modules.config import BRAND, CHANCE_COLORS, CHANCE_ICONS, STAGE_LABELS, STAGE_ORDER
from datetime import datetime
import re as _re


# ─────────────────────────────────────────────────────────────────────────────
# Global CSS (called once from app.py)
# ─────────────────────────────────────────────────────────────────────────────
def inject_global_css():
    BG   = BRAND["bg_dark"]
    CARD = BRAND["bg_card"]
    TXT  = BRAND["text"]
    MU   = BRAND["muted"]
    PR   = BRAND["primary"]
    AC   = BRAND["accent"]

    css = (
        "<style>"
        "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');"
        f"html,body,[class*='css']{{font-family:'Inter',sans-serif;background-color:{BG};color:{TXT};}}"
        "#MainMenu,footer{visibility:hidden;}"
        ".block-container{padding-top:1.5rem;padding-bottom:2rem;max-width:1100px;}"
        f"[data-testid='stSidebar']{{background:{BG} !important;border-right:1px solid #1E1E1E;}}"
        "::-webkit-scrollbar{width:6px;}"
        f"::-webkit-scrollbar-track{{background:{BG};}}"
        "::-webkit-scrollbar-thumb{background:#C0392B88;border-radius:3px;}"
        ".stButton>button{background:#C0392B;color:white;border:none;"
        "border-radius:10px;font-weight:600;transition:all .25s cubic-bezier(0.4,0,0.2,1);"
        "box-shadow:0 4px 15px rgba(192,57,43,0.3);}"
        ".stButton>button:hover{opacity:.88;transform:translateY(-1px);box-shadow:0 6px 20px rgba(192,57,43,0.45);}"
        ".stButton>button:active{transform:translateY(0px);}"
        f".stSelectbox>div>div,.stTextInput>div>div>input,.stNumberInput>div>div>input{{background:{CARD} !important;"
        f"color:{TXT} !important;border:1px solid #2A2A2A !important;border-radius:8px !important;transition:border-color .2s;}}"
        f".streamlit-expanderHeader{{background:{CARD} !important;border-radius:8px !important;color:{TXT} !important;}}"
        "@keyframes fadeUp{from{opacity:0;transform:translateY(12px);}to{opacity:1;transform:translateY(0);}}"
        ".gma-card{animation:fadeUp .35s ease both;}"
        f".stTabs [data-baseweb='tab-list']{{background:{CARD} !important;border-radius:12px;padding:4px;gap:2px;border:1px solid #1E1E1E;}}"
        f".stTabs [data-baseweb='tab']{{border-radius:8px !important;color:{MU} !important;font-weight:500;transition:all .2s;}}"
        ".stTabs [aria-selected='true']{background:rgba(192,57,43,0.18) !important;color:#E57373 !important;font-weight:700 !important;}"
        f"[data-testid='stMetric']{{background:{CARD};border:1px solid #1E1E1E;border-left:3px solid #C0392B;"
        "border-radius:12px;padding:12px 16px;transition:border-color .2s,box-shadow .2s;}"
        "[data-testid='stMetric']:hover{border-left-color:#4CAF50;box-shadow:0 4px 20px rgba(76,175,80,0.15);}"
        f"[data-testid='stMetricLabel']{{color:{MU} !important;font-size:12px;}}"
        "[data-testid='stMetricValue']{color:#4CAF50 !important;font-size:24px;font-weight:700;}"
        "@keyframes badgePulse{0%,100%{opacity:1;transform:scale(1);}50%{opacity:.75;transform:scale(1.08);}}"
        "@keyframes borderFlow{0%{background-position:0% 50%;}50%{background-position:100% 50%;}100%{background-position:0% 50%;}}"
        "@keyframes floatUp{0%,100%{transform:translateY(0px);}50%{transform:translateY(-6px);}}"
        "@keyframes fadeInUp{from{opacity:0;transform:translateY(22px);}to{opacity:1;transform:translateY(0);}}"
        "@keyframes shimmer{0%{transform:translateX(-100%) skewX(-15deg);}100%{transform:translateX(250%) skewX(-15deg);}}"
        "</style>"
    )
    st.markdown(css, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# App Header
# ─────────────────────────────────────────────────────────────────────────────
def render_header():
    MU = BRAND["muted"]
    st.markdown(
        f"<div style='background:{BRAND['bg_card']};border:1px solid #1E1E1E;"
        "border-left:4px solid #C0392B;border-radius:16px;padding:24px 28px;"
        "margin-bottom:24px;display:flex;align-items:center;gap:16px;'>"
        "<div style='font-size:40px;line-height:1;'>&#128302;</div>"
        "<div>"
        "<div style='font-size:26px;font-weight:800;color:#C0392B;'>GMA Insight</div>"
        f"<div style='color:{MU};font-size:13px;margin-top:2px;letter-spacing:.5px;'>"
        "Actionable Admission Intelligence &mdash; Personalised for You</div>"
        "</div></div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Stage Timeline
# ─────────────────────────────────────────────────────────────────────────────
def render_stage_timeline(current_stage):
    total = len(STAGE_ORDER)
    current_idx = STAGE_ORDER.index(current_stage)
    MU  = BRAND["muted"]
    PR  = BRAND["primary"]
    AC  = BRAND["accent"]

    dots_html = ""
    for i, stage in enumerate(STAGE_ORDER):
        label = STAGE_LABELS[stage]
        if i < current_idx:
            color, dot = AC, "&#10003;"
        elif i == current_idx:
            color, dot = PR, "&#9679;"
        else:
            color, dot = MU, "&#9675;"
        label_color = color if i == current_idx else MU

        dots_html += (
            "<div style='display:flex;flex-direction:column;align-items:center;min-width:80px;'>"
            f"<div style='width:28px;height:28px;border-radius:50%;background:{color}22;"
            f"border:2px solid {color};display:flex;align-items:center;justify-content:center;"
            f"font-size:12px;color:{color};font-weight:700;'>{dot}</div>"
            f"<div style='font-size:9px;color:{label_color};text-align:center;margin-top:5px;"
            f"max-width:70px;line-height:1.3;'>{label}</div>"
            "</div>"
        )
        if i < total - 1:
            if i == current_idx - 1:
                conn = f"linear-gradient(90deg,{AC},{PR})"
            elif i < current_idx:
                conn = AC
            else:
                conn = "#30363D"
            dots_html += f"<div style='flex:1;height:2px;background:{conn};margin-top:-14px;min-width:10px;'></div>"

    st.markdown(
        f"<div style='background:{BRAND['bg_card']};border:1px solid #30363D;"
        "border-radius:14px;padding:16px 20px;margin-bottom:24px;overflow-x:auto;'>"
        f"<div style='font-size:11px;color:{MU};text-transform:uppercase;letter-spacing:2px;margin-bottom:14px;'>Admission Journey</div>"
        f"<div style='display:flex;align-items:center;gap:0;min-width:600px;'>{dots_html}</div>"
        "</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Animated Rank Percentile Gauge
# ─────────────────────────────────────────────────────────────────────────────
def render_rank_gauge(rank: int, percentile: float, rank_band: str):
    MU    = BRAND["muted"]
    radius = 70
    circ   = 2 * 3.14159 * radius
    offset = circ * (1 - percentile / 100)

    if percentile >= 80:
        gc, glow = "#4CAF50", "rgba(76,175,80,0.4)"
    elif percentile >= 50:
        gc, glow = "#E57373", "rgba(229,115,115,0.4)"
    else:
        gc, glow = "#C0392B", "rgba(192,57,43,0.4)"

    rank_fmt = f"{rank:,}"

    svg = (
        f"<svg width='180' height='180' viewBox='0 0 180 180'>"
        f"<circle cx='90' cy='90' r='{radius}' fill='none' stroke='#1E1E1E' stroke-width='12'/>"
        f"<circle cx='90' cy='90' r='{radius}' fill='none' stroke='{gc}' stroke-width='12' stroke-linecap='round'"
        f" stroke-dasharray='{circ:.1f}' stroke-dashoffset='{offset:.1f}' transform='rotate(-90 90 90)'"
        f" style='filter:drop-shadow(0 0 8px {gc});transition:stroke-dashoffset 1.5s cubic-bezier(0.4,0,0.2,1);'/>"
        f"<text x='90' y='82' text-anchor='middle' font-family='Inter,sans-serif' font-size='28' font-weight='900' fill='{gc}'>{percentile:.1f}%</text>"
        f"<text x='90' y='103' text-anchor='middle' font-family='Inter,sans-serif' font-size='11' font-weight='500' fill='{MU}'>Percentile</text>"
        "</svg>"
    )

    st.markdown(
        "<div style='background:linear-gradient(145deg,#121512,#0D1117);border:1px solid #1E1E1E;"
        "border-radius:20px;padding:28px 20px 20px 20px;text-align:center;margin-bottom:16px;"
        "position:relative;overflow:hidden;'>"
        f"<div style='position:absolute;top:-40px;left:-40px;width:180px;height:180px;"
        f"background:radial-gradient(circle,{glow} 0%,transparent 70%);border-radius:50%;pointer-events:none;'></div>"
        f"<div style='font-size:11px;font-weight:800;letter-spacing:2px;color:{MU};"
        "text-transform:uppercase;margin-bottom:16px;'>Your Rank Percentile</div>"
        f"<div style='position:relative;display:inline-block;animation:floatUp 4s ease-in-out infinite;'>{svg}</div>"
        "<div style='margin-top:12px;'>"
        f"<div style='font-size:22px;font-weight:900;color:#FFFFFF;margin-bottom:4px;'>Rank <span style='color:{gc};'>#{rank_fmt}</span></div>"
        f"<div style='display:inline-block;background:{gc}22;border:1px solid {gc}55;"
        f"border-radius:20px;padding:4px 14px;font-size:12px;font-weight:700;color:{gc};'>{rank_band}</div>"
        "</div></div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Live Countdown Timer
# ─────────────────────────────────────────────────────────────────────────────
def render_countdown(event_name: str, target_date_str: str, icon: str = "&#9200;"):
    MU = BRAND["muted"]
    try:
        target_dt = datetime.strptime(target_date_str, "%Y-%m-%d %H:%M:%S")
        now       = datetime.now()
        diff      = target_dt - now
        if diff.total_seconds() <= 0:
            status = "expired"
            days = hours = mins = secs = 0
        else:
            status    = "active"
            total_sec = int(diff.total_seconds())
            days  = total_sec // 86400
            hours = (total_sec % 86400) // 3600
            mins  = (total_sec % 3600)  // 60
            secs  = total_sec % 60
    except Exception:
        return

    if status == "expired":
        st.markdown(
            f"<div style='background:#121512;border:1px solid #1E1E1E;border-radius:16px;"
            "padding:16px 20px;margin-bottom:16px;text-align:center;opacity:.5;'>"
            f"<div style='font-size:24px;'>{icon}</div>"
            f"<div style='font-size:13px;color:{MU};'>{event_name} &mdash; Event passed</div>"
            "</div>",
            unsafe_allow_html=True,
        )
        return

    def seg(val, label):
        return (
            "<div style='text-align:center;min-width:60px;'>"
            "<div style='font-size:32px;font-weight:900;color:#FFFFFF;"
            "background:rgba(192,57,43,0.12);border:1px solid rgba(192,57,43,0.3);"
            "border-radius:12px;padding:10px 14px;box-shadow:0 4px 16px rgba(192,57,43,0.15);'>"
            f"{val:02d}</div>"
            f"<div style='font-size:10px;font-weight:700;letter-spacing:1.5px;color:{MU};"
            f"text-transform:uppercase;margin-top:6px;'>{label}</div>"
            "</div>"
        )

    sep = "<div style='font-size:28px;font-weight:900;color:#C0392B;padding-top:8px;'>:</div>"
    segments = sep.join([seg(days, "Days"), seg(hours, "Hours"), seg(mins, "Mins"), seg(secs, "Secs")])

    st.markdown(
        "<div style='background:linear-gradient(145deg,#121512,#0D1117);"
        "border:1px solid rgba(192,57,43,0.3);border-radius:20px;padding:24px;margin-bottom:16px;"
        "position:relative;overflow:hidden;'>"
        "<div style='position:absolute;top:-30px;right:-30px;width:150px;height:150px;"
        "background:radial-gradient(circle,rgba(192,57,43,0.1) 0%,transparent 70%);"
        "border-radius:50%;pointer-events:none;'></div>"
        "<div style='display:flex;align-items:center;gap:12px;margin-bottom:16px;'>"
        f"<div style='font-size:28px;'>{icon}</div>"
        "<div>"
        f"<div style='font-size:10px;font-weight:800;letter-spacing:2px;color:#C0392B;text-transform:uppercase;'>Upcoming Deadline</div>"
        f"<div style='font-size:16px;font-weight:700;color:#FFFFFF;'>{event_name}</div>"
        "</div>"
        "<div style='margin-left:auto;background:rgba(76,175,80,0.15);border:1px solid rgba(76,175,80,0.4);"
        "border-radius:20px;padding:4px 12px;font-size:11px;font-weight:800;color:#4CAF50;"
        "animation:badgePulse 2s ease-in-out infinite;'>&#9679; LIVE</div>"
        "</div>"
        f"<div style='display:flex;align-items:flex-start;justify-content:center;gap:12px;'>{segments}</div>"
        "</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Insight Card
# ─────────────────────────────────────────────────────────────────────────────
def insight_card(icon: str, title: str, body: str, tag: str = "", tag_color: str = ""):
    MU   = BRAND["muted"]
    CARD = BRAND["bg_card"]
    color = tag_color or "#C0392B"
    tag_html = (
        f"<span style='background:{color}22;color:{color};font-size:10px;"
        f"font-weight:600;padding:2px 10px;border-radius:20px;letter-spacing:.5px;'>{tag}</span>"
    ) if tag else ""

    st.markdown(
        f"<div class='gma-card' style='background:{CARD};border:1px solid #1E1E1E;"
        "border-left:3px solid #C0392B;border-radius:12px;padding:16px 18px;margin-bottom:12px;"
        "transition:border-color .2s,box-shadow .2s;'>"
        "<div style='display:flex;align-items:flex-start;gap:12px;'>"
        f"<div style='font-size:24px;line-height:1;padding-top:2px;'>{icon}</div>"
        "<div style='flex:1;'>"
        "<div style='display:flex;align-items:center;gap:8px;margin-bottom:6px;'>"
        f"<div style='font-size:14px;font-weight:700;color:#FFFFFF;'>{title}</div>"
        f"{tag_html}"
        "</div>"
        f"<div style='font-size:13px;color:{MU};line-height:1.7;'>{body}</div>"
        "</div></div></div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# College Chance Card
# ─────────────────────────────────────────────────────────────────────────────
def college_chance_card(college, course, category, round_, closing_rank, chance,
                         total_fee=None, gma_rating=None, college_type=None):
    MU    = BRAND["muted"]
    color = CHANCE_COLORS.get(chance, BRAND["primary"])
    icon  = CHANCE_ICONS.get(chance, "&#128309;")

    type_badge = ""
    if college_type and college_type not in ("—", "", None):
        ti = "&#127963;" if "Gov" in str(college_type) else "&#127979;"
        type_badge = (
            f"<span style='background:rgba(255,255,255,0.06);color:{MU};"
            f"font-size:10px;padding:2px 8px;border-radius:10px;border:1px solid #2A2A2A;'>{ti} {college_type}</span>"
        )

    fee_html = (
        f"<div style='font-size:11px;color:{MU};margin-top:6px;'>"
        f"&#128176; Total Fee: <span style='color:#FFFFFF;font-weight:600;'>&#8377;{total_fee:,.0f}</span></div>"
    ) if total_fee else ""

    rating_html = (
        f"<div style='font-size:11px;color:{MU};margin-top:3px;'>"
        f"&#11088; GMA Rating: <span style='color:#FFD700;font-weight:600;'>{gma_rating}</span></div>"
    ) if gma_rating and str(gma_rating) not in ("—", "", "nan", "None") else ""

    st.markdown(
        f"<div class='gma-card' style='background:{BRAND['bg_card']};border:1px solid {color}33;"
        "border-radius:14px;padding:16px 18px;margin-bottom:12px;transition:all .2s;'>"
        "<div style='display:flex;justify-content:space-between;align-items:flex-start;'>"
        "<div style='flex:1;'>"
        f"<div style='font-size:14px;font-weight:700;color:{BRAND['text']};margin-bottom:5px;'>{college}</div>"
        f"<div style='font-size:12px;color:{MU};display:flex;flex-wrap:wrap;gap:6px;align-items:center;'>"
        f"<span>{course}</span><span style='color:#30363D;'>|</span>"
        f"<span>{category}</span><span style='color:#30363D;'>|</span>"
        f"<span>{round_}</span>{type_badge}</div>"
        f"{fee_html}{rating_html}"
        "</div>"
        "<div style='text-align:right;min-width:120px;'>"
        f"<div style='background:{color}22;color:{color};border:1px solid {color}55;"
        "border-radius:20px;padding:4px 12px;font-size:12px;font-weight:700;"
        f"margin-bottom:6px;white-space:nowrap;'>{icon} {chance} Chance</div>"
        f"<div style='font-size:11px;color:{MU};text-align:right;'>"
        f"2025 Closing: <span style='color:{BRAND['text']};font-weight:600;'>{closing_rank:,}</span></div>"
        "</div></div></div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Section Header
# ─────────────────────────────────────────────────────────────────────────────
def section_header(title: str, subtitle: str = ""):
    MU = BRAND["muted"]
    sub = f"<div style='font-size:12px;color:{MU};margin-top:3px;'>{subtitle}</div>" if subtitle else ""
    st.markdown(
        "<div style='margin:24px 0 14px 0;'>"
        f"<div style='font-size:18px;font-weight:700;color:{BRAND['text']};'>{title}</div>"
        f"{sub}</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Empty state
# ─────────────────────────────────────────────────────────────────────────────
def empty_state(message: str = "No data available", icon: str = "&#128269;"):
    MU = BRAND["muted"]
    st.markdown(
        f"<div style='text-align:center;padding:48px 24px;background:{BRAND['bg_card']};"
        "border:1px dashed #30363D;border-radius:16px;'>"
        f"<div style='font-size:36px;margin-bottom:12px;'>{icon}</div>"
        f"<div style='font-size:14px;color:{MU};'>{message}</div>"
        "</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Disclaimer banner
# ─────────────────────────────────────────────────────────────────────────────
def disclaimer_banner(text: str):
    W = BRAND["warn"]
    st.markdown(
        f"<div style='background:{W}11;border:1px solid {W}33;border-radius:10px;"
        f"padding:10px 14px;font-size:12px;color:{W};margin-top:16px;'>&#9888;&nbsp; {text}</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Animated Stats Row
# ─────────────────────────────────────────────────────────────────────────────
def render_stats_row(stats: list):
    """stats: list of dicts — icon, label, value, color (opt), sub (opt)"""
    MU = BRAND["muted"]
    tiles = ""
    for s in stats:
        color = s.get("color", "#4CAF50")
        sub   = s.get("sub", "")
        sub_html = (
            f"<div style='font-size:11px;color:{MU};margin-top:3px;'>{sub}</div>"
        ) if sub else ""
        tiles += (
            f"<div style='flex:1;min-width:130px;background:linear-gradient(145deg,#121512,#0D1117);"
            f"border:1px solid {color}22;border-radius:16px;padding:18px 16px;text-align:center;"
            "transition:all .2s;position:relative;overflow:hidden;'>"
            f"<div style='position:absolute;top:-20px;right:-20px;width:80px;height:80px;"
            f"background:radial-gradient(circle,{color}18 0%,transparent 70%);"
            "border-radius:50%;pointer-events:none;'></div>"
            f"<div style='font-size:24px;margin-bottom:6px;'>{s['icon']}</div>"
            f"<div style='font-size:22px;font-weight:900;color:{color};'>{s['value']}</div>"
            f"<div style='font-size:11px;font-weight:600;color:{MU};text-transform:uppercase;"
            f"letter-spacing:1px;margin-top:4px;'>{s['label']}</div>"
            f"{sub_html}"
            "</div>"
        )
    st.markdown(
        "<div style='display:flex;gap:12px;flex-wrap:wrap;margin-bottom:24px;'>"
        f"{tiles}"
        "</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Smart Action Plan
# ─────────────────────────────────────────────────────────────────────────────
def render_action_plan(rank: int, category_code: str, has_gov_chance: bool, has_priv_chance: bool):
    MU = BRAND["muted"]
    steps = []
    if rank <= 5000:
        steps += [
            ("&#127919;", "Priority Action",  "Fill Government college choices FIRST — your rank is strong enough for top government seats.", "#4CAF50"),
            ("&#128203;", "Choice Strategy",  "Add at least 10 government colleges ordered by preference. Include all districts for maximum coverage.", "#4CAF50"),
            ("&#128176;", "Fee Planning",     "Government colleges offer very low fees (&#8377;5,000&ndash;&#8377;20,000/year). Budget planning is minimal.", "#4CAF50"),
        ]
    elif rank <= 15000:
        steps += [
            ("&#9878;",   "Balanced Strategy", "Mix government and private college choices. Add reachable government options first, then quality private colleges.", "#E57373"),
            ("&#128202;", "Monitor Cutoffs",   "Track previous year closing ranks carefully. Add colleges where your rank is within 10% of closing rank.", "#E57373"),
            ("&#128188;", "Private Backup",    "Keep 3&ndash;5 private college options ready. Prepare for higher fee (~&#8377;30L&ndash;&#8377;60L total) if needed.", "#E57373"),
        ]
    else:
        steps += [
            ("&#127979;", "Private College Focus", "With this rank, private/self-financing colleges are the primary option. Research thoroughly.", "#C0392B"),
            ("&#128269;", "Category Check",        "If you have a reservation certificate (SC/ST/OBC/EZ), additional seats may be available &mdash; verify eligibility.", "#C0392B"),
            ("&#128222;", "GMA Counselling",       "Consider one-on-one counselling to identify the best available options for your specific rank &amp; category.", "#C0392B"),
        ]
    steps += [
        ("&#128196;", "Document Readiness", "Keep originals + 5 photocopies of: 10th/12th marksheets, NEET scorecard, category certificate, Aadhaar, and photos.", MU),
        ("&#128260;", "Stay Flexible",      "Apply for multiple rounds. Many seats open in Round 2 and Mop-up that weren't available in Round 1.", MU),
    ]

    items = ""
    for i, (icon, label, text, color) in enumerate(steps):
        border = "border-top:1px solid #1E1E1E;padding-top:18px;" if i > 0 else ""
        items += (
            f"<div style='display:flex;gap:14px;align-items:flex-start;margin-bottom:18px;{border}'>"
            f"<div style='width:40px;height:40px;border-radius:12px;flex-shrink:0;"
            f"background:{color}18;border:1px solid {color}44;"
            f"display:flex;align-items:center;justify-content:center;font-size:18px;'>{icon}</div>"
            "<div style='flex:1;'>"
            f"<div style='font-size:13px;font-weight:800;color:{color};text-transform:uppercase;"
            f"letter-spacing:.8px;margin-bottom:4px;'>{label}</div>"
            f"<div style='font-size:14px;color:#D1D9E0;line-height:1.65;'>{text}</div>"
            "</div></div>"
        )

    st.markdown(
        "<div style='background:linear-gradient(145deg,#121512,#0D1117);border:1px solid #1E1E1E;"
        "border-radius:20px;padding:28px 30px;margin-bottom:24px;position:relative;overflow:hidden;'>"
        "<div style='position:absolute;top:-50px;right:-50px;width:200px;height:200px;"
        "background:radial-gradient(circle,rgba(76,175,80,0.08) 0%,transparent 70%);"
        "border-radius:50%;pointer-events:none;'></div>"
        "<div style='display:flex;align-items:center;gap:14px;margin-bottom:24px;'>"
        "<div style='width:48px;height:48px;border-radius:16px;flex-shrink:0;"
        "background:#C0392B;"
        "display:flex;align-items:center;justify-content:center;font-size:22px;"
        "box-shadow:0 8px 24px rgba(192,57,43,0.4);'>&#9889;</div>"
        "<div>"
        "<div style='font-size:11px;font-weight:800;letter-spacing:2px;color:#C0392B;"
        "text-transform:uppercase;margin-bottom:3px;'>Personalised For You</div>"
        "<div style='font-size:20px;font-weight:900;color:#FFFFFF;'>What Should You Do Now?</div>"
        "</div></div>"
        f"{items}"
        "</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Allotment Reminder Flash Card
# ─────────────────────────────────────────────────────────────────────────────
def render_allotment_reminder(allotment: dict):
    """
    Prominent top-of-feed card shown when admin publishes an allotment notification.
    Shows college name, round, urgent reminders, memo/data-sheet download notice,
    and the document checklist in a clean layout.
    allotment dict keys: college_name, round, extra_notes, college_note, checklist_items
    """
    if not allotment or not allotment.get("college_name"):
        return

    MU           = BRAND["muted"]
    college_name = allotment.get("college_name", "")
    round_label  = allotment.get("round", "Round 1")
    extra_note   = allotment.get("college_note", "")
    extra_docs   = allotment.get("extra_docs", [])   # college-specific extras

    # Base document checklist (always shown)
    base_docs = [
        ("🪪", "Aadhaar Card", "Original + photocopy"),
        ("📸", "Passport Photographs", "Minimum 6 copies"),
        ("📄", "10th Marksheet & Certificate", "Original + 3 photocopies"),
        ("📄", "12th Marksheet & Certificate", "Original + 3 photocopies"),
        ("🩺", "NEET UG 2025 Admit Card", "Original"),
        ("🏆", "NEET UG 2025 Scorecard / Rank Letter", "Original"),
        ("📋", f"Kerala CEE {round_label} Allotment Order", "Printed from CEE portal"),
        ("📝", "Kerala CEE Application Printout", "Printed from CEE portal"),
        ("📑", "Category / Community Certificate", "If applicable — original + copy"),
        ("📂", "Transfer Certificate (TC)", "From school/college"),
        ("🏥", "Medical Fitness Certificate", "From registered medical officer"),
        ("📃", "Conduct Certificate", "From previous institution"),
    ]
    if extra_docs:
        for d in extra_docs:
            if d.strip():
                base_docs.append(("➕", d.strip(), "Required by this college"))

    # Build checklist HTML
    doc_rows = ""
    for icon, label, sub in base_docs:
        doc_rows += (
            f"<div style='display:flex;align-items:flex-start;gap:10px;"
            f"padding:8px 10px;border-radius:8px;margin-bottom:4px;"
            f"background:rgba(255,255,255,0.03);'>"
            f"<span style='font-size:15px;flex-shrink:0;'>{icon}</span>"
            f"<div>"
            f"<div style='font-size:12px;font-weight:700;color:#FFFFFF;'>{label}</div>"
            f"<div style='font-size:10px;color:{MU};'>{sub}</div>"
            f"</div></div>"
        )

    note_html = ""
    if extra_note:
        note_html = (
            f"<div style='background:#C0392B12;border:1px solid #C0392B44;"
            f"border-radius:10px;padding:10px 14px;margin-top:16px;'>"
            f"<div style='font-size:11px;font-weight:800;color:#C0392B;"
            f"text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;'>📌 College Note</div>"
            f"<div style='font-size:13px;color:#D1D9E0;line-height:1.6;'>{extra_note}</div>"
            f"</div>"
        )

    st.markdown(f"""
<style>
@keyframes allotmentPulse {{
  0%,100% {{ box-shadow: 0 0 0 0 rgba(76,175,80,0); }}
  50%      {{ box-shadow: 0 0 24px 4px rgba(76,175,80,0.22); }}
}}
.allotment-card {{
  animation: allotmentPulse 3s ease-in-out infinite;
}}
</style>
<div class="allotment-card" style="
  background:#0D1117;
  border:1px solid #4CAF5044;
  border-left:4px solid #4CAF50;
  border-radius:20px;
  padding:26px 28px;
  margin-bottom:24px;
  position:relative;overflow:hidden;">

  <div style="position:absolute;top:-40px;right:-40px;width:180px;height:180px;
    background:radial-gradient(circle,rgba(76,175,80,0.08) 0%,transparent 70%);
    border-radius:50%;pointer-events:none;"></div>

  <!-- Header -->
  <div style="display:flex;align-items:center;gap:14px;margin-bottom:20px;flex-wrap:wrap;">
    <div style="width:52px;height:52px;border-radius:16px;flex-shrink:0;
      background:#4CAF50;
      display:flex;align-items:center;justify-content:center;font-size:26px;
      box-shadow:0 6px 20px rgba(76,175,80,0.35);">🎓</div>
    <div style="flex:1;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
        <div style="width:8px;height:8px;border-radius:50%;background:#4CAF50;
          box-shadow:0 0 8px #4CAF50;animation:badgePulse 2s ease-in-out infinite;"></div>
        <div style="font-size:11px;font-weight:800;letter-spacing:2px;color:#4CAF50;
          text-transform:uppercase;">Allotment Received · {round_label}</div>
      </div>
      <div style="font-size:22px;font-weight:900;color:#FFFFFF;line-height:1.2;">
        🎉 Congratulations! You got allotted.
      </div>
    </div>
  </div>

  <!-- College Banner -->
  <div style="background:#4CAF5012;border:1px solid #4CAF5033;border-radius:14px;
    padding:16px 20px;margin-bottom:20px;text-align:center;">
    <div style="font-size:12px;color:{MU};letter-spacing:1px;margin-bottom:6px;">YOUR ALLOTTED COLLEGE</div>
    <div style="font-size:20px;font-weight:900;color:#4CAF50;line-height:1.3;">{college_name}</div>
    <div style="font-size:12px;color:{MU};margin-top:4px;">{round_label} · Kerala CEE 2025</div>
  </div>

  <!-- Urgent Reminders Row -->
  <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:20px;">
    <div style="flex:1;min-width:180px;background:#C0392B12;border:1px solid #C0392B33;
      border-radius:12px;padding:12px 14px;">
      <div style="font-size:18px;margin-bottom:6px;">⚡</div>
      <div style="font-size:12px;font-weight:800;color:#C0392B;margin-bottom:3px;">URGENT — Do This NOW</div>
      <div style="font-size:12px;color:{MU};line-height:1.5;">Gather ALL original documents immediately. Do not wait — the reporting deadline is strict.</div>
    </div>
    <div style="flex:1;min-width:180px;background:#9E9E9E12;border:1px solid #9E9E9E33;
      border-radius:12px;padding:12px 14px;">
      <div style="font-size:18px;margin-bottom:6px;">📥</div>
      <div style="font-size:12px;font-weight:800;color:#FFFFFF;margin-bottom:3px;">Memo & Data Sheet</div>
      <div style="font-size:12px;color:{MU};line-height:1.5;">Your <b style="color:#FFFFFF;">Allotment Memo</b> and <b style="color:#FFFFFF;">Data Sheet</b> will be available to download within <b style="color:#FFFFFF;">2 days</b>. Check your CEE portal regularly.</div>
    </div>
    <div style="flex:1;min-width:180px;background:#9E9E9E12;border:1px solid #9E9E9E33;
      border-radius:12px;padding:12px 14px;">
      <div style="font-size:18px;margin-bottom:6px;">📂</div>
      <div style="font-size:12px;font-weight:800;color:#FFFFFF;margin-bottom:3px;">Arrange Documents in Order</div>
      <div style="font-size:12px;color:{MU};line-height:1.5;">Sort all documents in the <b style="color:#FFFFFF;">same order as the checklist below</b>. Keep originals + 3 photocopies of each.</div>
    </div>
  </div>

  <!-- Divider -->
  <div style="height:1px;background:#1E1E1E;margin-bottom:16px;"></div>

  <!-- Document Checklist -->
  <div style="font-size:12px;font-weight:800;color:{MU};text-transform:uppercase;
    letter-spacing:1.5px;margin-bottom:10px;">📋 Document Checklist — Carry These on Reporting Day</div>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:4px;">
    {doc_rows}
  </div>
  {note_html}
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Live Seat Availability Tracker
# ─────────────────────────────────────────────────────────────────────────────
def render_live_seat_tracker(colleges: list, student_rank: int):
    """
    Shows each reachable college as a live seat-status card.
    Green = safely reachable | Red = tight / borderline | Grey = not reachable.
    """
    if not colleges:
        return
    MU = BRAND["muted"]

    header_html = (
        "<div style='margin-bottom:20px;'>"
        "<div style='display:flex;align-items:center;gap:12px;margin-bottom:6px;'>"
        "<div style='width:10px;height:10px;border-radius:50%;background:#4CAF50;"
        "box-shadow:0 0 8px #4CAF50;display:inline-block;'></div>"
        "<div style='font-size:11px;font-weight:800;letter-spacing:2px;color:#4CAF50;"
        "text-transform:uppercase;'>Live Seat Status — Based on 2025 Kerala CEE Cutoffs</div>"
        "</div>"
        "<div style='font-size:18px;font-weight:800;color:#FFFFFF;margin-bottom:4px;'>Your College Seat Availability</div>"
        f"<div style='font-size:13px;color:{MU};'>Showing reachable colleges based on your rank <b style='color:#FFFFFF;'>{student_rank:,}</b> vs actual 2025 closing ranks.</div>"
        "</div>"
    )
    st.markdown(header_html, unsafe_allow_html=True)

    cards_html = "<div style='max-height:500px; overflow-y:auto; padding-right:8px;'>"
    for c in colleges:
        name      = c.get("college", "Unknown")
        clean     = _re.sub(r"^[A-Z]{2,4}[-:\s]+", "", name).strip()
        cr        = c.get("last_rank", 0)
        col_type  = str(c.get("college_type", "—"))
        fee       = c.get("total_fee")
        is_gov    = "Gov" in col_type
        course    = c.get("course", "MBBS")
        category  = c.get("category", "—")

        # Seat status logic
        if cr == 0:
            status_color, status_label, bar_pct, status_icon = "#9E9E9E", "Data Unavailable", 0, "⚪"
        elif student_rank <= int(cr * 0.85):
            status_color, status_label, bar_pct, status_icon = "#4CAF50", "Safely Reachable", 90, "🟢"
        elif student_rank <= cr:
            status_color, status_label, bar_pct, status_icon = "#E57373", "Borderline", 55, "🔴"
        elif student_rank <= int(cr * 1.15):
            status_color, status_label, bar_pct, status_icon = "#C0392B", "Stretch Goal", 25, "🔴"
        else:
            status_color, status_label, bar_pct, status_icon = "#9E9E9E", "Out of Range", 5, "⚪"

        type_icon = "🏛️" if is_gov else "🏫"
        fee_str   = f"₹{fee:,.0f}" if fee else "Low Fees" if is_gov else "Check College"
        rank_gap  = cr - student_rank
        gap_str   = (f"+{rank_gap:,} buffer" if rank_gap > 0 else f"{rank_gap:,} above cutoff")

        cards_html += (
            f"<div style='background:#121512;border:1px solid {status_color}33;"
            f"border-left:3px solid {status_color};"
            "border-radius:14px;padding:16px 18px;margin-bottom:10px;"
            "position:relative;overflow:hidden;'>"
            f"<div style='position:absolute;top:0;right:0;width:80px;height:80px;"
            f"background:radial-gradient(circle,{status_color}10 0%,transparent 70%);"
            "border-radius:50%;pointer-events:none;'></div>"
            "<div style='display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap;'>"
            "<div style='flex:1;min-width:160px;'>"
            f"<div style='font-size:14px;font-weight:800;color:#FFFFFF;margin-bottom:5px;'>{type_icon} {clean}</div>"
            f"<div style='font-size:11px;color:{MU};display:flex;flex-wrap:wrap;gap:8px;'>"
            f"<span>📚 {course}</span><span style='color:#30363D;'>·</span><span>🏷️ {category}</span><span style='color:#30363D;'>·</span>"
            f"<span>💰 {fee_str}</span>"
            "</div>"
            "</div>"
            "<div style='text-align:right;min-width:120px;'>"
            f"<div style='background:{status_color}18;border:1px solid {status_color}55;"
            f"border-radius:20px;padding:4px 12px;font-size:12px;font-weight:800;"
            f"color:{status_color};margin-bottom:5px;white-space:nowrap;'>{status_icon} {status_label}</div>"
            f"<div style='font-size:11px;color:{MU};text-align:right;'>"
            f"2025 Cutoff: <span style='color:#FFFFFF;font-weight:700;'>{cr:,}</span></div>"
            f"<div style='font-size:10px;color:{status_color};text-align:right;margin-top:2px;'>{gap_str}</div>"
            "</div></div>"
            f"<div style='background:#0A0C0A;border-radius:6px;height:6px;overflow:hidden;margin-top:10px;'>"
            f"<div style='background:{status_color};width:{bar_pct}%;height:100%;border-radius:6px;"
            f"transition:width 1s ease;'></div></div>"
            "</div>"
        )

    cards_html += "</div>"

    st.markdown(
        f"<div style='background:#0D1117;border:1px solid #1E1E1E;border-radius:20px;"
        "padding:24px 26px;margin-bottom:24px;'>"
        + header_html
        + cards_html
        + "</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# NEET Personalised Admission Checklist
# ─────────────────────────────────────────────────────────────────────────────
def render_neet_checklist(rank: int, category_code: str, exam: str):
    """Personalised MBBS/BDS admission checklist based on student's rank."""
    MU = BRAND["muted"]

    # Determine course from rank/context
    is_mbbs = True  # Kerala CEE default is MBBS
    course_label = "MBBS"

    # Build personalised checklist items: (done_color, label, detail)
    # Green = recommended/completed phase | Red = urgent action | Grey = upcoming
    items = []

    # Phase 1 — Always done (they have rank)
    items.append(("#4CAF50", "✅ NEET UG Score & Rank Received",
                  f"Your rank {rank:,} has been recorded. You are eligible to apply for Kerala CEE Counselling.", True))

    items.append(("#4CAF50", "✅ Category Certificate Ready",
                  f"Category: {category_code}. Ensure your original certificate is valid and matches the category used during NEET registration.", True))

    # Phase 2 — Urgent actions (red)
    items.append(("#C0392B", "🔴 Register for Kerala CEE Counselling",
                  "Visit cee.kerala.gov.in and complete counselling registration with required documents and fee payment.", False))

    items.append(("#C0392B", "🔴 Prepare Document Set (5 Copies)",
                  "Keep originals + 5 photocopies of: NEET Scorecard, Class 10 & 12 Marksheets, Category Certificate, Aadhaar, and Passport Photos.", False))

    if rank <= 5000:
        items.append(("#C0392B", "🔴 Fill Government Colleges FIRST",
                      "Your rank is strong. Prioritise all Government medical colleges across all districts before private options.", False))
    elif rank <= 15000:
        items.append(("#C0392B", "🔴 Mix Govt + Private in Choice Filling",
                      "Add reachable government colleges first, then strong private options. Aim for at least 15 choices total.", False))
    else:
        items.append(("#C0392B", "🔴 Research Private/Aided Colleges Thoroughly",
                      "Focus on private and aided colleges. Compare fees, infrastructure, and NMC accreditation status.", False))

    items.append(("#C0392B", "🔴 Add Maximum College Choices",
                  "Always add the maximum allowed number of choices. More choices = better chance of allotment in Round 1.", False))

    # Phase 3 — Upcoming (grey)
    items.append(("#9E9E9E", "⚪ Round 1 Allotment",
                  "Check your allotment result. If allotted, report to the college within the deadline and pay the seat fee.", False))

    items.append(("#9E9E9E", "⚪ Round 2 / Mop-up Round",
                  "If not allotted in Round 1, participate in Round 2. Many seats open in subsequent rounds as students upgrade.", False))

    items.append(("#9E9E9E", "⚪ Final Admission & Reporting",
                  f"After final allotment, report to your {course_label} college with all original documents. Pay first-year fees and complete admission formalities.", False))

    items_html = ""
    for i, (color, label, detail, done) in enumerate(items):
        border_top = "border-top:1px solid #1A1A1A;padding-top:14px;" if i > 0 else ""
        items_html += (
            f"<div style='display:flex;gap:14px;align-items:flex-start;margin-bottom:14px;{border_top}'>"
            f"<div style='width:12px;height:12px;border-radius:50%;background:{color};"
            f"flex-shrink:0;margin-top:4px;box-shadow:0 0 6px {color}88;'></div>"
            "<div style='flex:1;'>"
            f"<div style='font-size:13px;font-weight:800;color:#FFFFFF;margin-bottom:3px;'>{label}</div>"
            f"<div style='font-size:12px;color:{MU};line-height:1.6;'>{detail}</div>"
            "</div></div>"
        )

    urgent_count = sum(1 for c, _, __, ___ in items if c == "#C0392B")
    done_count   = sum(1 for c, _, __, d in items if d)

    st.markdown(
        f"<div style='background:#0D1117;border:1px solid #1E1E1E;"
        "border-radius:20px;padding:24px 26px;margin-bottom:24px;'>"
        "<div style='display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;margin-bottom:18px;'>"
        "<div>"
        "<div style='display:flex;align-items:center;gap:10px;margin-bottom:4px;'>"
        "<div style='width:9px;height:9px;border-radius:50%;background:#C0392B;"
        "box-shadow:0 0 8px #C0392B;'></div>"
        "<div style='font-size:11px;font-weight:800;letter-spacing:2px;color:#C0392B;"
        "text-transform:uppercase;'>Personalised Action Checklist</div>"
        "</div>"
        f"<div style='font-size:18px;font-weight:800;color:#FFFFFF;'>Your MBBS Admission Roadmap</div>"
        "</div>"
        "<div style='display:flex;gap:10px;flex-wrap:wrap;'>"
        f"<span style='background:#4CAF5018;border:1px solid #4CAF5055;"
        f"border-radius:20px;padding:4px 12px;font-size:11px;font-weight:700;color:#4CAF50;'>"
        f"✅ {done_count} Done</span>"
        f"<span style='background:#C0392B18;border:1px solid #C0392B55;"
        f"border-radius:20px;padding:4px 12px;font-size:11px;font-weight:700;color:#C0392B;'>"
        f"🔴 {urgent_count} Urgent</span>"
        "</div></div>"
        f"{items_html}"
        "</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# NEET Counselling Stage Tracker
# ─────────────────────────────────────────────────────────────────────────────
def render_counselling_stage_tracker(rank: int, counselling_name: str = "Kerala CEE", current_stage: int = 2):
    """Shows the counselling journey as a live stage progress bar.
    current_stage: 0-based index set by admin (0=NEET Result … 5=Final Admission)
    """
    MU = BRAND["muted"]

    stages = [
        ("📋", "NEET Result",        "Rank received"),
        ("📝", "CEE Registration",   "Online counselling registration"),
        ("🎯", "Choice Filling",     "Add & lock college choices"),
        ("🔵", "Round 1 Allotment",  "Seat allotment published"),
        ("🟣", "Round 2 / Mop-up",  "Upgrade or fresh allotment"),
        ("🎓", "Final Admission",    "Report to college"),
    ]

    current_idx = max(0, min(current_stage, len(stages) - 1))

    dots_html = ""
    for i, (icon, label, sub) in enumerate(stages):
        if i < current_idx:
            dot_color, ring_color, label_color = "#4CAF50", "#4CAF50", "#4CAF50"
            dot_icon = "✓"
        elif i == current_idx:
            dot_color, ring_color, label_color = "#C0392B", "#C0392B", "#FFFFFF"
            dot_icon = icon
        else:
            dot_color, ring_color, label_color = "#1E1E1E", "#2A2A2A", MU
            dot_icon = icon

        dots_html += (
            f"<div style='display:flex;flex-direction:column;align-items:center;min-width:90px;flex:1;'>"
            f"<div style='width:42px;height:42px;border-radius:50%;background:{dot_color}18;"
            f"border:2px solid {ring_color};"
            f"display:flex;align-items:center;justify-content:center;"
            f"font-size:16px;color:#FFFFFF;font-weight:800;"
            f"{'box-shadow:0 0 12px ' + ring_color + '66;' if i == current_idx else ''}'>"
            f"{dot_icon}</div>"
            f"<div style='font-size:10px;color:{label_color};text-align:center;margin-top:6px;"
            f"font-weight:{'800' if i == current_idx else '500'};max-width:80px;line-height:1.3;'>{label}</div>"
            f"<div style='font-size:9px;color:{MU};text-align:center;margin-top:2px;line-height:1.2;'>{sub}</div>"
            "</div>"
        )
        if i < len(stages) - 1:
            conn_color = "#4CAF50" if i < current_idx else "#1E1E1E"
            dots_html += (
                f"<div style='flex:1;height:2px;background:{conn_color};"
                f"margin-top:-24px;min-width:10px;'></div>"
            )

    current_label = stages[current_idx][1]
    current_sub   = stages[current_idx][2]

    st.markdown(
        f"<div style='background:#0D1117;border:1px solid #1E1E1E;"
        "border-radius:20px;padding:24px 26px;margin-bottom:24px;'>"
        "<div style='display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;margin-bottom:20px;'>"
        "<div>"
        "<div style='display:flex;align-items:center;gap:10px;margin-bottom:4px;'>"
        "<div style='width:9px;height:9px;border-radius:50%;background:#C0392B;"
        "box-shadow:0 0 8px #C0392B;animation:badgePulse 2s ease-in-out infinite;'></div>"
        "<div style='font-size:11px;font-weight:800;letter-spacing:2px;color:#C0392B;"
        "text-transform:uppercase;'>Live Counselling Status</div>"
        "</div>"
        f"<div style='font-size:18px;font-weight:800;color:#FFFFFF;'>{counselling_name} Admission Journey</div>"
        "</div>"
        f"<span style='background:#C0392B18;border:1px solid #C0392B55;"
        f"border-radius:20px;padding:6px 14px;font-size:12px;font-weight:800;color:#C0392B;'>"
        f"Now: {current_label}</span>"
        "</div>"
        f"<div style='display:flex;align-items:center;gap:0;overflow-x:auto;padding-bottom:8px;'>{dots_html}</div>"
        "</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Registration Screen
# ─────────────────────────────────────────────────────────────────────────────
def render_registration():
    """Full registration / landing screen."""
    from modules.config import KERALA_CATEGORY_MAP
    from modules.data_loader import load_rank_distribution, score_to_rank
    from modules.kerala_data import get_all_categories

    MU = BRAND["muted"]

    # Animations
    st.markdown(
        "<style>"
        "@keyframes heroOrb{"
        "0%,100%{transform:scale(1) rotate(0deg);opacity:.18;}"
        "50%{transform:scale(1.2) rotate(180deg);opacity:.30;}}"
        "@keyframes heroPulse{"
        "0%,100%{box-shadow:0 0 40px rgba(192,57,43,0.25);}"
        "50%{box-shadow:0 0 80px rgba(192,57,43,0.55),0 0 120px rgba(192,57,43,0.20);}}"
        "@keyframes heroFadeIn{"
        "from{opacity:0;transform:translateY(28px);}"
        "to{opacity:1;transform:translateY(0);}}"
        "@keyframes pillFloat{"
        "0%,100%{transform:translateY(0px);}"
        "50%{transform:translateY(-4px);}}"
        "@keyframes borderFlow{"
        "0%{background-position:0% 50%;}"
        "50%{background-position:100% 50%;}"
        "100%{background-position:0% 50%;}}"
        ".hero-orb-wrap{position:absolute;top:0;left:50%;transform:translateX(-50%);"
        "width:360px;height:360px;pointer-events:none;overflow:visible;}"
        ".hero-orb-a{position:absolute;top:0;left:0;width:200px;height:200px;"
        "background:radial-gradient(circle,rgba(192,57,43,0.2) 0%,transparent 70%);"
        "border-radius:50%;animation:heroOrb 6s ease-in-out infinite;}"
        ".hero-orb-b{position:absolute;top:40px;right:0;width:160px;height:160px;"
        "background:radial-gradient(circle,rgba(27,94,32,0.15) 0%,transparent 70%);"
        "border-radius:50%;animation:heroOrb 8s ease-in-out infinite reverse;}"
        ".hero-icon-pulse{animation:heroPulse 3s ease-in-out infinite;display:inline-block;}"
        ".reg-pill{display:inline-flex;align-items:center;gap:7px;"
        "background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);"
        "border-radius:30px;padding:7px 16px;font-size:12px;font-weight:600;"
        "color:#D1D9E0;animation:pillFloat 3s ease-in-out infinite;}"
        ".reg-border-card{position:relative;padding:2px;border-radius:24px;"
        "background:linear-gradient(135deg,#96201A,#C0392B,#E55347,#C0392B,#96201A);"
        "background-size:300% 300%;animation:borderFlow 5s linear infinite;margin-bottom:0;}"
        ".reg-border-inner{background:linear-gradient(150deg,#121512 60%,#0A0C0A 100%);"
        "border-radius:22px;padding:28px 32px 20px 32px;position:relative;overflow:hidden;}"
        "</style>",
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([0.8, 2.4, 0.8])
    with center:
        # Hero
        st.markdown(
            "<div style='text-align:center;padding:48px 0 36px 0;"
            "position:relative;animation:heroFadeIn .7s ease both;'>"
            "<div class='hero-orb-wrap'>"
            "<div class='hero-orb-a'></div>"
            "<div class='hero-orb-b'></div>"
            "</div>"
            "<div class='hero-icon-pulse' style='font-size:64px;margin-bottom:14px;"
            "display:block;'>🔮</div>"
            "<div style='font-size:38px;font-weight:900;color:#FFFFFF;margin-bottom:6px;"
            "letter-spacing:-1px;line-height:1.1;'>"
            "GMA <span style='color:#C0392B;'>Insight</span></div>"
            f"<div style='font-size:15px;color:{MU};letter-spacing:.3px;margin-bottom:24px;'>"
            "Personalised Admission Intelligence &nbsp;&mdash;&nbsp; "
            "<span style='color:#E57373;'>powered by Get My Admission</span></div>"
            "<div style='display:flex;flex-wrap:wrap;gap:10px;justify-content:center;"
            "margin-bottom:8px;'>"
            "<span class='reg-pill' style='animation-delay:0s;'>&#127963; 2025 Kerala CEE Data</span>"
            "<span class='reg-pill' style='animation-delay:.4s;'>&#128202; Real Cutoff Analysis</span>"
            "<span class='reg-pill' style='animation-delay:.8s;'>&#9889; Instant Insights</span>"
            "<span class='reg-pill' style='animation-delay:1.2s;'>&#127919; College Match Engine</span>"
            "</div>"
            "</div>",
            unsafe_allow_html=True,
        )

        # Gradient border card header
        st.markdown(
            "<div class='reg-border-card'>"
            "<div class='reg-border-inner'>"
            "<div style='position:absolute;top:-60px;right:-60px;width:200px;height:200px;"
            "background:radial-gradient(circle,rgba(192,57,43,0.10) 0%,transparent 70%);"
            "border-radius:50%;pointer-events:none;'></div>"
            "<div style='display:flex;align-items:center;gap:14px;'>"
            "<div style='width:44px;height:44px;border-radius:14px;flex-shrink:0;"
            "background:linear-gradient(135deg,#96201A,#C0392B);"
            "display:flex;align-items:center;justify-content:center;font-size:22px;"
            "box-shadow:0 6px 20px rgba(192,57,43,0.45);'>&#127891;</div>"
            "<div>"
            "<div style='font-size:19px;font-weight:800;color:#FFFFFF;'>"
            "Get Your Personalised Insights</div>"
            f"<div style='font-size:13px;color:{MU};margin-top:2px;'>"
            "Enter your details once &mdash; everything is personalised for you instantly.</div>"
            "</div>"
            "</div>"
            "</div>"
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

        # Personal details
        st.markdown(
            f"<div style='font-size:11px;font-weight:800;color:{MU};"
            "text-transform:uppercase;letter-spacing:2px;margin-bottom:10px;'>"
            "&#128100; Personal Details</div>",
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Full Name *", placeholder="e.g. Arjun Kumar", key="pre_name")
        with col2:
            st.selectbox("State *", ["Kerala"], key="reg_state")

        cat_options = get_all_categories()

        st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='font-size:11px;font-weight:800;color:{MU};"
            "text-transform:uppercase;letter-spacing:2px;margin-bottom:10px;'>"
            "&#128203; Exam &amp; Rank Details</div>",
            unsafe_allow_html=True,
        )

        with st.form("registration_form"):
            col3, col4 = st.columns(2)
            with col3:
                category = st.selectbox("Category * (Kerala CEE)", cat_options)
            with col4:
                exam = st.selectbox("Exam *", ["NEET UG"])

            st.markdown("<br>", unsafe_allow_html=True)
            col_r, col_s = st.columns(2)
            with col_r:
                rank = st.number_input(
                    "State Rank (leave 0 if unknown) *", min_value=0, max_value=1_000_000, value=0, step=1
                )
            with col_s:
                score = st.number_input(
                    "NEET Score *", min_value=0, max_value=720, value=0, step=1
                )
            selected_courses = st.multiselect(
                "Select Course(s) *",
                ["MBBS", "BDS", "BAMS", "BHMS", "BSMS", "BUMS"],
                default=["MBBS"]
            )
            counsellings = st.multiselect(
                "Select Counselling(s) *",
                ["MCC (AIQ & Deemed)", "Kerala CEE (State Quota)", "KEA (Karnataka)", "TN Medical", "AYUSH (AACCC)"],
                default=["Kerala CEE (State Quota)"]
            )
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button(
                "🔮 Get My Insights →", use_container_width=True
            )

        if submitted:
            name = st.session_state.get("pre_name", "").strip()
            if not name:
                st.error("Please enter your full name.")
            elif not counsellings:
                st.error("Please select at least one counselling.")
            elif not selected_courses:
                st.error("Please select at least one course.")
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
                    "counsellings":  counsellings,
                    "courses":       selected_courses,
                }
                st.session_state.registered = True
                
                # Persist to URL
                st.query_params["reg"] = "1"
                st.query_params["name"] = name
                st.query_params["state"] = st.session_state.reg_state
                st.query_params["category"] = category
                st.query_params["cat_code"] = cat_code
                st.query_params["exam"] = exam
                st.query_params["score"] = final_score or 0
                st.query_params["rank"] = final_rank or 0
                st.query_params["couns"] = ",".join(counsellings)
                st.query_params["courses"] = ",".join(selected_courses)
                
                st.rerun()

        # Trust badges
        st.markdown(
            "<div style='display:flex;gap:8px;flex-wrap:wrap;margin-top:18px;"
            "margin-bottom:6px;justify-content:center;'>"
            "<span style='background:rgba(76,175,80,0.08);"
            "border:1px solid rgba(76,175,80,0.25);border-radius:20px;"
            "padding:5px 14px;font-size:11px;color:#4CAF50;font-weight:600;'>"
            "&#10003; 100% Free</span>"
            f"<span style='background:rgba(255,255,255,0.04);"
            "border:1px solid rgba(255,255,255,0.1);border-radius:20px;"
            f"padding:5px 14px;font-size:11px;color:{MU};font-weight:600;'>"
            "&#128274; No Data Stored</span>"
            f"<span style='background:rgba(255,255,255,0.04);"
            "border:1px solid rgba(255,255,255,0.1);border-radius:20px;"
            f"padding:5px 14px;font-size:11px;color:{MU};font-weight:600;'>"
            "&#128202; 2025 Real Cutoff Data</span>"
            f"<span style='background:rgba(255,255,255,0.04);"
            "border:1px solid rgba(255,255,255,0.1);border-radius:20px;"
            f"padding:5px 14px;font-size:11px;color:{MU};font-weight:600;'>"
            "&#9889; Instant Results</span>"
            "</div>"
            f"<div style='text-align:center;margin-top:10px;font-size:11px;color:{MU};'>"
            "&#128274; <b>Privacy &amp; Security:</b> Your data is used only to generate "
            "your personalised insights and is never stored or shared."
            "</div>",
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
# Sticky Top Bar
# ─────────────────────────────────────────────────────────────────────────────
def render_topbar(student: dict):
    """Sticky header bar with student info and rank/score badges."""
    MU = BRAND["muted"]
    s = student
    rank_display  = f"{s['rank']:,}" if s.get("rank")  else "–"
    score_display = str(s["score"])  if s.get("score") else "–"

    st.markdown(
        f"<div style='background:{BRAND['bg_card']};"
        f"border-bottom:2px solid #C0392B44; padding:16px 20px;"
        f"display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:16px;"
        f"position:sticky; top:0; z-index:100;'>"

        f"<div style='display:flex; align-items:center; gap:12px;'>"
        f"<div style='font-size:26px;'>🔮</div>"
        f"<div>"
        f"<div style='font-size:18px; font-weight:800; color:#C0392B;'>GMA Insight</div>"
        f"<div style='font-size:11px; color:{MU};'>Get My Admission</div>"
        f"</div></div>"

        f"<div style='display:flex; align-items:center; gap:12px; flex-wrap:wrap;'>"
        f"<div style='text-align:left;'>"
        f"<div style='font-size:14px; font-weight:700; color:#FFFFFF;'>{s['name']}</div>"
        f"<div style='font-size:11px; color:{MU};'>{s['exam']} &nbsp;·&nbsp; {s['category']} &nbsp;·&nbsp; {s['state']}</div>"
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


# ─────────────────────────────────────────────────────────────────────────────
# Quick Insight Card
# ─────────────────────────────────────────────────────────────────────────────
def render_quick_insight(student: dict):
    """Conversational insight card shown at the top of the feed for Kerala students."""
    import re as _re2
    from modules.kerala_data import get_quick_insight

    s          = student
    is_kerala  = s["state"] == "Kerala"
    final_rank = s.get("rank")
    cat_code   = s.get("category_code", "")

    if not (is_kerala and final_rank):
        return

    MU = BRAND["muted"]

    qi      = get_quick_insight(final_rank, cat_code)
    choices = qi["better_choices"]
    gov     = [c for c in choices if c["college_type"] == "Government"]
    priv    = [c for c in choices if c["college_type"] == "Private"]

    def _clean(n):
        return _re2.sub(r"^[A-Z]{2,4}[-:\s]+", "", n).strip()

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
        "Below, you'll find the latest updates and insights posted by the GMA team. "
        "Check back often as the admission process progresses."
    )

    hist = qi.get("historical_match")
    if hist:
        h_rank = hist["historical_rank"]
        h_col  = _clean(hist["college"])
        h_cat  = hist["category"]
        para_hist = (
            f"<b>Historic Match</b>: Last year, a student with a highly similar rank of "
            f"<b style='color:#C0392B;'>{h_rank:,}</b> (in the {h_cat} category) secured a seat at "
            f"<b style='color:#C0392B;'>{h_col}</b>. This is a strong indicator of what you might expect."
        )
        para_hist_html = f"<p style='font-size:15px; color:{MU}; line-height:2; margin-bottom:20px;'>{para_hist}</p>"
    else:
        para_hist_html = ""

    para2_html = f"<p style='font-size:15px; color:{MU}; line-height:2; margin-bottom:20px;'>{para2}</p>" if para2 else ""
    para3_html = f"<p style='font-size:15px; color:{MU}; line-height:2; margin:0;'>{para3}</p>"

    st.markdown(
        f"<div style='background:{BRAND['bg_card']}; border:1px solid #1E1E1E;"
        f"border-left:4px solid #C0392B; border-radius:16px;"
        f"padding:30px 36px; margin-bottom:24px;'>"
        f"<div style='font-size:20px; font-weight:800; color:#FFFFFF; margin-bottom:16px;'>"
        f"⚡ Quick Insight</div>"
        f"<p style='font-size:15px; color:{MU}; line-height:2; margin-bottom:20px;'>{para1}</p>"
        f"{para2_html}"
        f"{para_hist_html}"
        f"{para3_html}"
        f"</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Community Poll
# ─────────────────────────────────────────────────────────────────────────────
def render_poll(student: dict):
    """
    Renders the community poll section:
      - STATE 1: Active poll not yet voted → show form
      - STATE 2: Voted OR poll closed → show results
    """
    import json, os, re
    from datetime import datetime

    MU = BRAND["muted"]
    s  = student

    poll_file = os.path.join(os.path.dirname(__file__), "..", "poll_responses.json")
    poll_data = []
    if os.path.exists(poll_file):
        try:
            with open(poll_file, "r") as f:
                poll_data = json.load(f)
        except Exception:
            pass

    has_voted = any(p.get("name") == s["name"] for p in poll_data)

    # Read poll settings
    config_path    = os.path.join(os.path.dirname(__file__), "..", "runtime_config.json")
    is_poll_active = False
    poll_settings  = {}
    try:
        with open(config_path, "r") as f:
            cfg = json.load(f)
            poll_settings = cfg.get("poll_settings", {})
            is_active      = poll_settings.get("is_active", False)
            expires_at_str = poll_settings.get("expires_at", "")
            if is_active and expires_at_str:
                expires_dt = datetime.strptime(expires_at_str, "%Y-%m-%d %H:%M:%S")
                if datetime.now() < expires_dt:
                    is_poll_active = True
    except Exception:
        pass

    p_title = poll_settings.get("title", "📊 Community Poll")
    p_intro = poll_settings.get("intro_content", "Please share your feedback.")
    p_qs    = poll_settings.get("questions", ["Overall Exam", "Biology", "Chemistry", "Physics"])
    p_opts  = poll_settings.get("options", ["Easy", "Medium", "Difficult"])

    has_poll_settings = bool(poll_settings.get("title"))

    if is_poll_active and not has_voted:
        # ── STATE 1: Active — show voting form ──
        st.markdown(
            f"""<style>
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
                position: relative; padding: 2px; border-radius: 28px;
                background: linear-gradient(120deg, #96201A, #C0392B, #E55347, #C0392B, #96201A);
                background-size: 300% 300%;
                animation: pollBorderFlow 5s linear infinite, pollGlow 5s ease-in-out infinite;
                margin-bottom: 32px;
            }}
            .poll-inner {{
                background: linear-gradient(150deg, #121512 60%, #0A0C0A 100%);
                border-radius: 26px; padding: 24px;
                position: relative; overflow: hidden;
            }}
            .poll-orb {{
                position: absolute; top: -80px; right: -80px;
                width: 300px; height: 300px;
                background: radial-gradient(circle, rgba(192,57,43,0.12) 0%, transparent 70%);
                border-radius: 50%; pointer-events: none;
            }}
            [data-testid="stForm"] {{
                background: transparent !important; border: none !important;
                padding: 0 !important; box-shadow: none !important;
            }}
            [data-testid="stFormSubmitButton"] > button {{
                background: linear-gradient(135deg, #96201A, #C0392B, #E55347) !important;
                color: #FFFFFF !important; border: none !important;
                border-radius: 14px !important; font-weight: 800 !important;
                font-size: 15px !important; letter-spacing: 0.5px !important;
                padding: 14px 28px !important; transition: all 0.3s ease !important;
                box-shadow: 0 6px 24px rgba(192,57,43,0.4) !important;
            }}
            [data-testid="stFormSubmitButton"] > button:hover {{
                border: 1px solid rgba(255,255,255,0.05) !important;
            }}
            </style>""",
            unsafe_allow_html=True,
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
        # ── STATE 2: Show results ──
        status_msg = (
            "Thank you for voting! Here is how the community is currently voting."
            if is_poll_active
            else f"The poll has officially closed. Here is how the community voted based on {len(poll_data)} responses."
        )
        total_votes = len(poll_data)
        metrics = {q: {opt: 0 for opt in p_opts} for q in p_qs}
        for p in poll_data:
            for q in p_qs:
                vote = p.get(q, p_opts[0] if p_opts else "N/A")
                if vote in metrics[q]:
                    metrics[q][vote] += 1
                else:
                    metrics[q][vote] = 1

        # Extract poll insight (card published by admin alongside poll)
        poll_insight = None
        try:
            from modules.config import load_manual_insights
            all_insights = load_manual_insights()
            student_exam = s.get("exam", "")
            all_insights = [
                item for item in all_insights
                if item.get("target_exam", "All Students") in ("All Students", student_exam)
            ]
            for item in all_insights:
                if "Poll" in item.get("title", ""):
                    poll_insight = item
                    break
        except Exception:
            pass

        html = (
            f"<div style='background: linear-gradient(145deg, #121512, #0A0C0A); "
            f"border: 1px solid rgba(255,255,255,0.08); border-radius: 24px; padding: 24px; "
            f"margin-bottom: 30px; box-shadow: 0 10px 50px rgba(0,0,0,0.5); "
            f"position: relative; overflow: hidden;'>"
            f"<div style='position: absolute; top: -80px; left: -80px; width: 250px; height: 250px; "
            f"background: radial-gradient(circle, rgba(192,57,43,0.15) 0%, transparent 70%); "
            f"border-radius: 50%; pointer-events: none;'></div>"
            f"<div style='position: absolute; bottom: -80px; right: -80px; width: 300px; height: 300px; "
            f"background: radial-gradient(circle, rgba(76,175,80,0.1) 0%, transparent 70%); "
            f"border-radius: 50%; pointer-events: none;'></div>"
            f"<div style='position: relative; z-index: 10;'>"
            f"<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;'>"
            f"<div style='font-size:14px; font-weight:800; letter-spacing:2px; color:#C0392B; text-transform:uppercase;'>"
            f"📊 {'Live Polling Data' if is_poll_active else 'Final Polling Data'}</div>"
            f"<div style='background: rgba(192,57,43,0.15); border: 1px solid rgba(192,57,43,0.3); "
            f"padding: 6px 14px; border-radius: 20px; color: #FFFFFF; font-size: 13px; font-weight: 700; "
            f"box-shadow: 0 4px 12px rgba(192,57,43,0.2);'>🗳️ {total_votes} Response{'s' if total_votes != 1 else ''}</div>"
            f"</div>"
            f"<div style='font-size:32px; font-weight:800; color:#FFFFFF; margin-bottom:10px; line-height: 1.2;'>📌 Community Poll Results</div>"
            f"<div style='font-size:16px; color:{MU}; margin-bottom:36px;'>{status_msg}</div>"
        )

        for q in p_qs:
            html += (
                f"<div style='margin-bottom:32px;'>"
                f"<div style='display: flex; align-items: center; margin-bottom: 16px;'>"
                f"<div style='background: rgba(255,255,255,0.05); width: 36px; height: 36px; border-radius: 10px; "
                f"display: flex; align-items: center; justify-content: center; margin-right: 12px; font-size: 18px; "
                f"border: 1px solid rgba(255,255,255,0.1);'>📋</div>"
                f"<div style='font-size:18px; font-weight:700; color:#FFFFFF;'>{q}</div>"
                f"</div>"
            )
            for opt in p_opts:
                count = metrics[q].get(opt, 0)
                pct   = (count / total_votes * 100) if total_votes > 0 else 0
                is_majority = count == max(metrics[q].values()) and count > 0
                if is_majority:
                    bar_bg, label_color, pct_color = "linear-gradient(90deg, #96201A, #C0392B, #E55347)", "#FFFFFF", "#FFFFFF"
                    row_bg, row_border, icon, fw = "rgba(192,57,43,0.1)", "1px solid rgba(192,57,43,0.4)", "🏆 ", "700"
                else:
                    bar_bg, label_color, pct_color = "#2A2A2A", "#B0BEC5", "#B0BEC5"
                    row_bg, row_border, icon, fw = "transparent", "1px solid transparent", "", "500"
                html += (
                    f"<div style='background:{row_bg}; border:{row_border}; border-radius:10px; padding:12px 14px; margin-bottom:10px;'>"
                    f"<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>"
                    f"<span style='font-size:14px; font-weight:{fw}; color:{label_color};'>{icon}{opt}</span>"
                    f"<span style='font-size:14px; font-weight:700; color:{pct_color};'>{pct:.1f}%&nbsp;"
                    f"<span style='font-size:12px; color:{MU}; font-weight:400;'>({count})</span></span>"
                    f"</div>"
                    f"<div style='background:#0A0C0A; border-radius:6px; height:8px; overflow:hidden;'>"
                    f"<div style='background:{bar_bg}; width:{pct}%; height:100%; border-radius:6px; transition:width 1.2s ease-in-out;'></div>"
                    f"</div>"
                    f"</div>"
                )
            html += "</div>"  # close question block

        if poll_insight:
            raw = poll_insight.get("content", "")
            raw = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', raw)
            raw = raw.replace('\n', '<br>')
            html += (
                "<style>"
                "@keyframes insightPulse {"
                "0% { box-shadow: 0 0 15px rgba(192,57,43,0.1), inset 0 0 20px rgba(192,57,43,0.05); }"
                "50% { box-shadow: 0 0 30px rgba(192,57,43,0.3), inset 0 0 40px rgba(192,57,43,0.1); }"
                "100% { box-shadow: 0 0 15px rgba(192,57,43,0.1), inset 0 0 20px rgba(192,57,43,0.05); }"
                "}"
                "@keyframes borderFlow {"
                "0% { background-position: 0% 50%; }"
                "50% { background-position: 100% 50%; }"
                "100% { background-position: 0% 50%; }"
                "}"
                "</style>"
                "<div style='margin-top: 48px; position: relative; padding: 2px; border-radius: 24px; "
                "background: linear-gradient(90deg, #96201A, #C0392B, #E55347, #C0392B, #96201A); "
                "background-size: 300% auto; animation: borderFlow 4s linear infinite, insightPulse 4s ease-in-out infinite;'>"
                "<div style='background: rgba(10,12,10,0.97); backdrop-filter: blur(24px); border-radius: 22px; "
                "padding: 36px 40px; position: relative; overflow: hidden;'>"
                "<div style='position: absolute; top: -50px; right: -50px; width: 200px; height: 200px; "
                "background: radial-gradient(circle, rgba(192,57,43,0.15) 0%, transparent 70%); "
                "border-radius: 50%; pointer-events: none;'></div>"
                "<div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px;'>"
                "<div style='display: flex; align-items: center;'>"
                "<div style='background: #C0392B; width: 48px; height: 48px; "
                "border-radius: 16px; display: flex; align-items: center; justify-content: center; "
                "font-size: 24px; box-shadow: 0 8px 24px rgba(192,57,43,0.4); margin-right: 20px;'>✨</div>"
                "<div>"
                "<div style='font-size: 12px; font-weight: 800; letter-spacing: 2.5px; text-transform: uppercase; "
                "color: #C0392B; margin-bottom: 6px; display: flex; align-items: center;'>"
                "<span style='display: inline-block; width: 6px; height: 6px; background: #C0392B; border-radius: 50%; "
                "margin-right: 8px; box-shadow: 0 0 10px #C0392B;'></span>Verified GMA Insight</div>"
                f"<div style='font-size: 24px; font-weight: 800; color: #FFFFFF; line-height: 1.2;'>"
                f"{poll_insight.get('title', 'Community Insight')}</div>"
                "</div></div></div>"
                "<div style='font-size: 16px; color: #FFFFFF; line-height: 1.9; font-weight: 500; "
                "background: rgba(255,255,255,0.02); padding: 28px 32px; border-radius: 16px; "
                "border: 1px solid rgba(255,255,255,0.05); position: relative;'>"
                "<div style='position: absolute; top: 0; left: 0; width: 4px; height: 100%; "
                "background: linear-gradient(180deg, #96201A, #C0392B, #E55347); border-radius: 4px 0 0 4px;'></div>"
                f"{raw}</div>"
                "</div></div>"
            )

        html += "</div></div>"  # close card

        minified = re.sub(r'\n\s*', ' ', html)
        st.markdown(minified, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Manual Insights Cards
# ─────────────────────────────────────────────────────────────────────────────
def render_manual_insights(insights: list):
    """Renders the list of admin-published custom insight cards."""
    import re

    # Inject keyframes once
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
        return

    TYPE_MAP = {
        "poll":        {"grad":"#96201A,#C0392B,#E55347", "badge":"🗳️ POLL RESULT",   "badge_bg":"rgba(192,57,43,0.18)",  "badge_color":"#E57373", "orb1":"rgba(192,57,43,0.18)",  "orb2":"rgba(150,32,26,0.10)",  "accent":"#C0392B"},
        "result":      {"grad":"#96201A,#C0392B,#E55347", "badge":"📜 RESULT UPDATE",  "badge_bg":"rgba(192,57,43,0.15)",  "badge_color":"#C0392B", "orb1":"rgba(192,57,43,0.15)",  "orb2":"rgba(150,32,26,0.10)",  "accent":"#C0392B"},
        "counselling": {"grad":"#96201A,#C0392B,#E55347", "badge":"📝 COUNSELLING",    "badge_bg":"rgba(192,57,43,0.15)",  "badge_color":"#E57373", "orb1":"rgba(192,57,43,0.18)",  "orb2":"rgba(150,32,26,0.10)",  "accent":"#C0392B"},
        "rank":        {"grad":"#96201A,#C0392B,#E55347", "badge":"🏆 RANK INSIGHT",   "badge_bg":"rgba(192,57,43,0.15)",  "badge_color":"#E57373", "orb1":"rgba(192,57,43,0.18)",  "orb2":"rgba(150,32,26,0.10)",  "accent":"#E57373"},
        "default":     {"grad":"#96201A,#C0392B,#E55347", "badge":"✦ GMA INSIGHT",    "badge_bg":"rgba(192,57,43,0.15)",  "badge_color":"#C0392B", "orb1":"rgba(192,57,43,0.18)",  "orb2":"rgba(150,32,26,0.10)",  "accent":"#C0392B"},
    }

    def _card_type(title_str):
        t = title_str.lower()
        if "poll"    in t: return "poll"
        if "result"  in t: return "result"
        if "counsel" in t: return "counselling"
        if "rank"    in t: return "rank"
        return "default"

    EXAM_PILL_COLORS = {
        "NEET UG": ("#4CAF50", "rgba(76,175,80,0.18)"),
        "KEAM":    ("#E57373", "rgba(229,115,115,0.18)"),
        "NEET PG": ("#C0392B", "rgba(192,57,43,0.18)"),
    }

    for card_idx, item in enumerate(insights):
        raw_content = item.get("content", "")
        raw_content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', raw_content)
        raw_content = raw_content.replace('\n', '<br>')

        title       = item.get("title", "GMA Insight Update")
        target_exam = item.get("target_exam", "All Students")
        ctype       = _card_type(title)
        P           = TYPE_MAP[ctype]
        grad        = P["grad"]
        anim_delay  = f"{card_idx * 0.12:.2f}s"

        if target_exam != "All Students" and target_exam in EXAM_PILL_COLORS:
            pill_c, pill_bg = EXAM_PILL_COLORS[target_exam]
            top_right_badge = (
                f"<div style='display:inline-flex;align-items:center;gap:7px;"
                f"background:{pill_bg};border:1px solid {pill_c}55;border-radius:30px;padding:5px 14px;'>"
                f"<span style='font-size:13px;'>🎯</span>"
                f"<span style='font-size:11px;font-weight:800;letter-spacing:1.5px;"
                f"color:{pill_c};text-transform:uppercase;'>For You &nbsp;·&nbsp; {target_exam}</span>"
                f"</div>"
            )
        else:
            top_right_badge = (
                f"<div style='display:inline-flex;align-items:center;gap:7px;"
                f"background:rgba(76,175,80,0.15);border:1px solid rgba(76,175,80,0.45);"
                f"border-radius:30px;padding:5px 16px;box-shadow:0 0 12px rgba(76,175,80,0.35);'>"
                f"<span style='width:7px;height:7px;border-radius:50%;background:#4CAF50;"
                f"box-shadow:0 0 8px #4CAF50, 0 0 16px #4CAF50;display:inline-block;"
                f"animation:badgePulse 2s ease-in-out infinite;'></span>"
                f"<span style='font-size:11px;font-weight:800;letter-spacing:2.5px;"
                f"color:#4CAF50;text-transform:uppercase;"
                f"text-shadow:0 0 10px rgba(76,175,80,0.8);'>&#10022; NEW</span>"
                f"</div>"
            )

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
  <div style="
    position:relative; overflow:hidden;
    background:linear-gradient(150deg,#161B22 60%,#0D1117 100%);
    border-radius:24px; padding:36px 40px;
  ">
    <div style="position:absolute;top:-70px;left:-70px;width:260px;height:260px;
        background:radial-gradient(circle,{P['orb1']} 0%,transparent 70%);
        border-radius:50%;pointer-events:none;"></div>
    <div style="position:absolute;bottom:-80px;right:-60px;width:300px;height:300px;
        background:radial-gradient(circle,{P['orb2']} 0%,transparent 70%);
        border-radius:50%;pointer-events:none;"></div>
    <div class="gma-shimmer" style="
        position:absolute;top:0;left:0;width:60px;height:100%;
        background:linear-gradient(90deg,transparent,rgba(255,255,255,0.06),transparent);
        pointer-events:none; animation:none;
    "></div>
    <div style="position:relative;z-index:5;">
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
      <div style="font-size:26px;font-weight:900;color:#FFFFFF;
          line-height:1.25;margin-bottom:14px;letter-spacing:-0.3px;">
        {title}
      </div>
      <div style="font-size:15.5px;color:#D1D9E0;line-height:1.95;
          font-weight:500;letter-spacing:0.15px;">
        {raw_content}
      </div>
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
    </div>
  </div>
</div>
"""
        minified = re.sub(r'\n\s*', ' ', card_html)
        st.markdown(minified, unsafe_allow_html=True)

