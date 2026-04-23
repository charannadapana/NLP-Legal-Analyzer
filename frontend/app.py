import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import time
from datetime import datetime
import random

st.set_page_config(
    page_title="⚖️  Legal Document Analyzer",
    layout="centered",
    page_icon="⚖️",
    initial_sidebar_state="collapsed",
)


if "history" not in st.session_state:
    st.session_state.history = []
if "result" not in st.session_state:
    st.session_state.result = None
if "dark" not in st.session_state:
    st.session_state.dark = True


if st.session_state.dark:
    BG          = "#050A18"
    SURFACE     = "rgba(255,255,255,0.04)"
    TEXT        = "#E2E8F0"
    MUTED       = "#64748B"
    ACCENT      = "#38BDF8"
    BORDER      = "rgba(56,189,248,0.15)"
    CARD_BG     = "rgba(15,23,42,0.85)"
    PLOT_PAPER  = "#0B1120"
    PLOT_FONT   = "#94A3B8"
else:
    BG          = "#F0F9FF"
    SURFACE     = "rgba(0,0,0,0.03)"
    TEXT        = "#0F172A"
    MUTED       = "#64748B"
    ACCENT      = "#0284C7"
    BORDER      = "rgba(2,132,199,0.2)"
    CARD_BG     = "rgba(255,255,255,0.9)"
    PLOT_PAPER  = "#EFF6FF"
    PLOT_FONT   = "#334155"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=IBM+Plex+Mono:wght@400;600&display=swap');

/* ── Reset & Base ── */
* {{ box-sizing: border-box; }}
.stApp {{
    background: {BG};
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, {'#38BDF822' if st.session_state.dark else '#BAE6FD55'}, transparent),
        radial-gradient(ellipse 60% 40% at 80% 100%, {'#A78BFA22' if st.session_state.dark else '#DDD6FE44'}, transparent);
    color: {TEXT};
    font-family: 'IBM Plex Mono', monospace;
}}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 2rem; padding-bottom: 4rem; max-width: 860px; }}

/* ── Animated grid overlay ── */
.stApp::before {{
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient({'rgba(56,189,248,0.04)' if st.session_state.dark else 'rgba(2,132,199,0.04)'} 1px, transparent 1px),
        linear-gradient(90deg, {'rgba(56,189,248,0.04)' if st.session_state.dark else 'rgba(2,132,199,0.04)'} 1px, transparent 1px);
    background-size: 50px 50px;
    mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 30%, transparent 100%);
    pointer-events: none;
    z-index: 0;
}}

/* ── Cards ── */
.card {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 20px;
    padding: 24px 28px;
    margin-bottom: 18px;
    backdrop-filter: blur(16px);
    animation: fadeUp 0.6s ease both;
    position: relative;
    overflow: hidden;
}}
.card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, {ACCENT}44, transparent);
}}

/* ── Section labels ── */
.label {{
    font-size: 11px;
    letter-spacing: 0.2em;
    color: {ACCENT};
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}}
.label::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: {BORDER};
}}

/* ── Pills ── */
.pill {{
    display: inline-block;
    padding: 4px 14px;
    border-radius: 999px;
    border: 1px solid {BORDER};
    font-size: 12px;
    margin: 3px;
    font-family: 'IBM Plex Mono', monospace;
    background: {SURFACE};
    color: {ACCENT};
    transition: all 0.2s;
}}

/* ── Issue / warning box ── */
.issue-box {{
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 13px 16px;
    border-radius: 12px;
    background: rgba(248,113,113,0.07);
    border: 1px solid rgba(248,113,113,0.2);
    margin-bottom: 10px;
    font-size: 13px;
    animation: fadeUp 0.5s ease both;
    color: #FCA5A5;
}}

