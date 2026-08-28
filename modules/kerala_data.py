"""
GMA Insight – Kerala 2025 Rank Data Loader
--------------------------------------------
Reads 2025_Rank.xlsx + KERALA COMPARISON DATA.xlsx and provides:
  - load_kerala_data()      → allotment rows
  - load_comparison_data()  → college fees / ratings
  - get_better_choices()    → top reachable colleges with fees
  - get_quick_insight()     → summary dict for quick info card
"""

import os
import re
import pandas as pd
import streamlit as st

RANK_PATH   = os.path.join(os.path.dirname(__file__), "..", "2025_Rank.xlsx")
COMP_PATH   = os.path.join(os.path.dirname(__file__), "..", "KERALA COMPARISON DATA.xlsx")


# ── Data loaders ──────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def load_kerala_data() -> pd.DataFrame:
    df = pd.read_excel(RANK_PATH)
    df.columns = [c.strip() for c in df.columns]
    df["Rank"] = pd.to_numeric(df["Rank"], errors="coerce")
    df = df.dropna(subset=["Rank", "Alloted Category"])
    df["Rank"] = df["Rank"].astype(int)
    df["Alloted Category"] = df["Alloted Category"].str.strip()
    return df

@st.cache_data(show_spinner=False)
def get_all_categories() -> list[str]:
    """Returns a sorted list of all unique category codes present in the Kerala dataset."""
    df = load_kerala_data()
    cats = df["Alloted Category"].dropna().unique().tolist()
    # Sort them, keeping SM (State Merit / General) at the top if present
    cats.sort()
    if "SM" in cats:
        cats.remove("SM")
        cats.insert(0, "SM")
    return cats


@st.cache_data(show_spinner=False)
def load_comparison_data() -> pd.DataFrame:
    if not os.path.exists(COMP_PATH):
        return pd.DataFrame(columns=["College Name", "Tution Fee", "Total Fee", "Hostel Fee", "College Type", "GMA Rank", "GMA Rating", "code"])
        
    df = pd.read_excel(COMP_PATH)
    df.columns = [c.strip() for c in df.columns]

    # Normalise fee columns to int (strip commas etc.)
    for col in ["Tution Fee", "Total Fee", "Hostel Fee"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(",", "").str.strip()
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Extract 3-letter college code from "KKM : Govt. Medical…" → "KKM"
    df["code"] = df["College Name"].str.extract(r"^([A-Z]{2,4})\s*:", expand=False).str.strip()
    return df


def _extract_code(name: str) -> str:
    """Pull 3-letter prefix from rank-data college name e.g. 'KKM- Govt…' → 'KKM'"""
    m = re.match(r"^([A-Z]{2,4})[-\s]", name.strip())
    return m.group(1) if m else ""


# ── Core logic ────────────────────────────────────────────────────────────────

def get_last_ranks() -> pd.DataFrame:
    """Last allotted rank per college × course × category across all rounds."""
    df = load_kerala_data()
    cutoffs = (
        df.groupby(["College Name", "Course", "Alloted Category"])["Rank"]
        .max()
        .reset_index()
        .rename(columns={"Rank": "last_rank"})
    )
    cutoffs["code"] = cutoffs["College Name"].apply(_extract_code)
    return cutoffs


def get_better_choices(rank: int, category_code: str,
                       n: int = 6) -> list[dict]:
    """
    Return up to `n` colleges where the student's rank is BELOW the
    2025 last-allotted rank — i.e. they have a real shot.
    Enriched with fee + rating from comparison data.
    """
    cutoffs = get_last_ranks()
    comp    = load_comparison_data()

    # Show SM (general) + student's own category
    cats_to_show = list({"SM", category_code})
    relevant = cutoffs[cutoffs["Alloted Category"].isin(cats_to_show)].copy()

    # Student rank must be <= last allotted rank (they can get in)
    reachable = relevant[relevant["last_rank"] >= rank].copy()

    if reachable.empty:
        # Fallback: nearest colleges above rank (closest misses)
        reachable = relevant.sort_values("last_rank", ascending=False).head(30)
    else:
        # Sort by closest cutoff (tightest competition first = best match)
        reachable = reachable.sort_values("last_rank").head(30)

    # Join fee/rating data on college code
    results = []
    seen    = set()
    for _, row in reachable.iterrows():
        col_name = row["College Name"]
        if col_name in seen:
            continue
        seen.add(col_name)

        # Match comparison row by code
        code     = row["code"]
        fee_row  = comp[comp["code"] == code].head(1)

        total_fee   = int(fee_row["Total Fee"].values[0])   if not fee_row.empty and not pd.isna(fee_row["Total Fee"].values[0])   else None
        tuition_fee = int(fee_row["Tution Fee"].values[0])  if not fee_row.empty and not pd.isna(fee_row["Tution Fee"].values[0])  else None
        college_type= fee_row["College Type"].values[0]     if not fee_row.empty else "—"
        gma_rank    = fee_row["GMA Rank"].values[0]         if not fee_row.empty else None
        gma_rating  = str(fee_row["GMA Rating"].values[0])  if not fee_row.empty else "—"

        results.append({
            "college":      col_name,
            "course":       row["Course"],
            "category":     row["Alloted Category"],
            "last_rank":    int(row["last_rank"]),
            "total_fee":    total_fee,
            "tuition_fee":  tuition_fee,
            "college_type": college_type,
            "gma_rank":     gma_rank,
            "gma_rating":   gma_rating,
            "code":         code,
        })
        if len(results) >= n:
            break

    return results


def get_historical_match(rank: int, category_code: str) -> dict:
    """Finds the student from 2025 who had the closest rank in eligible categories."""
    df = load_kerala_data()
    # Student is eligible for their category and SM (General)
    eligible = df[df["Alloted Category"].isin(["SM", category_code])].copy()
    
    if eligible.empty:
        return None
        
    # Calculate absolute difference to find nearest rank
    eligible["diff"] = (eligible["Rank"] - rank).abs()
    closest_match = eligible.sort_values("diff").iloc[0]
    
    return {
        "historical_rank": int(closest_match["Rank"]),
        "college": str(closest_match["College Name"]),
        "category": str(closest_match["Alloted Category"]),
        "diff": int(closest_match["diff"])
    }


def get_quick_insight(rank: int, category_code: str) -> dict:
    """Summary for the quick-info card shown right after registration."""
    df       = load_kerala_data()
    max_rank = df["Rank"].max()
    percentile = round((1 - rank / max_rank) * 100, 1) if max_rank > 0 else 0

    # Rank band label
    if rank <= 1000:
        band = "Top 1,000 — Excellent rank!"
    elif rank <= 5000:
        band = "Top 5,000 — Very strong rank"
    elif rank <= 10000:
        band = "Top 10,000 — Good rank"
    elif rank <= 20000:
        band = "Top 20,000 — Moderate rank"
    elif rank <= 35000:
        band = "Top 35,000 — Limited options"
    else:
        band = "Above 35,000 — Few options available"

    better_choices = get_better_choices(rank, category_code, n=6)
    historical_match = get_historical_match(rank, category_code)

    return {
        "rank":           rank,
        "category_code":  category_code,
        "percentile":     percentile,
        "rank_band":      band,
        "better_choices": better_choices,
        "historical_match": historical_match,
    }

