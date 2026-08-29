"""
UI & Helper Utilities for Q-DRUG Platform.
Provides dark biotech + quantum theme styling, custom cards, alerts, and state management.
"""

import streamlit as st
from config import THEME_COLORS, SCIENTIFIC_DISCLAIMER

def inject_custom_css():
    """
    Injects custom CSS styling for futuristic dark biotech & quantum visual style.
    """
    css = f"""
    <style>
    /* Dark Biotech Global Styling */
    .stApp {{
        background-color: {THEME_COLORS['background']};
        color: {THEME_COLORS['text_main']};
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }}
    
    /* Main Header Styling */
    .main-title {{
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, {THEME_COLORS['primary']} 0%, {THEME_COLORS['secondary']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }}
    .sub-title {{
        font-size: 1.1rem;
        color: {THEME_COLORS['text_muted']};
        text-align: center;
        margin-bottom: 1.8rem;
        font-weight: 400;
    }}
    
    /* Custom Card Containers */
    .q-card {{
        background: {THEME_COLORS['card_bg']};
        border: 1px solid {THEME_COLORS['card_border']};
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0, 240, 255, 0.05);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }}
    .q-card:hover {{
        border-color: {THEME_COLORS['primary']};
        box-shadow: 0 6px 25px rgba(0, 240, 255, 0.12);
    }}
    
    .q-card-glow {{
        background: linear-gradient(145deg, #12192A 0%, #1A102F 100%);
        border: 1px solid {THEME_COLORS['secondary']};
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 0 15px rgba(138, 43, 226, 0.2);
    }}
    
    /* Metric Card */
    .q-metric-card {{
        background: #0E1524;
        border: 1px solid #1E293B;
        border-left: 4px solid {THEME_COLORS['primary']};
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }}
    .q-metric-value {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {THEME_COLORS['primary']};
    }}
    .q-metric-label {{
        font-size: 0.85rem;
        color: {THEME_COLORS['text_muted']};
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    /* Status Badges */
    .badge-demo {{
        background-color: rgba(255, 179, 0, 0.15);
        color: {THEME_COLORS['warning']};
        border: 1px solid {THEME_COLORS['warning']};
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }}
    .badge-simulated {{
        background-color: rgba(0, 240, 255, 0.15);
        color: {THEME_COLORS['primary']};
        border: 1px solid {THEME_COLORS['primary']};
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }}
    .badge-predictive {{
        background-color: rgba(138, 43, 226, 0.15);
        color: {THEME_COLORS['secondary']};
        border: 1px solid {THEME_COLORS['secondary']};
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }}
    .badge-pubchem {{
        background-color: rgba(0, 255, 136, 0.15);
        color: #00FF88;
        border: 1px solid #00FF88;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }}
    .badge-cache {{
        background-color: rgba(255, 179, 0, 0.15);
        color: #FFB300;
        border: 1px solid #FFB300;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }}
    
    /* Pass/Fail Tags */
    .tag-pass {{
        background-color: rgba(0, 255, 136, 0.15);
        color: {THEME_COLORS['success']};
        border: 1px solid {THEME_COLORS['success']};
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        font-weight: 700;
    }}
    .tag-fail {{
        background-color: rgba(255, 51, 102, 0.15);
        color: {THEME_COLORS['danger']};
        border: 1px solid {THEME_COLORS['danger']};
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        font-weight: 700;
    }}
    
    /* Recommendation Badges */
    .rec-highly-promising {{
        background-color: rgba(0, 255, 136, 0.2);
        color: #00FF88;
        font-weight: bold;
        padding: 4px 8px;
        border-radius: 6px;
    }}
    .rec-promising {{
        background-color: rgba(0, 240, 255, 0.2);
        color: #00F0FF;
        font-weight: bold;
        padding: 4px 8px;
        border-radius: 6px;
    }}
    .rec-moderate {{
        background-color: rgba(255, 179, 0, 0.2);
        color: #FFB300;
        font-weight: bold;
        padding: 4px 8px;
        border-radius: 6px;
    }}
    .rec-low-priority {{
        background-color: rgba(148, 163, 184, 0.2);
        color: #94A3B8;
        font-weight: bold;
        padding: 4px 8px;
        border-radius: 6px;
    }}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: #0D131F;
        border-right: 1px solid #1E2A45;
    }}
    
    /* Disclaimer Banner */
    .disclaimer-banner {{
        background: rgba(255, 179, 0, 0.08);
        border: 1px dashed {THEME_COLORS['warning']};
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-size: 0.8rem;
        color: {THEME_COLORS['warning']};
        margin-bottom: 1.5rem;
        line-height: 1.4;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_disclaimer_banner():
    """
    Displays scientific honesty banner across modules.
    """
    st.markdown(
        f"""
        <div class="disclaimer-banner">
            ⚠️ <b>SCIENTIFIC HONESTY DISCLAIMER</b><br/>
            {SCIENTIFIC_DISCLAIMER}
        </div>
        """,
        unsafe_allow_html=True
    )

def render_section_header(title, subtitle=None, badge=None):
    """
    Renders styled section headers with optional status badge.
    """
    badge_html = f'<span class="badge-{badge.lower()}">{badge.upper()}</span>' if badge else ""
    sub_html = f'<p style="color: {THEME_COLORS["text_muted"]}; margin-top: -5px;">{subtitle}</p>' if subtitle else ""
    st.markdown(
        f"""
        <div style="margin-bottom: 1.2rem; border-bottom: 1px solid #1E2A45; padding-bottom: 0.5rem;">
            <h2 style="color: {THEME_COLORS['text_main']}; margin: 0; display: inline-block;">{title}</h2>
            {badge_html}
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True
    )

def initialize_session_state():
    """
    Initializes session state defaults for Q-DRUG app.
    """
    if "selected_target_key" not in st.session_state:
        st.session_state["selected_target_key"] = "SARS-CoV-2 Mpro"
    if "selected_candidate_id" not in st.session_state:
        st.session_state["selected_candidate_id"] = "QD-101"
    if "optimized_candidates" not in st.session_state:
        st.session_state["optimized_candidates"] = []
    if "tour_active" not in st.session_state:
        st.session_state["tour_active"] = False
    if "tour_step" not in st.session_state:
        st.session_state["tour_step"] = 1
    if "vqe_results" not in st.session_state:
        st.session_state["vqe_results"] = None
    if "active_lead" not in st.session_state:
        st.session_state["active_lead"] = None