/* ── Suggestion box ── */
.suggestion-box {{
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 14px;
    padding: 14px 18px;
    border-radius: 14px;
    background: {'rgba(56,189,248,0.05)' if st.session_state.dark else 'rgba(2,132,199,0.05)'};
    border: 1px solid {BORDER};
    margin-bottom: 12px;
    animation: fadeUp 0.5s ease both;
    align-items: start;
}}
.suggestion-clause {{
    background: {'rgba(56,189,248,0.15)' if st.session_state.dark else 'rgba(2,132,199,0.1)'};
    color: {ACCENT};
    border-radius: 8px;
    padding: 4px 12px;
    font-size: 12px;
    font-weight: 600;
    white-space: nowrap;
    font-family: 'IBM Plex Mono', monospace;
}}
.suggestion-text {{
    font-size: 13px;
    color: {MUTED};
    line-height: 1.6;
}}

/* ── History card ── */
.history-card {{
    display: flex;
    align-items: center;
    gap: 16px;
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 16px 20px;
    margin-bottom: 12px;
    animation: fadeUp 0.5s ease both;
    backdrop-filter: blur(12px);
}}

/* ── Risk badge ── */
.risk-badge {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 22px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.1em;
    font-family: 'IBM Plex Mono', monospace;
}}

/* ── Entity tag ── */
.entity-tag {{
    display: inline-block;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 12px;
    margin: 2px;
    font-family: monospace;
}}

/* ── Progress track ── */
.progress-track {{
    background: rgba(255,255,255,0.06);
    border-radius: 99px;
    height: 6px;
    overflow: hidden;
    margin-top: 8px;
}}

