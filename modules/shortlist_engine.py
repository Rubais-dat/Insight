"""
GMA Insight – Dynamic College Shortlist Builder Engine
-------------------------------------------------------
Powers the interactive, real-time College Shortlist Builder feature.
All data is computed LIVE from 2025 Kerala allotment Excel on every filter change.
"""

import re
import pandas as pd
import streamlit as st
from modules.kerala_data import load_kerala_data, load_comparison_data, get_last_ranks, _extract_code


# ─────────────────────────────────────────────
# Round-by-round cutoff tracker
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def get_round_cutoffs() -> pd.DataFrame:
    """
    Returns per-college × course × category cutoffs for each counselling round.
    Columns: College Name, Course, Alloted Category, code, Round 1, Round 2, Round 3, Mop-up
    (only rounds that exist in the data)
    """
    df = load_kerala_data()
    if "Round" not in df.columns and "Allotment Round" not in df.columns:
        # No round column — return last-rank only
        return pd.DataFrame()

    round_col = "Round" if "Round" in df.columns else "Allotment Round"
    pivot = (
        df.pivot_table(
            index=["College Name", "Course", "Alloted Category"],
            columns=round_col,
            values="Rank",
            aggfunc="max",
        )
        .reset_index()
    )
    pivot.columns = [str(c).strip() for c in pivot.columns]
    pivot["code"] = pivot["College Name"].apply(_extract_code)
    return pivot


@st.cache_data(show_spinner=False)
def get_enriched_cutoffs() -> pd.DataFrame:
    """
    Full enriched table: last_rank + fee + type + GMA rating per (college, course, category).
    This is the master dataset for the shortlist builder.
    """
    cutoffs = get_last_ranks()       # college, course, category, last_rank, code
    comp    = load_comparison_data() # code → fee, type, rating

    merged = cutoffs.merge(comp, on="code", how="left", suffixes=("", "_comp"))

    # Normalise type
    merged["College Type"] = merged["College Type"].fillna("Unknown")
    merged["Total Fee"]    = pd.to_numeric(merged["Total Fee"], errors="coerce")
    merged["GMA Rating"]   = merged["GMA Rating"].astype(str)

    # Clean college name (remove prefix code)
    merged["clean_name"] = merged["College Name"].apply(
        lambda n: re.sub(r"^[A-Z]{2,4}[-:\s]+", "", str(n)).strip()
    )
    return merged


def compute_seat_probability(student_rank: int, cutoff_rank: int) -> tuple[float, str]:
    """
    Returns (probability_pct, label) based on how far student_rank is from cutoff.
    probability represents chance of securing this seat.
    """
    if cutoff_rank <= 0:
        return 0.0, "Unknown"
    ratio = student_rank / cutoff_rank  # < 1 = better than cutoff
    if ratio <= 0.70:
        return 98.0, "Very High"
    elif ratio <= 0.85:
        return 88.0, "High"
    elif ratio <= 0.95:
        return 72.0, "Good"
    elif ratio <= 1.00:
        return 55.0, "Moderate"
    elif ratio <= 1.10:
        return 30.0, "Low"
    elif ratio <= 1.25:
        return 12.0, "Very Low"
    else:
        return 4.0, "Unlikely"


