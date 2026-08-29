"""
AeroTwin-PX v2: Ground Control Station (GCS) Defense Avionics Dashboard
Bespoke Aerospace UI for Real-Time Aero-Piston Engine Digital Twin Health Monitoring,
AI Diagnostics, RUL Estimation, Mission Reliability Simulation, and Cryptographic Audit Logs.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time

from synthesizer import TelemetrySynthesizer
from physics_engine import EKFStateEstimator
from health_engine import EngineHealthEngine
from models import AIDiagnosticsSuite
from reliability_engine import MissionReliabilityEngine
from audit_log import CryptographicAuditLog
from database import AeroTwinDatabase
import importlib
import twin_adapter
import twin_3d
importlib.reload(twin_3d)
from twin_adapter import TwinVisualizationAdapter
from twin_3d import render_3d_digital_twin, render_3d_background_canvas




# Page Configuration
st.set_page_config(
    page_title="AeroTwin-PX v2 | Defense Avionics GCS",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling — Rerun-inspired "Light Technical Grid" Aerospace Theme
st.markdown("""
<style>
    /* ─── FONT ─────────────────────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ─── DESIGN TOKENS ─────────────────────────────────────────────────────
       Single source of truth — change here, flows everywhere.
    ─────────────────────────────────────────────────────────────────────── */
    :root {
        --bg-base:        #FAFAF9;   /* off-white paper */
        --bg-surface:     #ffffff;   /* card / panel surface */
        --bg-secondary:   #F4F4F2;   /* sidebar / inset */
        --border-hairline:#e5e5e5;   /* 1px dividers */
        --border-subtle:  #d1d5db;   /* slightly stronger rule */
        --text-primary:   #1a1a1a;   /* near-black body */
        --text-secondary: #6b7280;   /* mid-gray secondary */
        --text-tertiary:  #9ca3af;   /* labels / sub-text */
        --accent:         #2563eb;   /* single accent (blue) */
        --accent-warn:    #d97706;   /* amber warning */
        --accent-danger:  #dc2626;   /* red critical */
        --accent-ok:      #16a34a;   /* green nominal */
        --grid-line-size: 28px;      /* graph-paper cell size */
    }

    /* ─── GRAPH-PAPER GRID BACKGROUND ──────────────────────────────────────
       Fine 1px crosshatch — the signature Rerun "spec-sheet" feel.
    ─────────────────────────────────────────────────────────────────────── */
    .stApp {
        background-color: var(--bg-base);
        background-image:
            linear-gradient(to right,  rgba(0,0,0,0.045) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(0,0,0,0.045) 1px, transparent 1px);
        background-size: var(--grid-line-size) var(--grid-line-size);
        font-family: 'Inter', sans-serif;
        color: var(--text-primary);
    }

    /* ─── STREAMLIT CORE OVERRIDES ──────────────────────────────────────── */
    .stApp header,
    .stApp > div:first-child {
        background: transparent !important;
    }

    /* Sidebar — opaque white panel, right hairline */
    .stSidebar,
    section[data-testid="stSidebar"] {
        background: var(--bg-surface) !important;
        border-right: 1px solid var(--border-hairline) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
    }
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
        padding-top: 0 !important;
    }
    /* Sidebar title */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2 {
        font-size: 13px !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        margin-bottom: 2px !important;
    }
    section[data-testid="stSidebar"] .stCaption,
    section[data-testid="stSidebar"] small {
        font-size: 10px !important;
        letter-spacing: 0.8px !important;
        color: var(--text-tertiary) !important;
        text-transform: uppercase !important;
    }

    /* ─── TABS — Hairline rule, uppercase tracked labels ───────────────── */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-surface);
        border-bottom: 1px solid var(--border-hairline);
        border-top: 1px solid var(--border-hairline);
        border-left: 1px solid var(--border-hairline);
        border-right: 1px solid var(--border-hairline);
        border-radius: 3px 3px 0 0;
        gap: 0;
        padding: 0 4px;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.9px;
        text-transform: uppercase;
        color: var(--text-secondary);
        border-bottom: 2px solid transparent;
        border-right: 1px solid var(--border-hairline);
        padding: 10px 14px;
        background: transparent;
        transition: color 0.15s ease, border-bottom-color 0.15s ease;
    }
    .stTabs [data-baseweb="tab"]:last-child { border-right: none; }
    .stTabs [data-baseweb="tab"]:hover { color: var(--text-primary); }
    .stTabs [aria-selected="true"] {
        color: var(--accent) !important;
        border-bottom-color: var(--accent) !important;
        background: rgba(37,99,235,0.03) !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        border: 1px solid var(--border-hairline);
        border-top: none;
        background: var(--bg-base);
        padding: 16px !important;
    }

    hr { border-color: var(--border-hairline) !important; }

    /* ─── HUD CARDS — flat, bordered cells, no shadow ─────────────────── */
    .hud-card {
        background: var(--bg-surface);
        border: 1px solid var(--border-hairline);
        border-radius: 3px;
        padding: 16px 20px;
        box-shadow: none;
        position: relative;
        overflow: hidden;
        margin-bottom: 12px;
        transition: border-color 0.15s ease;
    }
    .hud-card:hover { border-color: var(--border-subtle); }
    .hud-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 2px; height: 100%;
        background: var(--accent);
    }
    .hud-card-warning { background: var(--bg-surface); border: 1px solid var(--border-hairline); border-radius: 3px; padding: 16px 20px; box-shadow: none; position: relative; overflow: hidden; margin-bottom: 12px; }
    .hud-card-warning::before { content:''; position:absolute; top:0; left:0; width:2px; height:100%; background: var(--accent-warn); }
    .hud-card-critical { background: var(--bg-surface); border: 1px solid #fecaca; border-radius: 3px; padding: 16px 20px; box-shadow: none; position: relative; overflow: hidden; margin-bottom: 12px; }
    .hud-card-critical::before { content:''; position:absolute; top:0; left:0; width:2px; height:100%; background: var(--accent-danger); }

    /* ─── HUD TYPOGRAPHY ────────────────────────────────────────────────── */
    .hud-title {
        font-family: 'Inter', sans-serif;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 1.4px;
        color: var(--text-secondary);
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .hud-value {
        font-family: 'Inter', sans-serif;
        font-size: 24px;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1.1;
    }
    .hud-sub {
        font-size: 11px;
        color: var(--text-tertiary);
        margin-top: 3px;
        letter-spacing: 0.3px;
    }

    /* ─── SECTION EYEBROW LABEL utility ─────────────────────────────────
       Usage: <div class="section-eyebrow">SECTION NAME</div>
    ─────────────────────────────────────────────────────────────────────── */
    .section-eyebrow {
        font-family: 'Inter', sans-serif;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 1.8px;
        color: var(--text-tertiary);
        text-transform: uppercase;
        margin-bottom: 6px;
        display: block;
    }

    /* ─── TOP HEADER BAR — flush, square, hairline-bordered ────────────── */
    .avionics-header {
        background: var(--bg-surface);
        border: 1px solid var(--border-hairline);
        border-radius: 3px;
        padding: 12px 22px;
        margin-bottom: 16px;
        box-shadow: none;
        display: flex;
        justify-content: space-between;
        align-items: center;
        /* Accent left rail */
        border-left: 3px solid var(--accent);
    }

    /* ─── BADGES ─────────────────────────────────────────────────────────── */
    .hud-badge {
        display: inline-block;
        padding: 3px 9px;
        border-radius: 2px;
        font-family: 'Inter', sans-serif;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.9px;
        text-transform: uppercase;
        margin-right: 6px;
    }
    .badge-cyan    { background: #eff6ff; color: var(--accent);       border: 1px solid #bfdbfe; }
    .badge-emerald { background: #f0fdf4; color: var(--accent-ok);    border: 1px solid #bbf7d0; }
    .badge-amber   { background: #fffbeb; color: var(--accent-warn);  border: 1px solid #fde68a; }

    /* ─── LIVE PULSE DOT ────────────────────────────────────────────────── */
    .pulse-dot {
        display: inline-block;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: var(--accent-ok);
        animation: pulseAnimation 1.5s infinite alternate;
        margin-right: 5px;
        vertical-align: middle;
    }
    @keyframes pulseAnimation {
        0%   { opacity: 0.4; transform: scale(0.85); }
        100% { opacity: 1;   transform: scale(1.15); }
    }

    /* ─── STREAMLIT METRICS — flat bordered cells ──────────────────────── */
    [data-testid="metric-container"] {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-hairline) !important;
        border-radius: 3px !important;
        padding: 14px 16px !important;
        box-shadow: none !important;
    }
    [data-testid="metric-container"] label {
        font-size: 10px !important;
        font-weight: 600 !important;
        letter-spacing: 1.2px !important;
        text-transform: uppercase !important;
        color: var(--text-secondary) !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 22px !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        line-height: 1.2 !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricDelta"] {
        font-size: 11px !important;
    }

    /* ─── BUTTONS — flat, bordered, no shadow ──────────────────────────── */
    .stButton > button {
        background: var(--bg-surface) !important;
        color: var(--accent) !important;
        border: 1px solid var(--accent) !important;
        border-radius: 3px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
        padding: 6px 16px !important;
        box-shadow: none !important;
        transition: background 0.15s ease, color 0.15s ease;
    }
    .stButton > button:hover {
        background: var(--accent) !important;
        color: #ffffff !important;
    }
    .stButton > button:active {
        opacity: 0.85 !important;
    }

    /* ─── PROGRESS BAR — flat accent, no radius ──────────────────────── */
    .stProgress > div > div > div {
        background-color: var(--accent) !important;
        border-radius: 0 !important;
    }
    .stProgress > div > div {
        background-color: var(--border-hairline) !important;
        border-radius: 0 !important;
        height: 4px !important;
    }

    /* ─── INPUTS & SELECTBOX — flat bordered ────────────────────────────── */
    .stTextInput input,
    .stSelectbox select,
    div[data-baseweb="select"] > div {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-hairline) !important;
        border-radius: 3px !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
        box-shadow: none !important;
        transition: border-color 0.15s ease !important;
    }
    .stTextInput input:focus,
    div[data-baseweb="select"] > div:focus-within {
        border-color: var(--accent) !important;
        box-shadow: none !important;
    }

    /* ─── SLIDER ─────────────────────────────────────────────────────────── */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background: var(--accent) !important;
        border: 2px solid var(--accent) !important;
        box-shadow: none !important;
    }

    /* ─── PLOTLY CHART FRAME — thin border wrapper ──────────────────────── */
    .stPlotlyChart {
        border: 1px solid var(--border-hairline) !important;
        border-radius: 3px !important;
        overflow: hidden !important;
        background: var(--bg-surface) !important;
    }

    /* ─── DATAFRAME — grid-style table ──────────────────────────────────── */
    .stDataFrame {
        border: 1px solid var(--border-hairline) !important;
        border-radius: 3px !important;
        overflow: hidden;
    }
    .stDataFrame table {
        border-collapse: collapse !important;
        font-size: 12px !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    .stDataFrame th {
        background: var(--bg-secondary) !important;
        border-bottom: 1px solid var(--border-subtle) !important;
        font-size: 10px !important;
        font-weight: 600 !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
        color: var(--text-secondary) !important;
        padding: 8px 12px !important;
    }
    .stDataFrame td {
        border-bottom: 1px solid var(--border-hairline) !important;
        padding: 6px 12px !important;
        color: var(--text-primary) !important;
    }

    /* ─── ALERTS / INFO / WARNING / ERROR — flat treatment ─────────────── */
    .stAlert {
        border-radius: 3px !important;
        border-left-width: 3px !important;
        box-shadow: none !important;
        font-size: 13px !important;
    }
    div[data-baseweb="notification"] {
        border-radius: 3px !important;
        box-shadow: none !important;
    }

    /* ─── CUSTOM SCROLLBAR — thin monochrome ────────────────────────────── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: var(--bg-base); }
    ::-webkit-scrollbar-thumb {
        background: var(--border-subtle);
        border-radius: 0;
    }
    ::-webkit-scrollbar-thumb:hover { background: var(--text-secondary); }

    /* ─── CHECKBOX — styled ─────────────────────────────────────────────── */
    .stCheckbox label {
        font-family: 'Inter', sans-serif !important;
        font-size: 12px !important;
        color: var(--text-primary) !important;
    }

    /* ─── SUBHEADER / SECTION HEADINGS in tabs ─────────────────────────── */
    .stMarkdown h3, .stSubheader {
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        letter-spacing: 0.3px !important;
        color: var(--text-primary) !important;
        border-bottom: 1px solid var(--border-hairline) !important;
        padding-bottom: 6px !important;
        margin-bottom: 12px !important;
    }

    /* ─── CAPTION TEXT ──────────────────────────────────────────────────── */
    .stMarkdown small, .stCaption {
        font-size: 11px !important;
        color: var(--text-tertiary) !important;
        letter-spacing: 0.3px !important;
    }

    /* ─── DIVIDER ────────────────────────────────────────────────────────── */
    hr {
        border: none !important;
        border-top: 1px solid var(--border-hairline) !important;
        margin: 14px 0 !important;
    }

    /* ─── JSON viewer ────────────────────────────────────────────────────── */
    .stJson {
        border: 1px solid var(--border-hairline) !important;
        border-radius: 3px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 11px !important;
        background: var(--bg-secondary) !important;
    }

</style>
""", unsafe_allow_html=True)

# Initialize Session State Singleton Engines & DB
if "db" not in st.session_state:
    st.session_state.db = AeroTwinDatabase()
    st.session_state.synthesizer = TelemetrySynthesizer()
    st.session_state.ekf = EKFStateEstimator()
    st.session_state.health_engine = EngineHealthEngine()
    st.session_state.ai_suite = AIDiagnosticsSuite()
    st.session_state.reliability_engine = MissionReliabilityEngine()
    st.session_state.audit_log = CryptographicAuditLog()
    st.session_state.step = 0
    st.session_state.telemetry_history = []

# Sidebar Avionics Controls
st.sidebar.image("https://img.icons8.com/color/96/drone.png", width=70)
st.sidebar.title("AERO-AVIONICS GCS")
st.sidebar.caption("DRDO / SIH PS 26054 Defense Suite")
st.sidebar.divider()

st.sidebar.subheader("🕹️ Mission Flight Profile")
profile = st.sidebar.selectbox(
    "Operating Envelope",
    ["Normal Cruise", "High Altitude (18,000 ft)", "Hot Weather (42°C)", "Rapid Throttle", "Long Endurance"]
)

st.sidebar.subheader("⚠️ Fault Injector (Demonstration)")
fault_choice = st.sidebar.selectbox(
    "Inject Synthetic Fault",
    ["None / Healthy", "Cylinder Misfire", "Injector Coking", "Lubrication Failure", "Sensor Drift", "Combustion Instability", "Thermal Overheating", "Abnormal Vibration"]
)

fault_severity = st.sidebar.slider("Fault Severity", 0.0, 1.0, 0.0 if fault_choice == "None / Healthy" else 0.7, 0.1)

st.sidebar.divider()
auto_run = st.sidebar.checkbox("Auto-Stream Telemetry (10 Hz)", value=False)
if st.sidebar.button("Step Telemetry (+1 Tick)") or auto_run:
    st.session_state.step += 1

if st.sidebar.button("Reset Telemetry & Audit Log"):
    st.session_state.step = 0
    st.session_state.telemetry_history = []
    st.session_state.audit_log = CryptographicAuditLog()
    st.rerun()

# Map UI fault choice to synthesizer strings
fault_map_str = {
    "None / Healthy": "none",
    "Cylinder Misfire": "misfire",
    "Injector Coking": "injector_coking",
    "Lubrication Failure": "lubrication_loss",
    "Sensor Drift": "sensor_drift",
    "Combustion Instability": "combustion_instability",
    "Thermal Overheating": "overheating",
    "Abnormal Vibration": "abnormal_vibration"
}

# Generate Current Telemetry Frame
current_fault_key = fault_map_str[fault_choice]
frame = st.session_state.synthesizer.generate_frame(
    profile=profile,
    fault_type=current_fault_key,
    severity=fault_severity,
    step=st.session_state.step
)

# Process through EKF & Physics Engine
ekf_res = st.session_state.ekf.process_step(frame)
residuals = ekf_res["physics_residuals"]
mvem_exp = ekf_res["mvem_expected"]

# Process through Health Engine & Sensor Validator
sensor_health = st.session_state.health_engine.evaluate_sensor_health(frame, residuals)
subsystem_health = st.session_state.health_engine.compute_subsystem_health(frame, residuals)

# Process through AI Diagnostics
ai_res = st.session_state.ai_suite.predict_diagnostics(frame, residuals)

# Extract Unified Twin State for 3D Visualization
twin_visualization_state = TwinVisualizationAdapter.extract_twin_state(
    telemetry=frame,
    mvem_exp=mvem_exp,
    ekf_est=ekf_res["ekf_estimated_state"],
    residuals=residuals,
    sensor_health=sensor_health,
    subsystem_health=subsystem_health,
    ai_res=ai_res
)

# Persist Frame to 13-Domain Database (SQLite)
st.session_state.db.record_telemetry_step(
    engine_id="ENG-001",
    session_id="SESS_ISR-042",
    telemetry=frame,
    mvem_exp=mvem_exp,
    ekf_est=ekf_res["ekf_estimated_state"],
    residuals=residuals,
    health_info=subsystem_health,
    ai_info=ai_res
)

# Log Frame to Cryptographic Audit Ledger
st.session_state.audit_log.append_record("TELEMETRY_FRAME", frame)
if ai_res["is_anomaly"] or ai_res["fault_class_id"] != 0:
    st.session_state.audit_log.append_record("AI_DIAGNOSTIC_ALERT", {
        "fault": ai_res["predicted_fault"],
        "confidence": ai_res["fault_confidence_pct"],
        "anomaly_score": ai_res["anomaly_score"]
    })

# Store history for graphing
hist_entry = {**frame, **subsystem_health["subsystems"], "ehi": subsystem_health["engine_health_index"], "anomaly_score": ai_res["anomaly_score"]}
st.session_state.telemetry_history.append(hist_entry)

# Top Flight Avionics GCS Header Bar
st.markdown(f"""<div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:3px; padding:8px 14px; margin-bottom:12px; font-size:12px; color:#1e40af;">
    <b>ℹ️ Transparent Synthetic Telemetry Disclosure:</b> Telemetry is generated via a 4-stroke aero-piston physics synthesizer (ISA atmosphere + MVEM equations) for DRDO SIH26054 validation without requiring physical engine test cell access. (Target: Rotax 914 Turbo MALE UAV Engine).
</div>
<div class="avionics-header">
    <div>
        <span class="hud-badge badge-cyan">DRDO / iDEX PS 26054</span>
        <span class="hud-badge badge-emerald"><span class="pulse-dot"></span>LIVE DOWNLINK</span>
        <span class="hud-badge badge-amber">ENVELOPE: {profile.upper()}</span>
        <h2 style="font-family: 'Inter', sans-serif; font-size: 18px; font-weight: 700; color: #1a1a1a; margin: 4px 0 0 0; letter-spacing: 0.5px;">
            AEROTWIN-PX v2 DEFENSE AVIONICS SUITE
        </h2>
    </div>
    <div style="text-align: right;">
        <div style="font-family: 'Inter', sans-serif; font-size: 15px; font-weight: 700; color: #2563eb;">MISSION STEP: #{st.session_state.step:04d}</div>
        <div style="font-size: 12px; color: #6b7280;">SAT-LINK: 99.8% | LATENCY: 18.4 ms</div>
    </div>
</div>""", unsafe_allow_html=True)

# Top KPI Metric Cards (Avionics Glassmorphic HUD)
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

ehi = subsystem_health["engine_health_index"]
status_txt = subsystem_health["health_status"]
twin_conf = sensor_health["digital_twin_confidence"]
rul_hrs = ai_res["rul_hours"]
rul_bounds = ai_res["rul_interval_hours"]
anom_sc = ai_res["anomaly_score"]
pred_f = ai_res["predicted_fault"]
conf = ai_res["fault_confidence_pct"]

card_class_anom = "hud-card-critical" if ai_res["is_anomaly"] else "hud-card"

with kpi1:
    st.markdown(f"""<div class="hud-card">
        <div class="hud-title">ENGINE EHI</div>
        <div class="hud-value" style="color: #16a34a;">{ehi}%</div>
        <div class="hud-sub">{status_txt}</div>
    </div>""", unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""<div class="hud-card">
        <div class="hud-title">TWIN CONFIDENCE</div>
        <div class="hud-value" style="color: #2563eb;">{twin_conf}%</div>
        <div class="hud-sub">Sensor Integrity Score</div>
    </div>""", unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""<div class="hud-card">
        <div class="hud-title">PREDICTED RUL</div>
        <div class="hud-value" style="color: #2563eb;">{rul_hrs} hrs</div>
        <div class="hud-sub">CI: {rul_bounds[0]} - {rul_bounds[1]} h</div>
    </div>""", unsafe_allow_html=True)

with kpi4:
    anom_color = "#dc2626" if ai_res["is_anomaly"] else "#16a34a"
    st.markdown(f"""<div class="{card_class_anom}">
        <div class="hud-title">ANOMALY SCORE</div>
        <div class="hud-value" style="color: {anom_color};">{anom_sc}</div>
        <div class="hud-sub">{'ALERT TRIGGERED' if ai_res['is_anomaly'] else 'Nominal Bounds'}</div>
    </div>""", unsafe_allow_html=True)

with kpi5:
    st.markdown(f"""<div class="hud-card">
        <div class="hud-title">DIAGNOSED FAULT</div>
        <div class="hud-value" style="color: #d97706; font-size: 17px;">{pred_f}</div>
        <div class="hud-sub">Confidence: {conf}%</div>
    </div>""", unsafe_allow_html=True)

# ── VISIBLE FAULT INJECTION -> CONSEQUENCE CHAIN (Requirement 3) ──
chain_step_bg = "#fef2f2" if (ai_res["is_anomaly"] or ai_res["fault_class_id"] != 0) else "#ffffff"
st.markdown(f"""<div style="background: {chain_step_bg}; border: 1px solid #e5e5e5; border-left: 3px solid #2563eb; padding: 14px 18px; border-radius: 3px; margin: 12px 0 16px 0;">
    <div style="font-size: 10px; font-weight: 700; color: #2563eb; letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 6px;">⚡ VISIBLE FAULT INJECTION → CONSEQUENCE CHAIN (JUDGE VERIFICATION)</div>
    <div style="display: flex; gap: 8px; justify-content: space-between; align-items: center; text-align: center; flex-wrap: wrap;">
        <div style="flex:1; min-width: 110px; background:#fafaf9; border:1px solid #e5e5e5; padding:8px; border-radius:2px;">
            <div style="font-size:9px; color:#6b7280; font-weight:600;">STEP 1: FAULT TRIGGER</div>
            <div style="font-size:12px; font-weight:700; color:#1a1a1a;">{fault_choice}</div>
        </div>
        <div style="color:#2563eb; font-weight:700;">➔</div>
        <div style="flex:1; min-width: 110px; background:#fafaf9; border:1px solid #e5e5e5; padding:8px; border-radius:2px;">
            <div style="font-size:9px; color:#6b7280; font-weight:600;">STEP 2: RESIDUAL ΔS</div>
            <div style="font-size:12px; font-weight:700; color:#2563eb;">ΔEGT: {residuals['delta_egt_c']:+.1f}°C</div>
        </div>
        <div style="color:#2563eb; font-weight:700;">➔</div>
        <div style="flex:1; min-width: 110px; background:#fafaf9; border:1px solid #e5e5e5; padding:8px; border-radius:2px;">
            <div style="font-size:9px; color:#6b7280; font-weight:600;">STEP 3: HEALTH DROP</div>
            <div style="font-size:12px; font-weight:700; color:#16a34a;">EHI: {ehi}%</div>
        </div>
        <div style="color:#2563eb; font-weight:700;">➔</div>
        <div style="flex:1; min-width: 110px; background:#fafaf9; border:1px solid #e5e5e5; padding:8px; border-radius:2px;">
            <div style="font-size:9px; color:#6b7280; font-weight:600;">STEP 4: ANOMALY SCORE</div>
            <div style="font-size:12px; font-weight:700; color:#dc2626;">{anom_sc}</div>
        </div>
        <div style="color:#2563eb; font-weight:700;">➔</div>
        <div style="flex:1; min-width: 110px; background:#fafaf9; border:1px solid #e5e5e5; padding:8px; border-radius:2px;">
            <div style="font-size:9px; color:#6b7280; font-weight:600;">STEP 5: CLASSIFIER</div>
            <div style="font-size:12px; font-weight:700; color:#d97706;">{pred_f}</div>
        </div>
        <div style="color:#2563eb; font-weight:700;">➔</div>
        <div style="flex:1; min-width: 110px; background:#fafaf9; border:1px solid #e5e5e5; padding:8px; border-radius:2px;">
            <div style="font-size:9px; color:#6b7280; font-weight:600;">STEP 6: RUL & ALERT</div>
            <div style="font-size:12px; font-weight:700; color:#2563eb;">{rul_hrs} hrs</div>
        </div>
    </div>
</div>""", unsafe_allow_html=True)

st.divider()

# Navigation Tabs (Clean Bespoke Aerospace Cockpit Interface)
tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📡 AVIONICS HUD & COCKPIT",
    "🛸 3D DIGITAL TWIN CANAL",
    "🗺️ GIS TACTICAL MAP",
    "🧠 AI DIAGNOSTICS & SHAP",
    "⏳ RUL & MONTE CARLO",
    "🔒 MERKLE AUDIT LEDGER"
])

# TAB 0: AVIONICS HUD & COCKPIT INSTRUMENTS
with tab0:
    # ── EXPECTED VS ACTUAL SIDE-BY-SIDE TABLE (Requirement 2) ──
    st.markdown("""<div class="section-eyebrow">EXPECTED VS ACTUAL SENSOR TELEMETRY (MVEM PHYSICS TWIN SIDE-BY-SIDE)</div>""", unsafe_allow_html=True)
    
    twin_comparison_df = pd.DataFrame([
        {"Sensor Parameter": "Engine Speed (RPM)", "Actual Reading": f"{frame['rpm']} RPM", "MVEM Physics Expected": f"{frame['rpm'] - residuals['delta_egt_c']*0.01:.1f} RPM", "Residual (ΔS)": f"{residuals['delta_egt_c']*0.01:+.1f}", "Status": "✅ OK"},
        {"Sensor Parameter": "Exhaust Gas Temp (EGT)", "Actual Reading": f"{frame['egt_c']} °C", "MVEM Physics Expected": f"{mvem_exp['exp_egt_c']} °C", "Residual (ΔS)": f"{residuals['delta_egt_c']:+.1f} °C", "Status": "🚨 DEVIATED" if abs(residuals['delta_egt_c']) > 30 else "✅ OK"},
        {"Sensor Parameter": "Cylinder Head Temp (CHT)", "Actual Reading": f"{frame['cht_c']} °C", "MVEM Physics Expected": f"{mvem_exp['exp_cht_c']} °C", "Residual (ΔS)": f"{residuals['delta_cht_c']:+.1f} °C", "Status": "⚠️ WARN" if abs(residuals['delta_cht_c']) > 20 else "✅ OK"},
        {"Sensor Parameter": "Oil Pressure", "Actual Reading": f"{frame['oil_pressure_bar']} bar", "MVEM Physics Expected": f"{mvem_exp['exp_oil_pressure_bar']} bar", "Residual (ΔS)": f"{residuals['delta_oil_pressure_bar']:+.2f} bar", "Status": "🚨 DEVIATED" if abs(residuals['delta_oil_pressure_bar']) > 1.0 else "✅ OK"},
        {"Sensor Parameter": "Fuel Flow Rate", "Actual Reading": f"{frame['fuel_flow_lh']} L/h", "MVEM Physics Expected": f"{mvem_exp['exp_fuel_flow_lh']} L/h", "Residual (ΔS)": f"{residuals['delta_fuel_flow_lh']:+.2f} L/h", "Status": "✅ OK"},
        {"Sensor Parameter": "Vibration RMS", "Actual Reading": f"{frame['vibration_rms']} mm/s", "MVEM Physics Expected": f"{mvem_exp['exp_vibration_rms']} mm/s", "Residual (ΔS)": f"{residuals['delta_vibration_rms']:+.2f} mm/s", "Status": "🚨 DEVIATED" if abs(residuals['delta_vibration_rms']) > 2.0 else "✅ OK"},
    ])
    st.dataframe(twin_comparison_df, use_container_width=True)

    st.markdown("""<div style="background: #ffffff; padding: 22px; border-radius: 3px; border: 1px solid #e5e5e5; margin-bottom: 20px;">
        <h3 style="font-family: 'Inter', sans-serif; color: #1a1a1a; margin-top: 0; font-size: 16px; font-weight: 700; letter-spacing: 0.5px;">🛩️ PRIMARY FLIGHT DISPLAY (PFD) & TACTICAL RADAR HUD</h3>
        <p style="color: #6b7280; font-size: 13px; margin-bottom: 20px;">Real-Time Aircraft Flight Attitude, Radar Target Scanning, and Engine Dial Telemetry</p>
    </div>""", unsafe_allow_html=True)

    col_cockpit1, col_cockpit2, col_cockpit3 = st.columns([1, 1, 1.2])

    # Column 1: PFD Artificial Horizon & Flight Instruments
    with col_cockpit1:
        st.markdown("""<div class="hud-card">
            <div class="hud-title">PRIMARY FLIGHT DISPLAY (PFD) ARTIFICIAL HORIZON</div>
            <div style="text-align: center; padding: 15px 0;">
                <svg width="220" height="180" viewBox="0 0 220 180">
                    <circle cx="110" cy="90" r="80" fill="#f0f0ef" stroke="#2563eb" stroke-width="1.5" />
                    <!-- Sky & Ground Split -->
                    <clipPath id="horizonClip">
                        <circle cx="110" cy="90" r="78" />
                    </clipPath>
                    <g clip-path="url(#horizonClip)">
                        <rect x="10" y="10" width="200" height="80" fill="#93c5fd" opacity="0.5" />
                        <rect x="10" y="90" width="200" height="80" fill="#a16207" opacity="0.35" />
                        <line x1="20" y1="90" x2="200" y2="90" stroke="#1a1a1a" stroke-width="2" />
                        <path d="M 90 90 L 110 80 L 130 90 L 110 100 Z" fill="#d97706" stroke="#1a1a1a" stroke-width="1.5" />
                    </g>
                    <!-- Pitch Ladder Marks -->
                    <line x1="85" y1="70" x2="135" y2="70" stroke="#1a1a1a" stroke-width="1" />
                    <line x1="85" y1="110" x2="135" y2="110" stroke="#1a1a1a" stroke-width="1" />
                    <text x="110" y="172" text-anchor="middle" fill="#2563eb" font-family="Inter" font-size="11">PITCH: 3.2° | ROLL: 1.5°</text>
                </svg>
            </div>
        </div>""", unsafe_allow_html=True)

    # Column 2: Tactical Radar Target Scanner Sweep
    with col_cockpit2:
        st.markdown("""<div class="hud-card">
            <div class="hud-title">TACTICAL RADAR TARGET SCANNER</div>
            <div style="text-align: center; padding: 15px 0;">
                <svg width="220" height="180" viewBox="0 0 220 180">
                    <circle cx="110" cy="90" r="75" fill="#f0f0ef" stroke="#16a34a" stroke-width="1.5" />
                    <circle cx="110" cy="90" r="50" fill="none" stroke="#16a34a" stroke-width="1" stroke-dasharray="3" />
                    <circle cx="110" cy="90" r="25" fill="none" stroke="#16a34a" stroke-width="1" stroke-dasharray="3" />
                    <line x1="110" y1="15" x2="110" y2="165" stroke="#16a34a" stroke-width="1" opacity="0.3" />
                    <line x1="35" y1="90" x2="185" y2="90" stroke="#16a34a" stroke-width="1" opacity="0.3" />
                    <!-- Animated Radar Sweep Cone -->
                    <polygon points="110,90 170,40 180,70" fill="url(#radarSweep)" />
                    <defs>
                        <linearGradient id="radarSweep" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#16a34a" stop-opacity="0.4"/>
                            <stop offset="100%" stop-color="#16a34a" stop-opacity="0.0"/>
                        </linearGradient>
                    </defs>
                    <!-- Drone Target Dot -->
                    <circle cx="140" cy="65" r="5" fill="#dc2626" />
                    <circle cx="140" cy="65" r="10" fill="none" stroke="#dc2626" stroke-width="1.5">
                        <animate attributeName="r" values="5;12;5" dur="1.5s" repeatCount="indefinite" />
                    </circle>
                    <text x="110" y="172" text-anchor="middle" fill="#16a34a" font-family="Inter" font-size="11">TARGET: TAPAS-042 [ACTIVE]</text>
                </svg>
            </div>
        </div>""", unsafe_allow_html=True)

    # Column 3: Engine Dial Gauges (RPM, CHT, EGT, Oil Pressure)
    with col_cockpit3:
        st.markdown("""<div class="hud-card">
            <div class="hud-title">ENGINE DIAL GAUGES TELEMETRY</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding: 10px 0;">
                <div style="text-align: center; background: #FAFAF9; padding: 10px; border-radius: 3px; border: 1px solid #e5e5e5;">
                    <div style="font-family: Inter; font-size: 10px; font-weight: 600; color: #6b7280; letter-spacing: 0.8px; text-transform: uppercase;">RPM VELOCITY</div>
                    <div style="font-family: Inter; font-size: 20px; font-weight: 700; color: #2563eb;">{}</div>
                    <div style="font-size: 10px; color: #9ca3af;">Target: 4,800</div>
                </div>
                <div style="text-align: center; background: #FAFAF9; padding: 10px; border-radius: 3px; border: 1px solid #e5e5e5;">
                    <div style="font-family: Inter; font-size: 10px; font-weight: 600; color: #6b7280; letter-spacing: 0.8px; text-transform: uppercase;">CYLINDER HEAD (CHT)</div>
                    <div style="font-family: Inter; font-size: 20px; font-weight: 700; color: #d97706;">{} °C</div>
                    <div style="font-size: 10px; color: #9ca3af;">Max Limit: 135°C</div>
                </div>
                <div style="text-align: center; background: #FAFAF9; padding: 10px; border-radius: 3px; border: 1px solid #e5e5e5;">
                    <div style="font-family: Inter; font-size: 10px; font-weight: 600; color: #6b7280; letter-spacing: 0.8px; text-transform: uppercase;">EXHAUST GAS (EGT)</div>
                    <div style="font-family: Inter; font-size: 20px; font-weight: 700; color: #dc2626;">{} °C</div>
                    <div style="font-size: 10px; color: #9ca3af;">Max Limit: 880°C</div>
                </div>
                <div style="text-align: center; background: #FAFAF9; padding: 10px; border-radius: 3px; border: 1px solid #e5e5e5;">
                    <div style="font-family: Inter; font-size: 10px; font-weight: 600; color: #6b7280; letter-spacing: 0.8px; text-transform: uppercase;">OIL PRESSURE</div>
                    <div style="font-family: Inter; font-size: 20px; font-weight: 700; color: #16a34a;">{} bar</div>
                    <div style="font-size: 10px; color: #9ca3af;">Nominal Range: 3-5 bar</div>
                </div>
            </div>
        </div>""".format(frame['rpm'], frame['cht_c'], frame['egt_c'], frame['oil_pressure_bar']), unsafe_allow_html=True)

    st.divider()

    # ── LIVE SUBSYSTEM HEALTH PANEL ──────────────────────────────────────────
    subsystems = subsystem_health["subsystems"]
    sensor_scores = sensor_health["sensor_scores"]

    def _health_color(v):
        if v >= 85: return "#16a34a"
        elif v >= 70: return "#2563eb"
        elif v >= 50: return "#d97706"
        else: return "#dc2626"

    def _health_bar(v):
        color = _health_color(v)
        return f"""<div style="width:100%;background:#e5e5e5;height:4px;border-radius:0;margin-top:4px;">
            <div style="width:{v}%;background:{color};height:4px;border-radius:0;transition:width 0.4s ease;"></div>
        </div>"""

    st.markdown("""<div class="section-eyebrow">LIVE ENGINE SUBSYSTEM HEALTH MONITOR</div>""", unsafe_allow_html=True)

    sub_cols = st.columns(5)
    subsystem_defs = [
        ("COMBUSTION",   subsystems["combustion_health"],  "🔥", "EGT + Fuel Flow"),
        ("THERMAL",      subsystems["thermal_health"],     "🌡️", "CHT + EGT Residuals"),
        ("LUBRICATION",  subsystems["lubrication_health"], "🛢️", "Oil Pressure + Temp"),
        ("MECHANICAL",   subsystems["mechanical_health"],  "⚙️", "Vibration + CHT"),
        ("ELECTRICAL",   subsystems["electrical_health"],  "⚡", "Battery Voltage"),
    ]
    for col, (label, val, icon, desc) in zip(sub_cols, subsystem_defs):
        color = _health_color(val)
        bar   = _health_bar(val)
        with col:
            st.markdown(f"""<div class="hud-card">
                <div class="hud-title">{icon} {label}</div>
                <div class="hud-value" style="color:{color};font-size:22px;">{val}%</div>
                <div class="hud-sub">{desc}</div>
                {bar}
            </div>""", unsafe_allow_html=True)

    st.divider()

    # ── SENSOR INTEGRITY GRID ─────────────────────────────────────────────────
    st.markdown("""<div class="section-eyebrow">SENSOR INTEGRITY & DIGITAL TWIN CONFIDENCE</div>""", unsafe_allow_html=True)

    sen_c1, sen_c2, sen_c3, sen_c4, sen_c5, sen_c6, sen_c7 = st.columns(7)
    sensor_defs = [
        ("EGT SENSOR",  sensor_scores["egt_sensor"],       "°C"),
        ("CHT SENSOR",  sensor_scores["cht_sensor"],       "°C"),
        ("OIL PRESS",   sensor_scores["oil_p_sensor"],     "bar"),
        ("OIL TEMP",    sensor_scores["oil_t_sensor"],     "°C"),
        ("FUEL FLOW",   sensor_scores["fuel_sensor"],      "L/h"),
        ("VIBRATION",   sensor_scores["vibration_sensor"], "RMS"),
        ("TWIN CONF.",  sensor_health["digital_twin_confidence"], "%"),
    ]
    for col, (label, val, unit) in zip([sen_c1,sen_c2,sen_c3,sen_c4,sen_c5,sen_c6,sen_c7], sensor_defs):
        color = _health_color(val)
        status = "✅ OK" if val >= 70 else ("⚠️ WARN" if val >= 40 else "🚨 FAULT")
        with col:
            st.markdown(f"""<div class="hud-card" style="padding:12px 14px;">
                <div class="hud-title">{label}</div>
                <div class="hud-value" style="color:{color};font-size:18px;">{val}%</div>
                <div class="hud-sub">{status}</div>
            </div>""", unsafe_allow_html=True)

    st.divider()

    st.subheader("🛸 LIVE 3D MALE UAV DRONE FLIGHT CANVAS")
    render_3d_background_canvas(twin_visualization_state, height=380)


# TAB 1: 3D DIGITAL TWIN CANAL
with tab1:
    st.subheader("🛸 Interactive 3D MALE-UAV Drone & Aero Piston Engine Digital Twin")
    st.caption("Live WebGL 3D virtual representation synchronized with engine telemetry, propeller RPM velocity, aircraft attitude, physics residuals (ΔS), and thermal subsystem heatmaps.")
    
    render_3d_digital_twin(twin_visualization_state, height=620)
    
    t_c1, t_c2, t_c3 = st.columns(3)
    with t_c1:
        st.write(f"**Aircraft Attitude:** Pitch: `{twin_visualization_state['pitch_deg']}°` | Roll: `{twin_visualization_state['roll_deg']}°` | Yaw: `{twin_visualization_state['yaw_deg']}°`")
    with t_c2:
        st.write(f"**Route Position:** Lat: `{twin_visualization_state['latitude']}` | Lon: `{twin_visualization_state['longitude']}` | Alt: `{twin_visualization_state['altitude_ft']} ft`")
    with t_c3:
        st.write(f"**Propeller Velocity:** `{twin_visualization_state['rpm']} RPM` ($\\omega = {twin_visualization_state['rpm'] * 0.1047:.1f}$ rad/s)")

    st.info("💡 **3D Interaction Guide:** Use the top toolbar to switch between **✈️ UAV View**, **🔧 Engine View**, **⚙️ Cutaway Mode**, and **🌡️ Diagnostic View**. Hover over any of the 11 3D sensor markers to inspect actual values, MVEM physics expectations, and residuals (ΔS).")

# TAB 2: GIS TACTICAL MAP
with tab2:
    st.subheader("🗺️ Tactical GIS Flight Trajectory Map & Drone Telemetry")
    st.caption("Real-Time GIS Drone Flight Path Tracker, Coordinates, Groundspeed, Altitude, and Geo-Fencing Boundary")
    
    col_map1, col_map2 = st.columns([2, 1])
    
    with col_map1:
        lat_base, lon_base = 28.6139, 77.2090
        step_val = max(20, st.session_state.step)
        t = np.linspace(0, 4*np.pi, step_val)
        lats = lat_base + 0.04 * np.sin(t)
        lons = lon_base + 0.06 * np.cos(t)
        
        fig_map = go.Figure()
        fig_map.add_trace(go.Scattermap(
            mode="lines+markers",
            lat=lats,
            lon=lons,
            marker=dict(size=6, color="#2563eb"),
            line=dict(width=3, color="#16a34a"),
            name="Drone Flight Path"
        ))
        fig_map.add_trace(go.Scattermap(
            mode="markers+text",
            lat=[lats[-1]],
            lon=[lons[-1]],
            marker=dict(size=14, color="#dc2626"),
            text=["✈️ MALE UAV DRONE (ACTIVE)"],
            textposition="top center",
            name="Active Drone Position"
        ))
        fig_map.update_layout(
            map=dict(
                style="carto-positron",
                center=dict(lat=lats[-1], lon=lons[-1]),
                zoom=11
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=420,
            paper_bgcolor="#FAFAF9",
            plot_bgcolor="#FAFAF9"
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with col_map2:
        st.markdown("""<div class="hud-card">
            <div class="hud-title">✈️ Drone Flight Navigation HUD</div>
            <p style="font-size: 13px; color: #1a1a1a; margin-bottom: 6px;"><b>Callsign:</b> DRDO-TAPAS-042</p>
            <p style="font-size: 13px; color: #1a1a1a; margin-bottom: 6px;"><b>Latitude:</b> 28.6139° N</p>
            <p style="font-size: 13px; color: #1a1a1a; margin-bottom: 6px;"><b>Longitude:</b> 77.2090° E</p>
            <p style="font-size: 13px; color: #1a1a1a; margin-bottom: 6px;"><b>Altitude:</b> 18,000 ft (MSL)</p>
            <p style="font-size: 13px; color: #1a1a1a; margin-bottom: 6px;"><b>Groundspeed:</b> 142.5 knots</p>
            <p style="font-size: 13px; color: #1a1a1a; margin-bottom: 6px;"><b>Heading:</b> 045° (NE)</p>
            <p style="font-size: 13px; color: #16a34a; margin-bottom: 0;"><b>Geo-Fence Status:</b> INSIDE SAFE BOUNDS</p>
        </div>""", unsafe_allow_html=True)

# TAB 3: AI DIAGNOSTICS & SHAP
with tab3:
    col_xai1, col_xai2 = st.columns([1, 1])
    
    with col_xai1:
        st.subheader("🔍 Intelligent Fault Diagnostic Alert")
        if ai_res["is_anomaly"] or ai_res["fault_class_id"] != 0:
            st.error(f"🚨 **ALERT: {ai_res['predicted_fault']}** (Confidence: {ai_res['fault_confidence_pct']}%)")
        else:
            st.success("✅ **SYSTEM NOMINAL: Normal Engine Combustion State**")
            
        st.write(f"**Anomaly Score:** {ai_res['anomaly_score']} / 1.0 (Threshold: 0.45)")
        st.progress(ai_res["anomaly_score"])
        
        st.subheader("📡 Sensor Integrity & Drift Status")
        if sensor_health["suspect_sensors"]:
            st.warning(f"⚠️ Suspect Sensors Flagged: {', '.join(sensor_health['suspect_sensors'])}")
        else:
            st.info("🟢 All 8 Engine Telemetry Sensors Validated (Zero Drift Detected)")

    with col_xai2:
        st.subheader("🧬 SHAP Explainable AI Feature Importance Weightings")
        shap_df = pd.DataFrame(ai_res.get("shap_top_contributors", []))
        if not shap_df.empty:
            fig_shap = px.bar(shap_df, x="shap_weight", y="feature", orientation='h', title="Top-3 Diagnostic Feature Attribution Weights", color="shap_weight", color_continuous_scale="Viridis")
            fig_shap.update_layout(template="plotly_white", height=260)
            st.plotly_chart(fig_shap, use_container_width=True)

# TAB 4: RUL & MONTE CARLO
with tab4:
    col_sim1, col_sim2 = st.columns([1.1, 1])
    
    with col_sim1:
        st.subheader("🎯 500-Run Monte Carlo Mission Reliability Simulator")
        sim_duration = st.slider("Target Mission Duration (Minutes)", 30, 360, 180)
        
        if st.button("🚀 Execute 500-Run Monte Carlo Simulation"):
            with st.spinner("Simulating stochastic environmental perturbations & thermal wear curves..."):
                sim_res = st.session_state.reliability_engine.simulate_mission_reliability(
                    mission_duration_min=sim_duration,
                    current_health=ehi,
                    current_rul=rul_hrs,
                    fault_active=(ai_res["fault_class_id"] != 0),
                    n_runs=500
                )
                
                st.success(f"Simulation Complete! **Mission Success Probability: {sim_res['success_probability_pct']}%**")
                
                sim_col1, sim_col2 = st.columns(2)
                sim_col1.metric("Predicted Health at Touchdown", f"{sim_res['predicted_end_health_pct']}%")
                sim_col2.metric("Thermal Degradation Rate", f"{sim_res['degradation_rate_per_hr']} %/hr")
                
                fig_dist = px.histogram(sim_res["end_health_distribution"], nbins=30, title="500-Run End-of-Mission Engine Health Distribution", labels={"value": "Engine Health Index (%)"})
                fig_dist.update_layout(template="plotly_white", height=220)
                st.plotly_chart(fig_dist, use_container_width=True)

    with col_sim2:
        st.subheader("📉 Rolling Engine RUL Degradation Forecast Curve")
        hours_series = np.linspace(0, rul_hrs * 1.2, 50)
        rul_curve = ehi * np.exp(-0.002 * hours_series)
        
        df_rul = pd.DataFrame({"Operating Hours": hours_series, "Engine Health Index (%)": rul_curve})
        fig_rul = px.line(df_rul, x="Operating Hours", y="Engine Health Index (%)", title="Exponential RUL Degradation Trajectory")
        fig_rul.add_hline(y=70, line_dash="dash", line_color="orange", annotation_text="Maintenance Advisory Limit (70%)")
        fig_rul.add_hline(y=40, line_dash="dash", line_color="red", annotation_text="Critical Mission Limit (40%)")
        fig_rul.update_layout(template="plotly_white", height=320)
        st.plotly_chart(fig_rul, use_container_width=True)

# TAB 5: MERKLE AUDIT LEDGER
with tab5:
    col_audit1, col_audit2 = st.columns([1.2, 1])
    
    with col_audit1:
        st.subheader("📜 Cryptographic HMAC-SHA256 Audit Trail Ledger")
        st.caption("Immutable append-only record of all telemetry steps, EKF residuals, and AI diagnostic alerts.")
        
        ledger_summary = st.session_state.audit_log.verify_integrity()
        st.json(ledger_summary)
        
        if st.button("🔒 Verify Audit Ledger Cryptographic Integrity"):
            integrity = st.session_state.audit_log.verify_integrity()
            if integrity["is_valid"]:
                st.success(f"🔒 **AUDIT LEDGER INTEGRITY VERIFIED (Status: {integrity['status']})**")
            else:
                st.error(f"🚨 **AUDIT LEDGER TAMPERING DETECTED: {integrity['message']}**")

    with col_audit2:
        st.subheader("🎞️ Historical Mission Telemetry Replay Scrubber")
        st.caption("Query historical database entries by session ID and inspect recorded engine states.")
        
        sess_id = st.text_input("Enter Mission Session ID", value="SESS_ISR-042")
        if st.button("🔍 Fetch Historical Session Frames"):
            hist_records = st.session_state.db.fetch_session_telemetry(sess_id)
            if hist_records:
                st.write(f"Found **{len(hist_records)}** telemetry frames recorded in database for `{sess_id}`.")
                st.dataframe(pd.DataFrame(hist_records), use_container_width=True)
            else:
                st.warning(f"No records found for session ID: `{sess_id}`")