/* ── Animations ── */
@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(16px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes glow {{
    0%,100% {{ box-shadow: 0 0 20px {ACCENT}33; }}
    50%      {{ box-shadow: 0 0 40px {ACCENT}66; }}
}}
@keyframes shimmer {{
    0%   {{ background-position: -200% center; }}
    100% {{ background-position:  200% center; }}
}}
@keyframes spin {{
    to {{ transform: rotate(360deg); }}
}}

/* ── File uploader ── */
[data-testid="stFileUploader"] {{
    border: 2px dashed {BORDER};
    border-radius: 20px;
    padding: 24px;
    text-align: center;
    transition: all 0.3s;
    background: {SURFACE};
}}
[data-testid="stFileUploader"]:hover {{
    border-color: {ACCENT};
    background: {'rgba(56,189,248,0.05)' if st.session_state.dark else 'rgba(2,132,199,0.05)'};
}}

/* ── Buttons ── */
.stButton > button {{
    background: linear-gradient(135deg, {ACCENT}, #A78BFA) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 14px 32px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    letter-spacing: 0.08em !important;
    width: 100% !important;
    transition: all 0.3s !important;
    box-shadow: 0 8px 32px {'rgba(56,189,248,0.25)' if st.session_state.dark else 'rgba(2,132,199,0.2)'} !important;
    animation: glow 3s ease infinite !important;
}}
.stButton > button:hover {{
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 0 12px 40px {'rgba(56,189,248,0.4)' if st.session_state.dark else 'rgba(2,132,199,0.35)'} !important;
}}
.stButton > button:active {{
    transform: scale(0.98) !important;
}}

/* ── Nav radio ── */
.stRadio > div {{
    display: flex;
    flex-direction: row !important;
    justify-content: center;
    gap: 12px;
    background: transparent !important;
}}
.stRadio > div > label {{
    border: 1px solid {BORDER} !important;
    border-radius: 999px !important;
    padding: 8px 22px !important;
    cursor: pointer !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
    transition: all 0.25s !important;
    background: {SURFACE} !important;
    color: {MUTED} !important;
}}
.stRadio > div > label:has(input:checked) {{
    border-color: {ACCENT} !important;
    background: {'rgba(56,189,248,0.12)' if st.session_state.dark else 'rgba(2,132,199,0.1)'} !important;
    color: {ACCENT} !important;
}}

/* ── Toggle ── */
.stToggle span {{ font-family: 'IBM Plex Mono', monospace; font-size: 13px; }}

/* ── Spinner ── */
.stSpinner > div {{ border-top-color: {ACCENT} !important; }}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
    background: transparent;
    justify-content: center;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 999px !important;
    border: 1px solid {BORDER} !important;
    background: {SURFACE} !important;
    color: {MUTED} !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
    padding: 8px 20px !important;
}}
.stTabs [aria-selected="true"] {{
    border-color: {ACCENT} !important;
    color: {ACCENT} !important;
    background: {'rgba(56,189,248,0.1)' if st.session_state.dark else 'rgba(2,132,199,0.08)'} !important;
}}
</style>
""", unsafe_allow_html=True)



def risk_config(score):
    if score < 30:
        return {"label": "LOW RISK",    "icon": "🟢", "color": "#34D399", "hex": "34D399"}
    elif score < 70:
        return {"label": "MEDIUM RISK", "icon": "🟡", "color": "#FBBF24", "hex": "FBBF24"}
    else:
        return {"label": "HIGH RISK",   "icon": "🔴", "color": "#F87171", "hex": "F87171"}


def risk_badge_html(score):
    cfg = risk_config(score)
    return f"""
    <div class='risk-badge' style='
        border: 1px solid {cfg["color"]}44;
        background: {cfg["color"]}11;
        color: {cfg["color"]};
    '>
        <span style='font-size:18px'>{cfg["icon"]}</span>
        {cfg["label"]}
    </div>"""


def gauge_chart(score):
    cfg = risk_config(score)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"font": {"size": 48, "color": cfg["color"], "family": "Playfair Display"}},
        title={"text": "RISK SCORE", "font": {"size": 12, "color": MUTED, "family": "IBM Plex Mono"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": MUTED, "tickfont": {"size": 10, "color": MUTED}},
            "bar": {"color": cfg["color"], "thickness": 0.25},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 30],   "color": "rgba(52,211,153,0.12)"},
                {"range": [30, 70],  "color": "rgba(251,191,36,0.10)"},
                {"range": [70, 100], "color": "rgba(248,113,113,0.10)"},
            ],
            "threshold": {
                "line": {"color": cfg["color"], "width": 3},
                "thickness": 0.8,
                "value": score,
            },
        },
    ))
    fig.update_layout(
        height=240,
        margin=dict(l=20, r=20, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": PLOT_FONT},
    )
    return fig


def sparkline_chart(scores, files):
    colors = [risk_config(s)["color"] for s in scores]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=scores, x=files,
        mode="lines+markers+text",
        text=scores,
        textposition="top center",
        textfont={"size": 11, "color": PLOT_FONT, "family": "IBM Plex Mono"},
        line=dict(color=ACCENT, width=2.5, shape="spline"),
        marker=dict(size=10, color=colors, line=dict(color=PLOT_PAPER, width=2)),
        fill="tozeroy",
        fillcolor=f"rgba(56,189,248,0.07)",
    ))
    fig.update_layout(
        height=280,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=40),
        xaxis=dict(showgrid=False, tickfont=dict(size=10, color=MUTED, family="IBM Plex Mono")),
        yaxis=dict(range=[0, 110], showgrid=True, gridcolor=BORDER,
                   tickfont=dict(size=10, color=MUTED)),
        font={"color": PLOT_FONT},
    )
    return fig


def progress_bar_html(value, color):
    return f"""
    <div class='progress-track'>
        <div style='
            height: 100%;
            width: {value}%;
            background: linear-gradient(90deg, {color}88, {color});
            border-radius: 99px;
            box-shadow: 0 0 10px {color}66;
            transition: width 1.2s ease;
        '></div>
    </div>"""


def mock_analyze(filename):
    """Simulate backend analysis."""
    score = random.randint(15, 90)
    clauses = random.sample(
        ["Indemnification", "Non-Compete", "Arbitration", "IP Assignment",
         "Termination", "Force Majeure", "Confidentiality", "Governing Law"], k=5
    )
    issues = [
        "Unlimited liability clause detected in §4.2",
        "Non-compete period exceeds 24 months",
        "Unilateral termination rights for employer only",
    ] if score > 50 else ["Minor formatting inconsistency in §2.1"]

    return {
        "score": score,
        "summary": (
            "This contract contains several concerning clauses related to liability limitations "
            "and unilateral termination rights. The arbitration clause restricts the party's legal "
            "remedies, and the intellectual property assignment is overly broad. "
            "Recommend legal review before signing."
        ),
        "clauses": clauses,
        "entities": {
            "Parties":      ["Acme Corp", "John Doe"],
            "Dates":        ["2025-01-01", "2026-12-31"],
            "Jurisdiction": ["State of California"],
        },
        "issues": issues,
        "suggestions": [
            {"clause": "Non-Compete",  "suggestion": "Limit scope to 12 months and restrict geography."},
            {"clause": "Arbitration",  "suggestion": "Negotiate for class action rights retention."},
            {"clause": "IP Assignment","suggestion": "Carve out pre-existing IP and personal projects."},
        ],
    }



st.markdown("""
<div style='text-align:center; padding: 20px 0 10px;'>
    <div style='font-size:11px; letter-spacing:0.25em; color:#38BDF8; margin-bottom:14px; font-family: IBM Plex Mono, monospace;'>
        ── AI-POWERED LEGAL INTELLIGENCE ──
    </div>
    <div style='font-size:64px; line-height:1; margin-bottom:8px; filter:drop-shadow(0 0 30px #38BDF866);'>⚖️</div>
    <h1 style='
        font-family: Playfair Display, Georgia, serif;
        font-size: clamp(36px, 6vw, 58px);
        font-weight: 800;
        background: linear-gradient(135deg, #fff 30%, #38BDF8, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 10px;
        line-height: 1.1;
    '>Legal Analyzer</h1>
    <p style='color:#64748B; font-family: IBM Plex Mono, monospace; font-size:13px; margin:0;'>
        Upload · Analyze · Understand your legal exposure
    </p>
</div>
""", unsafe_allow_html=True)

# Dark mode toggle (right-aligned)
tcol1, tcol2, tcol3 = st.columns([3, 1, 1])
with tcol3:
    st.session_state.dark = st.toggle("🌙 Dark", value=st.session_state.dark)

st.markdown("<br>", unsafe_allow_html=True)


tab_analyzer, tab_trends, tab_history = st.tabs(["⚖️ Analyzer", "📈 Trends", "🕘 History"])



with tab_analyzer:

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"<div style='background:{CARD_BG};border:1px solid {BORDER};border-radius:20px;padding:24px 28px;"
        f"backdrop-filter:blur(16px);margin-bottom:18px;'>"
        f"<div style='font-size:11px;letter-spacing:0.2em;color:{ACCENT};margin-bottom:14px;"
        f"display:flex;align-items:center;gap:10px;font-family:monospace;'>"
        f"UPLOAD CONTRACT<span style='flex:1;height:1px;background:{BORDER};display:inline-block;'></span></div></div>",
        unsafe_allow_html=True
    )
    uploaded = st.file_uploader("Drop your PDF or TXT contract here", type=["pdf", "txt"])


    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        analyze = st.button("⚖️  ANALYZE ", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if uploaded and analyze:
        with st.spinner("🔍 Scanning clauses and extracting entities..."):
            time.sleep(0.6)
            prog = st.progress(0, text="Initializing analysis…")
            steps = [
                (25, "📄 Parsing document structure…"),
                (50, "🔍 Identifying clauses…"),
                (75, "⚠️ Evaluating risk factors…"),
                (100, "✅ Generating insights…"),
            ]
            for val, msg in steps:
                time.sleep(0.45)
                prog.progress(val, text=msg)
            time.sleep(0.3)
            prog.empty()

            data = mock_analyze(uploaded.name)
            st.session_state.result = data
            st.session_state.history.append({
                "file":  uploaded.name,
                "score": data["score"],
                "time":  datetime.now().strftime("%H:%M:%S"),
            })

   
    data = st.session_state.result
    if data:
        score = data["score"]
        cfg   = risk_config(score)

   
        col_g, col_s = st.columns([1, 1], gap="medium")

        with col_g:
            st.markdown(
                f"<div style='background:{CARD_BG};border:1px solid {BORDER};border-radius:20px;padding:20px 28px 10px;"
                f"backdrop-filter:blur(16px);text-align:center;'>"
                f"<div style='font-size:11px;letter-spacing:0.2em;color:{ACCENT};margin-bottom:4px;"
                f"font-family:monospace;'>RISK ASSESSMENT</div></div>",
                unsafe_allow_html=True
            )
            st.plotly_chart(gauge_chart(score), use_container_width=True, config={"displayModeBar": False})
            st.markdown(
                f"<div style='text-align:center;margin-top:-12px;margin-bottom:12px;'>{risk_badge_html(score)}</div>",
                unsafe_allow_html=True
            )

        with col_s:
            st.markdown(
                f"<div style='background:{CARD_BG};border:1px solid {BORDER};border-radius:20px;padding:20px 28px 10px;"
                f"backdrop-filter:blur(16px);'>"
                f"<div style='font-size:11px;letter-spacing:0.2em;color:#A78BFA;margin-bottom:10px;"
                f"font-family:monospace;'>AI SUMMARY</div></div>",
                unsafe_allow_html=True
            )
            # Typewriter via st.empty
            placeholder = st.empty()
            typed = ""
            for ch in data["summary"]:
                typed += ch
                placeholder.markdown(
                    f"<p style='font-size:13px;line-height:1.8;color:{MUTED};font-family:IBM Plex Mono,monospace;'>{typed}▋</p>",
                    unsafe_allow_html=True
                )
                time.sleep(0.008)
            placeholder.markdown(
                f"<p style='font-size:13px;line-height:1.8;color:{MUTED};font-family:IBM Plex Mono,monospace;'>{typed}</p>",
                unsafe_allow_html=True
            )

        
        issues_html = ""
        for issue in data["issues"]:
            issues_html += (
                f"<div style='display:flex;align-items:flex-start;gap:12px;padding:13px 16px;"
                f"border-radius:12px;background:rgba(248,113,113,0.07);border:1px solid rgba(248,113,113,0.22);"
                f"margin-bottom:10px;font-size:13px;color:#FCA5A5;font-family:IBM Plex Mono,monospace;'>"
                f"<span style='font-size:18px;flex-shrink:0;'>⚠</span><span>{issue}</span></div>"
            )
        st.markdown(
            f"<div style='background:{CARD_BG};border:1px solid {BORDER};border-radius:20px;padding:24px 28px;"
            f"backdrop-filter:blur(16px);margin-bottom:18px;position:relative;overflow:hidden;'>"
            f"<div style='font-size:11px;letter-spacing:0.2em;color:#F87171;margin-bottom:14px;"
            f"display:flex;align-items:center;gap:10px;font-family:monospace;'>"
            f"⚠ DETECTED ISSUES<span style='flex:1;height:1px;background:rgba(248,113,113,0.2);display:inline-block;'></span></div>"
            f"{issues_html}</div>",
            unsafe_allow_html=True
        )

   
        col_c, col_e = st.columns([1, 1], gap="medium")

        with col_c:
            pills_html = "".join(
                f"<span style='display:inline-block;padding:4px 14px;border-radius:999px;"
                f"border:1px solid {BORDER};font-size:12px;margin:3px;font-family:IBM Plex Mono,monospace;"
                f"background:rgba(56,189,248,0.08);color:{ACCENT};'>{c}</span>"
                for c in data["clauses"]
            )
            st.markdown(
                f"<div style='background:{CARD_BG};border:1px solid {BORDER};border-radius:20px;padding:24px 28px;"
                f"backdrop-filter:blur(16px);'>"
                f"<div style='font-size:11px;letter-spacing:0.2em;color:#FBBF24;margin-bottom:14px;"
                f"display:flex;align-items:center;gap:10px;font-family:monospace;'>"
                f"DETECTED CLAUSES<span style='flex:1;height:1px;background:rgba(251,191,36,0.2);display:inline-block;'></span></div>"
                f"<div>{pills_html}</div></div>",
                unsafe_allow_html=True
            )

        with col_e:
            ent_colors = ["#34D399", "#38BDF8", "#A78BFA"]
            entity_html = ""
            for i, (k, vs) in enumerate(data["entities"].items()):
                c = ent_colors[i % len(ent_colors)]
                tags = "".join(
                    f"<span style='display:inline-block;padding:3px 10px;border-radius:6px;font-size:12px;margin:2px;"
                    f"background:{c}18;border:1px solid {c}44;color:{c};font-family:monospace;'>{v}</span>"
                    for v in vs
                )
                entity_html += (
                    f"<div style='margin-bottom:14px;'>"
                    f"<div style='font-size:10px;letter-spacing:0.12em;color:{MUTED};margin-bottom:5px;font-family:monospace;'>{k.upper()}</div>"
                    f"<div>{tags}</div>"
                    f"</div>"
                )
            st.markdown(
                f"<div style='background:{CARD_BG};border:1px solid {BORDER};border-radius:20px;padding:24px 28px;backdrop-filter:blur(16px);position:relative;overflow:hidden;'>"
                f"<div style='font-size:11px;letter-spacing:0.2em;color:#34D399;margin-bottom:14px;display:flex;align-items:center;gap:10px;font-family:monospace;'>"
                f"ENTITIES<span style='flex:1;height:1px;background:{BORDER};display:inline-block;'></span></div>"
                f"{entity_html}</div>",
                unsafe_allow_html=True
            )

      
        sug_html = ""
        for s in data["suggestions"]:
            sug_html += (
                f"<div style='display:grid;grid-template-columns:auto 1fr;gap:14px;padding:14px 18px;"
                f"border-radius:14px;background:{'rgba(56,189,248,0.05)'};border:1px solid {BORDER};"
                f"margin-bottom:12px;align-items:start;'>"
                f"<div style='background:{'rgba(56,189,248,0.15)'};color:{ACCENT};border-radius:8px;"
                f"padding:4px 12px;font-size:12px;font-weight:600;white-space:nowrap;"
                f"font-family:IBM Plex Mono,monospace;'>{s['clause']}</div>"
                f"<div style='font-size:13px;color:{MUTED};line-height:1.6;font-family:IBM Plex Mono,monospace;'>{s['suggestion']}</div>"
                f"</div>"
            )
        st.markdown(
            f"<div style='background:{CARD_BG};border:1px solid {BORDER};border-radius:20px;padding:24px 28px;"
            f"backdrop-filter:blur(16px);margin-bottom:18px;position:relative;overflow:hidden;'>"
            f"<div style='font-size:11px;letter-spacing:0.2em;color:{ACCENT};margin-bottom:14px;"
            f"display:flex;align-items:center;gap:10px;font-family:monospace;'>"
            f"💡 RECOMMENDATIONS<span style='flex:1;height:1px;background:{BORDER};display:inline-block;'></span></div>"
            f"{sug_html}</div>",
            unsafe_allow_html=True
        )

    elif not uploaded:
        st.markdown(f"""
        <div style='text-align:center; padding: 60px 0; color:{MUTED}; font-family: IBM Plex Mono, monospace; font-size:14px;'>
            <div style='font-size:48px; margin-bottom:16px;'>📂</div>
            Upload a contract above to begin analysis
        </div>""", unsafe_allow_html=True)



with tab_trends:
    st.markdown("<br>", unsafe_allow_html=True)

    if len(st.session_state.history) >= 2:
        h = st.session_state.history
        scores = [i["score"] for i in h]
        files  = [i["file"][:18] + "…" if len(i["file"]) > 18 else i["file"] for i in h]

        # Stats row
        avg_s = round(sum(scores) / len(scores))
        max_s = max(scores)
        min_s = min(scores)

        stat_cols = st.columns(3, gap="medium")
        for col, label, val, color in zip(
            stat_cols,
            ["AVG RISK", "PEAK RISK", "LOWEST"],
            [avg_s, max_s, min_s],
            [ACCENT, "#F87171", "#34D399"],
        ):
            with col:
                st.markdown(f"""
                <div class='card' style='text-align:center; padding:20px 12px;'>
                    <div style='font-size:40px; font-weight:800; color:{color}; font-family:Playfair Display,serif;'>{val}</div>
                    <div style='font-size:10px; letter-spacing:0.15em; color:{MUTED}; margin-top:6px;'>{label}</div>
                    {progress_bar_html(val, color)}
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<div class='card'><div class='label'>RISK SCORE HISTORY</div>", unsafe_allow_html=True)
        st.plotly_chart(sparkline_chart(scores, files), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div style='text-align:center; padding:80px 0; color:{MUTED}; font-family:IBM Plex Mono,monospace;'>
            <div style='font-size:48px; margin-bottom:16px;'>📈</div>
            Analyze 2 or more contracts to see trend data
        </div>""", unsafe_allow_html=True)



with tab_history:
    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.history:
        for item in reversed(st.session_state.history):
            cfg = risk_config(item["score"])
            st.markdown(f"""
            <div class='history-card'>
                <div style='
                    width:52px; height:52px; flex-shrink:0;
                    border-radius:14px;
                    background:{cfg["color"]}14;
                    border:1px solid {cfg["color"]}33;
                    display:flex; align-items:center; justify-content:center;
                    font-size:22px;
                '>📄</div>
                <div style='flex:1; min-width:0;'>
                    <div style='
                        font-family:IBM Plex Mono,monospace;
                        font-size:13px; font-weight:600;
                        color:{TEXT};
                        white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
                        margin-bottom:8px;
                    '>{item["file"]}</div>
                    {progress_bar_html(item["score"], cfg["color"])}
                </div>
                <div style='text-align:right; flex-shrink:0;'>
                    <div style='font-size:28px; font-weight:800; color:{cfg["color"]}; font-family:Playfair Display,serif;'>
                        {item["score"]}
                    </div>
                    <div style='font-size:10px; color:{MUTED}; font-family:monospace;'>{item["time"]}</div>
                </div>
            </div>""", unsafe_allow_html=True)

        # Clear button
        st.markdown("<br>", unsafe_allow_html=True)
        cc1, cc2, cc3 = st.columns([2, 1, 2])
        with cc2:
            if st.button("🗑 Clear History", use_container_width=True):
                st.session_state.history = []
                st.rerun()
    else:
        st.markdown(f"""
        <div style='text-align:center; padding:80px 0; color:{MUTED}; font-family:IBM Plex Mono,monospace;'>
            <div style='font-size:48px; margin-bottom:16px;'>🕘</div>
            No uploads yet — analyze a contract to get started
        </div>""", unsafe_allow_html=True)


st.markdown(f"""
<div style='text-align:center; margin-top:48px; opacity:0.2; font-size:11px;
     font-family:IBM Plex Mono,monospace; letter-spacing:0.12em; color:{MUTED};'>
    ── AI LEGAL ANALYZER · NOT LEGAL ADVICE ──
</div>""", unsafe_allow_html=True)