def render_shortlist_builder(student_rank: int, category_code: str):
    """
    Main entry point: renders the full interactive Shortlist Builder UI.
    All filtering is live — Streamlit rerenders on every widget change.
    """
    from modules.config import BRAND

    # ── Load data ────────────────────────────────────────────────────────────
    df_all = get_enriched_cutoffs()
    if df_all.empty:
        st.info("Shortlist data not available.")
        return

    # Session state for shortlisted colleges
    if "shortlist" not in st.session_state:
        st.session_state.shortlist = []

    # ── Header ───────────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    @keyframes sliderGlow {
        0%,100% { box-shadow: 0 0 0 rgba(192,57,43,0); }
        50%      { box-shadow: 0 0 14px rgba(192,57,43,0.4); }
    }
    .shortlist-header {
        background: linear-gradient(135deg, #121512, #0D1117);
        border: 1px solid rgba(192,57,43,0.35);
        border-radius: 20px;
        padding: 26px 30px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    .prob-bar-fill {
        height: 100%;
        border-radius: 6px;
        transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .college-row {
        background: linear-gradient(145deg, #161B22, #0D1117);
        border: 1px solid #1E1E1E;
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 10px;
        transition: border-color 0.2s, box-shadow 0.2s;
        animation: fadeUp 0.35s ease both;
    }
    .college-row:hover {
        border-color: rgba(192,57,43,0.4);
        box-shadow: 0 4px 20px rgba(192,57,43,0.12);
    }
    .shortlist-badge {
        background: rgba(76,175,80,0.15);
        border: 1px solid rgba(76,175,80,0.4);
        color: #4CAF50;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 11px;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="shortlist-header">
        <div style="position:absolute;top:-40px;right:-40px;width:160px;height:160px;
            background:radial-gradient(circle,rgba(192,57,43,0.12) 0%,transparent 70%);
            border-radius:50%;pointer-events:none;"></div>
        <div style="display:flex;align-items:center;gap:14px;margin-bottom:8px;">
            <div style="width:50px;height:50px;border-radius:16px;flex-shrink:0;
                background:linear-gradient(135deg,#C0392B,#1B5E20);
                display:flex;align-items:center;justify-content:center;font-size:24px;
                box-shadow:0 8px 24px rgba(192,57,43,0.4);animation:sliderGlow 3s ease-in-out infinite;">🎯</div>
            <div>
                <div style="font-size:11px;font-weight:800;letter-spacing:2.5px;
                    color:#C0392B;text-transform:uppercase;margin-bottom:3px;">Brand New · Live Feature</div>
                <div style="font-size:22px;font-weight:900;color:#FFFFFF;line-height:1.2;">
                    Dynamic College Shortlist Builder
                </div>
            </div>
        </div>
        <div style="font-size:14px;color:{BRAND['muted']};line-height:1.65;">
            Filter and explore <b style="color:#FFFFFF;">all 2025 Kerala CEE allotment data</b> in real time.
            Every filter change instantly recalculates your personalised college list with
            live seat probability bars — powered by actual rank data.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Filter panel ─────────────────────────────────────────────────────────
    st.markdown(
        f"<div style='font-size:11px;font-weight:800;letter-spacing:2px;"
        f"color:{BRAND['muted']};text-transform:uppercase;margin-bottom:10px;'>🔧 Live Filters</div>",
        unsafe_allow_html=True,
    )
    fc1, fc2, fc3, fc4 = st.columns([2, 2, 2, 2])
    with fc1:
        filter_type = st.selectbox(
            "College Type",
            ["All", "Government", "Private", "Aided"],
            key="sb_type",
        )
    with fc2:
        all_courses = sorted(df_all["Course"].dropna().unique().tolist())
        filter_course = st.selectbox(
            "Course",
            ["All Courses"] + all_courses,
            key="sb_course",
        )
    with fc3:
        filter_chance = st.selectbox(
            "Min. Chance Level",
            ["Any Chance", "Moderate+", "Good+", "High+", "Very High"],
            key="sb_chance",
        )
    with fc4:
        # Max fee slider — in lakhs
        max_fee_lakh = st.slider(
            "Max Total Fee (₹ Lakhs)",
            min_value=0,
            max_value=100,
            value=100,
            step=5,
            key="sb_fee",
        )

    # Categories filter
    eligible_cats = list({category_code, "SM"})
    cat_options   = ["My Categories (" + " + ".join(eligible_cats) + ")", "All Categories"]
    filter_cat    = st.radio("Category Scope", cat_options, horizontal=True, key="sb_cat")

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # ── Apply filters ─────────────────────────────────────────────────────────
    df = df_all.copy()

    # Category filter
    if "My Categories" in filter_cat:
        df = df[df["Alloted Category"].isin(eligible_cats)]

    # Type filter
    if filter_type != "All":
        df = df[df["College Type"].str.contains(filter_type, case=False, na=False)]

    # Course filter
    if filter_course != "All Courses":
        df = df[df["Course"] == filter_course]

    # Fee filter
    max_fee = max_fee_lakh * 100_000
    if max_fee_lakh < 100:
        df = df[(df["Total Fee"].isna()) | (df["Total Fee"] <= max_fee)]

    # Compute probability for each row
    df = df.copy()
    df["prob_pct"]    = df["last_rank"].apply(lambda cr: compute_seat_probability(student_rank, cr)[0])
    df["prob_label"]  = df["last_rank"].apply(lambda cr: compute_seat_probability(student_rank, cr)[1])

    # Chance filter
    CHANCE_ORDER = {"Unlikely": 0, "Very Low": 1, "Low": 2, "Moderate": 3, "Good": 4, "High": 5, "Very High": 6}
    if filter_chance == "Moderate+":
        df = df[df["prob_label"].map(CHANCE_ORDER).fillna(0) >= 3]
    elif filter_chance == "Good+":
        df = df[df["prob_label"].map(CHANCE_ORDER).fillna(0) >= 4]
    elif filter_chance == "High+":
        df = df[df["prob_label"].map(CHANCE_ORDER).fillna(0) >= 5]
    elif filter_chance == "Very High":
        df = df[df["prob_label"].map(CHANCE_ORDER).fillna(0) >= 6]

    # Sort: best chance first, then by last_rank ascending
    df = df.sort_values(["prob_pct", "last_rank"], ascending=[False, True]).reset_index(drop=True)

    # ── Result summary bar ────────────────────────────────────────────────────
    total_results = len(df)
    shortlist_cnt = len(st.session_state.shortlist)

    CHANCE_COLORS_MAP = {
        "Very High": "#4CAF50",
        "High":      "#66BB6A",
        "Good":      "#FFC107",
        "Moderate":  "#E57373",
        "Low":       "#C0392B",
        "Very Low":  "#8B1A1A",
        "Unlikely":  "#4A4A4A",
    }

    st.markdown(
        f"<div style='display:flex;align-items:center;justify-content:space-between;"
        f"background:rgba(255,255,255,0.03);border:1px solid #1E1E1E;border-radius:12px;"
        f"padding:10px 16px;margin-bottom:16px;flex-wrap:wrap;gap:10px;'>"
        f"<span style='font-size:13px;font-weight:700;color:#FFFFFF;'>"
        f"📋 <span style='color:#4CAF50;'>{total_results}</span> colleges matched your filters</span>"
        f"<span style='font-size:12px;color:{BRAND['muted']};'>"
        f"🗂️ Shortlisted: <b style='color:#FFD700;'>{shortlist_cnt}</b> college(s)</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    if total_results == 0:
        st.markdown("""
        <div style='text-align:center;padding:48px 24px;background:#121512;
            border:1px dashed #2A2A2A;border-radius:16px;color:#B0BEC5;'>
            <div style='font-size:36px;margin-bottom:12px;'>🔍</div>
            <div style='font-size:15px;font-weight:700;color:#FFFFFF;'>No colleges match your filters</div>
            <div style='font-size:13px;margin-top:6px;'>Try relaxing the fee limit or chance filter.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Render college rows ───────────────────────────────────────────────────
    display_df = df.head(30)  # cap at 30 for performance

    for idx, row in display_df.iterrows():
        college_key = f"{row['College Name']}|{row['Course']}|{row['Alloted Category']}"
        is_shortlisted = college_key in st.session_state.shortlist

        prob    = row["prob_pct"]
        label   = row["prob_label"]
        bar_color = CHANCE_COLORS_MAP.get(label, "#4A4A4A")
        fee_str = f"₹{int(row['Total Fee']):,.0f}" if pd.notna(row["Total Fee"]) else "—"
        rating  = str(row["GMA Rating"]) if str(row["GMA Rating"]) not in ("nan", "None", "—", "") else "—"
        col_type = str(row["College Type"])
        type_icon = "🏛️" if "Gov" in col_type else ("🏥" if "Aided" in col_type else "🏫")

        clean = row["clean_name"]
        cat   = row["Alloted Category"]
        cr    = int(row["last_rank"])
        course = row["Course"]

        # Probability bar HTML
        prob_bar = (
            f"<div style='background:#0A0C0A;border-radius:6px;height:8px;"
            f"overflow:hidden;margin-top:10px;margin-bottom:4px;'>"
            f"<div class='prob-bar-fill' style='width:{prob:.0f}%;background:"
            f"linear-gradient(90deg,{bar_color}88,{bar_color});'></div></div>"
        )

        # Row: college info + shortlist button
        row_col, btn_col = st.columns([10, 2])
        with row_col:
            shortlist_badge = (
                "<span class='shortlist-badge'>✓ Shortlisted</span>"
                if is_shortlisted else ""
            )
            st.markdown(
                f"<div class='college-row'>"
                f"<div style='display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;'>"
                f"<div style='flex:1;'>"
                f"<div style='font-size:15px;font-weight:800;color:#FFFFFF;margin-bottom:4px;'>"
                f"{type_icon} {clean} {shortlist_badge}</div>"
                f"<div style='font-size:12px;color:{BRAND['muted']};display:flex;flex-wrap:wrap;gap:8px;'>"
                f"<span>📚 {course}</span>"
                f"<span style='color:#30363D;'>·</span>"
                f"<span>🏷️ {cat}</span>"
                f"<span style='color:#30363D;'>·</span>"
                f"<span>🏢 {col_type}</span>"
                f"</div>"
                f"</div>"
                f"<div style='display:flex;gap:10px;align-items:center;flex-wrap:wrap;'>"
                f"<div style='text-align:right;'>"
                f"<div style='font-size:11px;color:{BRAND['muted']};'>2025 Last Rank</div>"
                f"<div style='font-size:16px;font-weight:900;color:#FFFFFF;'>{cr:,}</div>"
                f"</div>"
                f"<div style='text-align:right;'>"
                f"<div style='font-size:11px;color:{BRAND['muted']};'>Total Fee</div>"
                f"<div style='font-size:14px;font-weight:700;color:#FFD700;'>{fee_str}</div>"
                f"</div>"
                f"<div style='text-align:center;min-width:90px;'>"
                f"<div style='background:{bar_color}22;border:1px solid {bar_color}55;"
                f"border-radius:20px;padding:4px 12px;font-size:12px;font-weight:800;color:{bar_color};'>"
                f"{label}</div>"
                f"<div style='font-size:10px;color:{BRAND['muted']};margin-top:3px;'>{prob:.0f}% chance</div>"
                f"</div>"
                f"</div>"
                f"</div>"
                f"{prob_bar}"
                f"<div style='font-size:10px;color:{BRAND['muted']};text-align:right;'>"
                f"{'⭐ GMA Rating: ' + rating if rating != '—' else ''}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

        with btn_col:
            st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
            if is_shortlisted:
                if st.button("✓ Remove", key=f"sl_remove_{idx}", use_container_width=True):
                    st.session_state.shortlist.remove(college_key)
                    st.rerun()
            else:
                if st.button("＋ Shortlist", key=f"sl_add_{idx}", use_container_width=True):
                    st.session_state.shortlist.append(college_key)
                    st.rerun()

    if total_results > 30:
        st.markdown(
            f"<div style='text-align:center;font-size:12px;color:{BRAND['muted']};padding:12px;'>"
            f"Showing top 30 of {total_results} matched colleges. Refine filters to narrow down.</div>",
            unsafe_allow_html=True,
        )

    # ── Shortlist Panel ───────────────────────────────────────────────────────
    if st.session_state.shortlist:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='font-size:14px;font-weight:700;color:#FFD700;margin-bottom:12px;'>"
            f"⭐ Your Shortlist ({len(st.session_state.shortlist)} colleges)</div>",
            unsafe_allow_html=True,
        )
        for i, key in enumerate(st.session_state.shortlist):
            parts = key.split("|")
            name  = re.sub(r"^[A-Z]{2,4}[-:\s]+", "", parts[0]).strip() if parts else key
            course_sl = parts[1] if len(parts) > 1 else "—"
            cat_sl    = parts[2] if len(parts) > 2 else "—"
            st.markdown(
                f"<div style='background:rgba(255,215,0,0.06);border:1px solid rgba(255,215,0,0.2);"
                f"border-radius:10px;padding:10px 14px;margin-bottom:6px;"
                f"display:flex;justify-content:space-between;align-items:center;'>"
                f"<span style='font-size:13px;font-weight:700;color:#FFFFFF;'>"
                f"{i+1}. {name}</span>"
                f"<span style='font-size:11px;color:#B0BEC5;'>{course_sl} · {cat_sl}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )
        if st.button("🗑️ Clear Entire Shortlist", use_container_width=False):
            st.session_state.shortlist = []
            st.rerun()
