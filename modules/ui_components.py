"""
GMA Insight – UI Components
-----------------------------
Reusable glassmorphism-styled cards, badges, timeline, and metric tiles.
"""

import streamlit as st
from modules.config import BRAND, CHANCE_COLORS, CHANCE_ICONS, STAGE_LABELS, STAGE_ORDER


# ─────────────────────────────────────────────
# Global CSS injection (call once from app)
# ─────────────────────────────────────────────
def inject_global_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        background-color: {BRAND["bg_dark"]};
        color: {BRAND["text"]};
    }}

    /* Hide Streamlit chrome but keep header for sidebar toggle */
    #MainMenu, footer {{ visibility: hidden; }}
    .block-container {{ padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1100px; }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: {BRAND["bg_dark"]} !important;
        border-right: 1px solid #1E1E1E;
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 6px; }}
    ::-webkit-scrollbar-track {{ background: {BRAND["bg_dark"]}; }}
    ::-webkit-scrollbar-thumb {{ background: #C0392B88; border-radius: 3px; }}

    /* Button — volcano red → forest green gradient */
    .stButton > button {{
        background: linear-gradient(135deg, #C0392B, #1B5E20);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        transition: opacity .2s;
    }}
    .stButton > button:hover {{ opacity: 0.85; }}

    /* Selectbox / inputs */
    .stSelectbox > div > div, .stTextInput > div > div > input, .stNumberInput > div > div > input {{
        background: {BRAND["bg_card"]} !important;
        color: {BRAND["text"]} !important;
        border: 1px solid #2A2A2A !important;
        border-radius: 8px !important;
    }}

    /* Expander */
    .streamlit-expanderHeader {{
        background: {BRAND["bg_card"]} !important;
        border-radius: 8px !important;
        color: {BRAND["text"]} !important;
    }}

    /* Card fade-in animation */
    @keyframes fadeUp {{
        from {{ opacity: 0; transform: translateY(12px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}
    .gma-card {{ animation: fadeUp .35s ease both; }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background: {BRAND["bg_card"]} !important;
        border-radius: 12px;
        padding: 4px;
        gap: 2px;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px !important;
        color: {BRAND["muted"]} !important;
        font-weight: 500;
        transition: all .2s;
    }}
    .stTabs [aria-selected="true"] {{
        background: rgba(76,175,80,0.15) !important;
        color: #4CAF50 !important;
    }}

    /* Metric */
    [data-testid="stMetric"] {{
        background: {BRAND["bg_card"]};
        border: 1px solid #1E1E1E;
        border-left: 3px solid #C0392B;
        border-radius: 12px;
        padding: 12px 16px;
    }}
    [data-testid="stMetricLabel"] {{ color: {BRAND["muted"]} !important; font-size:12px; }}
    [data-testid="stMetricValue"] {{ color: #4CAF50 !important; font-size:24px; font-weight:700; }}
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# App Header
# ─────────────────────────────────────────────
def render_header():
    st.markdown(f"""
    <div style='
        background: {BRAND["bg_card"]};
        border: 1px solid #1E1E1E;
        border-left: 4px solid #C0392B;
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 16px;
    '>
        <div style='font-size:40px; line-height:1;'>🔮</div>
        <div>
            <div style='font-size:26px; font-weight:800; color:#C0392B;'>
                GMA Insight
            </div>
            <div style='color:{BRAND["muted"]}; font-size:13px; margin-top:2px; letter-spacing:.5px;'>
                Actionable Admission Intelligence — Personalised for You
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Stage Timeline
# ─────────────────────────────────────────────
def render_stage_timeline(current_stage):
    """Horizontal scrollable timeline showing admission journey progress."""
    total = len(STAGE_ORDER)
    current_idx = STAGE_ORDER.index(current_stage)

    dots_html = ""
    for i, stage in enumerate(STAGE_ORDER):
        label = STAGE_LABELS[stage]

        # Determine color and dot symbol
        if i < current_idx:
            color = BRAND["accent"]
            dot = "✓"
        elif i == current_idx:
            color = BRAND["primary"]
            dot = "●"
        else:
            color = BRAND["muted"]
            dot = "○"

        label_color = color if i == current_idx else BRAND["muted"]

        # Build dot HTML
        dot_html = (
            '<div style="display:flex; flex-direction:column; align-items:center; min-width:80px;">'
            f'<div style="width:28px; height:28px; border-radius:50%; background:{color}22; border:2px solid {color}; display:flex; align-items:center; justify-content:center; font-size:12px; color:{color}; font-weight:700;">{dot}</div>'
            f'<div style="font-size:9px; color:{label_color}; text-align:center; margin-top:5px; max-width:70px; line-height:1.3;">{label}</div>'
            '</div>'
        )

        # Build connector
        if i < total - 1:
            if i == current_idx - 1:
                conn_bg = f"linear-gradient(90deg,{BRAND['accent']},{BRAND['primary']})"
            elif i < current_idx:
                conn_bg = BRAND["accent"]
            else:
                conn_bg = "#30363D"
            connector = f'<div style="flex:1; height:2px; background:{conn_bg}; margin-top:-14px; min-width:10px;"></div>'
        else:
            connector = ""

        dots_html += dot_html + connector

    container_html = (
        f'<div style="background:{BRAND["bg_card"]}; border:1px solid #30363D; border-radius:14px; padding:16px 20px; margin-bottom:24px; overflow-x:auto;">'
        f'<div style="font-size:11px; color:{BRAND["muted"]}; text-transform:uppercase; letter-spacing:2px; margin-bottom:14px;">Admission Journey</div>'
        f'<div style="display:flex; align-items:center; gap:0; min-width:600px;">'
        f'{dots_html}'
        f'</div></div>'
    )
    st.markdown(container_html, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Insight Card
# ─────────────────────────────────────────────
def insight_card(icon: str, title: str, body: str, tag: str = "", tag_color: str = ""):
    tag_html = ""
    if tag:
        color = tag_color or "#C0392B"
        tag_html = f'<span style="background:{color}22; color:{color}; font-size:10px; font-weight:600; padding:2px 10px; border-radius:20px; letter-spacing:.5px;">{tag}</span>'

    st.markdown(f"""
    <div class='gma-card' style='
        background: {BRAND["bg_card"]};
        border: 1px solid #1E1E1E;
        border-left: 3px solid #C0392B;
        border-radius: 12px;
        padding: 16px 18px;
        margin-bottom: 12px;
    '>
        <div style='display:flex; align-items:flex-start; gap:12px;'>
            <div style='font-size:24px; line-height:1; padding-top:2px;'>{icon}</div>
            <div style='flex:1;'>
                <div style='display:flex; align-items:center; gap:8px; margin-bottom:6px;'>
                    <div style='font-size:14px; font-weight:700; color:#FFFFFF;'>{title}</div>
                    {tag_html}
                </div>
                <div style='font-size:13px; color:{BRAND["muted"]}; line-height:1.7;'>{body}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# College Chance Card
# ─────────────────────────────────────────────
def college_chance_card(college: str, course: str, category: str,
                         round_: str, closing_rank: int, chance: str):
    color = CHANCE_COLORS.get(chance, BRAND["primary"])
    icon  = CHANCE_ICONS.get(chance, "🔵")

    st.markdown(f"""
    <div class='gma-card' style='
        background: {BRAND["bg_card"]};
        border: 1px solid {color}33;
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 10px;
    '>
        <div style='display:flex; justify-content:space-between; align-items:flex-start;'>
            <div style='flex:1;'>
                <div style='font-size:14px; font-weight:700; color:{BRAND["text"]}; margin-bottom:4px;'>{college}</div>
                <div style='font-size:12px; color:{BRAND["muted"]};'>
                    {course} &nbsp;|&nbsp; {category} &nbsp;|&nbsp; {round_}
                </div>
            </div>
            <div style='text-align:right; min-width:110px;'>
                <div style='
                    background:{color}22;
                    color:{color};
                    border:1px solid {color}55;
                    border-radius:20px;
                    padding:4px 12px;
                    font-size:12px;
                    font-weight:700;
                    margin-bottom:6px;
                '>{icon} {chance} Chance</div>
                <div style='font-size:11px; color:{BRAND["muted"]}; text-align:right;'>
                    2025 Closing Rank: <span style='color:{BRAND["text"]}; font-weight:600;'>{closing_rank:,}</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Section Header
# ─────────────────────────────────────────────
def section_header(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div style='margin: 24px 0 14px 0;'>
        <div style='font-size:18px; font-weight:700; color:{BRAND["text"]};'>{title}</div>
        {'<div style="font-size:12px; color:' + BRAND["muted"] + '; margin-top:3px;">' + subtitle + '</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# No-data placeholder
# ─────────────────────────────────────────────
def empty_state(message: str = "No data available", icon: str = "🔍"):
    st.markdown(f"""
    <div style='
        text-align:center;
        padding:48px 24px;
        background:{BRAND["bg_card"]};
        border:1px dashed #30363D;
        border-radius:16px;
        color:{BRAND["muted"]};
    '>
        <div style='font-size:36px; margin-bottom:12px;'>{icon}</div>
        <div style='font-size:14px;'>{message}</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Disclaimer banner
# ─────────────────────────────────────────────
def disclaimer_banner(text: str):
    st.markdown(f"""
    <div style='
        background:{BRAND["warn"]}11;
        border:1px solid {BRAND["warn"]}33;
        border-radius:10px;
        padding:10px 14px;
        font-size:12px;
        color:{BRAND["warn"]};
        margin-top:16px;
    '>⚠️&nbsp; {text}</div>
    """, unsafe_allow_html=True)
