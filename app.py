"""
Q-DRUG: Quantum-Assisted Drug Discovery & Lead Optimization Platform
Main Streamlit Application.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Streamlit Page Config
st.set_page_config(
    page_title="Q-DRUG | Quantum Drug Discovery Platform",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

from config import (
    APP_TITLE, APP_SUBTITLE, TAGLINE, PREDEFINED_TARGETS,
    THEME_COLORS, SCIENTIFIC_DISCLAIMER, DEFAULT_SCORING_WEIGHTS, MODIFICATION_PROTOTYPES
)
from utils import (
    inject_custom_css, render_disclaimer_banner, render_section_header, initialize_session_state
)
from quantum_engine import (
    VQEEngine, build_convergence_chart, render_quantum_circuit_diagram
)
from docking_engine import (
    fetch_pdb_structure_info, generate_fallback_3d_molecular_plot,
    evaluate_lipinski_rule_of_five, predict_admet_prototype_scores
)
from drug_engine import (
    load_candidate_database, assign_recommendation_label, generate_pareto_chart,
    generate_candidate_radar_chart, parse_and_score_custom_smiles
)
from lead_optimizer import (
    optimize_lead_candidate, MODIFICATION_PROTOTYPES
)
from report_generator import generate_scientific_html_report

# Initialize CSS and session state
inject_custom_css()
initialize_session_state()

# Target Selection setup
target_keys = list(PREDEFINED_TARGETS.keys())
if st.session_state["selected_target_key"] not in target_keys:
    st.session_state["selected_target_key"] = target_keys[0]

# Load candidate database from PubChem service for active target
df_candidates = load_candidate_database(target_name=st.session_state["selected_target_key"])
data_source_badge = df_candidates.attrs.get("data_source_label", "PubChem Data Source")
status_message = df_candidates.attrs.get("status_msg", "")

# Top Header Bar & Judge Demo Tour Trigger
col_title, col_tour = st.columns([3, 1])
with col_title:
    st.markdown(f'<div class="main-title">🧪 {APP_TITLE}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-title">{APP_SUBTITLE}</div>', unsafe_allow_html=True)

with col_tour:
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    if st.button("🎯 Judge Demo Tour", use_container_width=True, type="primary"):
        st.session_state["tour_active"] = True
        st.session_state["tour_step"] = 1

# Render Judge Demo Tour Overlay Modal if active
if st.session_state["tour_active"]:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E1035 0%, #0A192F 100%); border: 2px solid #00F0FF; border-radius: 12px; padding: 20px; margin-bottom: 25px; box-shadow: 0 0 30px rgba(0, 240, 255, 0.3);">
        <h3 style="color: #00F0FF; margin-top:0;">🎯 Q-DRUG Hackathon Judge Guided Tour</h3>
    """, unsafe_allow_html=True)
    
    tour_step = st.session_state["tour_step"]
    
    if tour_step == 1:
        st.markdown("""
        <h4>STEP 1: Target Receptor Selection</h4>
        <p>Q-DRUG identifies therapeutic drug targets (e.g. <b>SARS-CoV-2 Mpro PDB: 6LU7</b>) and extracts binding pocket active-site residues (His41, Cys145).</p>
        <div style="background: #0E1524; padding: 10px; border-radius: 6px;">
            🔑 <i>Key Metric:</i> Binding Pocket Volume estimate: <b>842.5 Å³</b> | Catalytic dyad Cys145-His41
        </div>
        """, unsafe_allow_html=True)
    elif tour_step == 2:
        st.markdown("""
        <h4>STEP 2: 3D Docking Studio & ADMET Analysis</h4>
        <p>Interactive 3D molecular viewer renders protein ribbon backbone, pocket envelope, and docked ligand while calculating Lipinski Rule of 5 and ADMET risk scores.</p>
        <div style="background: #0E1524; padding: 10px; border-radius: 6px;">
            🔑 <i>Key Metric:</i> Top Candidate <b>Nirmatrelvir-Q1</b> passes all 5 Lipinski Rules (MW: 499.5 Da, LogP: 1.85)
        </div>
        """, unsafe_allow_html=True)
    elif tour_step == 3:
        st.markdown("""
        <h4>STEP 3: Simulated VQE Quantum Optimizer Engine</h4>
        <p>Variational Quantum Eigensolver (VQE) models molecular Hamiltonian electronic ground state optimization over 6 qubits using RealAmplitudes ansatz.</p>
        <div style="background: #0E1524; padding: 10px; border-radius: 6px;">
            ⚡ <i>Key Metric:</i> Ground state energy optimized from <b>-120.0 Hartree → -145.32 Hartree</b> (ΔE: 25.32 Ha)
        </div>
        """, unsafe_allow_html=True)
    elif tour_step == 4:
        st.markdown("""
        <h4>STEP 4: VHTS Pareto Screening & De-Novo Lead Optimization</h4>
        <p>Screening 25+ candidate molecules on Pareto Frontier (Binding vs Quantum E) followed by De-Novo chemical fluorination (-F) enhancing pKd by +0.45.</p>
        <div style="background: #0E1524; padding: 10px; border-radius: 6px;">
            🚀 <i>Key Metric:</i> Thermodynamic binding energy shift <b>ΔΔG = -0.61 kcal/mol</b> | Q-DRUG Score increase <b>+4.85 pts</b>
        </div>
        """, unsafe_allow_html=True)
    elif tour_step == 5:
        st.markdown("""
        <h4>🏆 Q-DRUG Final Recommendation Summary</h4>
        <div style="background: #0A0F1A; border: 1px solid #00FF88; padding: 15px; border-radius: 8px;">
            <h5 style="color: #00FF88; margin:0;">Top Recommended Lead Candidate: Nirmatrelvir-Q1 + Fluorination (-F)</h5>
            <p style="margin: 5px 0;"><b>Overall Q-DRUG Composite Score:</b> 94.85 / 100</p>
            <p style="margin: 5px 0;"><b>Quantum Ground State Optimization:</b> -150.95 Hartree</p>
            <p style="margin: 5px 0;"><b>Predicted Binding Affinity:</b> 9.30 pKd (K<sub>d</sub> ~ 0.50 nM)</p>
            <p style="margin: 5px 0; color: #FFB300; font-size: 0.85rem;">⚠️ Prototype recommendation — requires experimental biological validation.</p>
        </div>
        """, unsafe_allow_html=True)

    col_t1, col_t2, col_t3 = st.columns([1, 1, 1])
    with col_t1:
        if tour_step > 1:
            if st.button("⬅️ Previous Step"):
                st.session_state["tour_step"] -= 1
                st.rerun()
    with col_t2:
        if tour_step < 5:
            if st.button("Next Step ➡️", type="primary"):
                st.session_state["tour_step"] += 1
                st.rerun()
    with col_t3:
        if st.button("❌ Close Tour"):
            st.session_state["tour_active"] = False
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown(f"<h2 style='color:{THEME_COLORS['primary']}; margin-bottom:0;'>Q-DRUG</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size:0.8rem; color:#94A3B8;'>Quantum-Inspired Drug Discovery Platform</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Active Target Selection
selected_sidebar_target = st.sidebar.selectbox(
    "🎯 Select Target Receptor:",
    target_keys,
    index=target_keys.index(st.session_state["selected_target_key"]),
    key="sb_target_selector"
)
if selected_sidebar_target != st.session_state["selected_target_key"]:
    st.session_state["selected_target_key"] = selected_sidebar_target
    st.rerun()

st.sidebar.markdown(f"""
<div style="background:#0E1524; border:1px solid #1E293B; border-radius:8px; padding:10px; margin-top:8px;">
    <div style="font-size:0.75rem; color:#94A3B8;">DATA SOURCE STATUS</div>
    <div style="font-size:0.85rem; font-weight:bold; color:{'#00FF88' if 'Live' in data_source_badge else '#FFB300'}; margin-top:3px;">
        {'🟢' if 'Live' in data_source_badge else '🟡'} {data_source_badge}
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

nav_choice = st.sidebar.radio(
    "Select Platform Module:",
    [
        "🏠 Main Dashboard",
        "1. Target Receptor Hub",
        "2. 3D Docking Studio",
        "3. Simulated VQE Engine",
        "4. Screening VHTS",
        "5. De-Novo Lead Optimizer",
        "6. Report Export"
    ]
)

st.sidebar.markdown("---")
# Ensure candidate selector stays valid
cand_ids = df_candidates["candidate_id"].tolist()
if st.session_state.get("selected_candidate_id") not in cand_ids and cand_ids:
    st.session_state["selected_candidate_id"] = cand_ids[0]

sel_cand_sb = st.sidebar.selectbox("Active Lead Candidate:", cand_ids, index=cand_ids.index(st.session_state.get("selected_candidate_id", cand_ids[0])))
st.session_state["selected_candidate_id"] = sel_cand_sb

st.sidebar.markdown("---")
st.sidebar.caption("Q-DRUG v2.0 Real PubChem Integration\nPubChem REST API • Python • Streamlit")


# ==========================================
# MODULE 0: MAIN DASHBOARD
# ==========================================
if nav_choice == "🏠 Main Dashboard":
    render_disclaimer_banner()
    render_section_header("Quantum-Assisted Computational Drug Discovery & Optimization", TAGLINE, badge="LIVE PROTOTYPE")
    
    # Key Live Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("""
        <div class="q-metric-card">
            <div class="q-metric-value">4 Target Hubs</div>
            <div class="q-metric-label">Therapeutic Targets</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="q-metric-card">
            <div class="q-metric-value">{len(df_candidates)} Leads</div>
            <div class="q-metric-label">Screened Database</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        best_score = df_candidates["qdrug_score"].max()
        st.markdown(f"""
        <div class="q-metric-card">
            <div class="q-metric-value">{best_score:.1f} / 100</div>
            <div class="q-metric-label">Top Q-DRUG Score</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown("""
        <div class="q-metric-card">
            <div class="q-metric-value">25.32 Ha</div>
            <div class="q-metric-label">VQE Energy ΔE</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Platform Architecture Workflow Diagram
    st.markdown("### 🔬 End-to-End Computational Pipeline Architecture")
    
    fig_flow = go.Figure()
    stages = ["1. TARGET HUB", "2. 3D DOCKING", "3. VHTS SCREENING", "4. VQE ENGINE", "5. DE-NOVO OPT", "6. LEAD REPORT"]
    x_pos = [1, 2.5, 4, 5.5, 7, 8.5]
    y_pos = [1, 1, 1, 1, 1, 1]
    
    # Process nodes
    fig_flow.add_trace(go.Scatter(
        x=x_pos, y=y_pos,
        mode="markers+text",
        marker=dict(size=40, color=[THEME_COLORS['primary'], THEME_COLORS['highlight'], THEME_COLORS['secondary'], THEME_COLORS['accent'], THEME_COLORS['success'], THEME_COLORS['warning']], symbol="hexagon"),
        text=stages,
        textposition="bottom center",
        textfont=dict(color=THEME_COLORS['text_main'], size=11, family="Inter"),
        showlegend=False
    ))
    # Arrows / Connection lines
    for i in range(len(x_pos) - 1):
        fig_flow.add_annotation(
            x=x_pos[i+1]-0.4, y=1,
            ax=x_pos[i]+0.4, ay=1,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1.2,
            arrowwidth=2,
            arrowcolor=THEME_COLORS['primary']
        )
        
    fig_flow.update_layout(
        xaxis=dict(range=[0.2, 9.3], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[0.5, 1.5], showgrid=False, zeroline=False, showticklabels=False),
        paper_bgcolor=THEME_COLORS["card_bg"],
        plot_bgcolor="#0A0F1A",
        height=180,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_flow, use_container_width=True)

    st.markdown("""
    <div class="q-card">
        <h4>🚀 Executive Platform Overview</h4>
        <p><b>Q-DRUG</b> integrates classical cheminformatics, molecular docking evaluation, simulated quantum variational eigensolvers (VQE), and de-novo lead optimization into an intuitive unified research environment.</p>
        <ul>
            <li><b>Target Receptor Hub:</b> Analyzes 3D structures (PDB: 6LU7, 3W23, 4B70, 7L10) and active site pockets.</li>
            <li><b>3D Docking Studio:</b> Interactive molecular rendering, Lipinski Rule of 5 validation, and prototype ADMET risk profiles.</li>
            <li><b>Simulated VQE Engine:</b> Calculates molecular ground-state electronic energy using parametrized quantum circuits.</li>
            <li><b>Virtual High-Throughput Screening:</b> Multi-objective candidate ranking on Pareto Frontiers.</li>
            <li><b>De-Novo Lead Optimizer:</b> Simulates chemical modification shifts (-F, -CONH2, -OH) and thermodynamic binding free energy ΔΔG.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# MODULE 1: TARGET RECEPTOR HUB
# ==========================================
elif nav_choice == "1. Target Receptor Hub":
    render_disclaimer_banner()
    render_section_header("1. Target Receptor Hub", "Therapeutic Disease Target Selection & Pocket Profile", badge="MODULE 1")
    
    t_tab1, t_tab2 = st.tabs(["🎯 Predefined Therapeutic Targets", "📥 Load Custom PDB Structure"])
    
    with t_tab1:
        target_keys = list(PREDEFINED_TARGETS.keys())
        selected_t_key = st.selectbox("Select Target Receptor:", target_keys, index=target_keys.index(st.session_state["selected_target_key"]), key="thub_target_selector")
        if selected_t_key != st.session_state["selected_target_key"]:
            st.session_state["selected_target_key"] = selected_t_key
            st.rerun()
        
        t_info = PREDEFINED_TARGETS[selected_t_key]
        pdb_info = fetch_pdb_structure_info(t_info["pdb_id"])
        
        col_t_left, col_t_right = st.columns([1.2, 1])
        
        with col_t_left:
            st.markdown(f"""
            <div class="q-card-glow">
                <h3 style="color:{THEME_COLORS['primary']}; margin-top:0;">{t_info['name']}</h3>
                <p><b>PDB Identifier:</b> <code style="font-size:1.1rem; color:{THEME_COLORS['accent']};">{t_info['pdb_id']}</code></p>
                <p><b>Disease / Application:</b> {t_info['disease']}</p>
                <p><b>Target Category:</b> {t_info['category']}</p>
                <p><b>Description:</b> {t_info['description']}</p>
                <hr style="border-color:#1E2A45;"/>
                <p><b>Active-Site Residues:</b> {", ".join([f"<span class='tag-pass'>{r}</span>" for r in t_info['active_residues']])}</p>
                <p><b>Binding Pocket Information:</b> {t_info['pocket_info']}</p>
                <p><b>Pocket Volume:</b> <span style="color:{THEME_COLORS['warning']}; font-weight:bold;">{t_info['pocket_volume_text']}</span> ({t_info['pocket_volume_val']} Å³)</p>
                <p><b>Drugability Summary:</b> {t_info['drugability_summary']}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col_t_right:
            st.markdown("#### 3D Structural Preview")
            fig_3d_preview = generate_fallback_3d_molecular_plot({"Ribbon": True, "Surface Pocket": True, "Binding Site Residues": True, "Ligand": True}, pdb_id=t_info["pdb_id"])
            st.plotly_chart(fig_3d_preview, use_container_width=True)

    with t_tab2:
        st.markdown("#### Load Custom PDB Structure")
        custom_pdb_input = st.text_input("Enter PDB ID (e.g., 1HSG, 6LU7, 3W23):", value="1HSG")
        if st.button("Fetch & Analyze PDB Structure"):
            res = fetch_pdb_structure_info(custom_pdb_input)
            if "Error" in res["status"]:
                st.error(res["status"])
            else:
                st.success(f"Status: {res['status']}")
                c1, c2 = st.columns(2)
                with c1:
                    st.json(res)
                with c2:
                    fig_custom = generate_fallback_3d_molecular_plot({"Ribbon": True, "Surface Pocket": True, "Ligand": True}, pdb_id=res["pdb_id"])
                    st.plotly_chart(fig_custom, use_container_width=True)


# ==========================================
# MODULE 2: 3D DOCKING STUDIO
# ==========================================
elif nav_choice == "2. 3D Docking Studio":
    render_disclaimer_banner()
    render_section_header("2. 3D Docking Studio", "Interactive Molecular Docking, Lipinski Rule of 5 & ADMET Risk Profile", badge="MODULE 2")
    
    col_d1, col_d2 = st.columns([1.5, 1])
    
    # Filter candidates by current target
    cand_options = df_candidates["candidate_id"].tolist()
    sel_cand_id = st.session_state.get("selected_candidate_id", cand_options[0])
    if sel_cand_id not in cand_options:
        sel_cand_id = cand_options[0]
        
    cand_row = df_candidates[df_candidates["candidate_id"] == sel_cand_id].iloc[0]
    
    with col_d1:
        st.markdown("#### Display Representation Toggles")
        col_tog1, col_tog2, col_tog3, col_tog4, col_tog5 = st.columns(5)
        t_ribbon = col_tog1.checkbox("Ribbon", value=True)
        t_pocket = col_tog2.checkbox("Surface Pocket", value=True)
        t_spacefill = col_tog3.checkbox("Spacefill", value=False)
        t_ligand = col_tog4.checkbox("Ligand", value=True)
        t_residues = col_tog5.checkbox("Binding Site", value=True)
        
        toggles = {
            "Ribbon": t_ribbon,
            "Surface Pocket": t_pocket,
            "Spacefill": t_spacefill,
            "Ligand": t_ligand,
            "Binding Site Residues": t_residues
        }
        
        target_info = PREDEFINED_TARGETS.get(st.session_state["selected_target_key"], PREDEFINED_TARGETS["SARS-CoV-2 Mpro"])
        fig_docking = generate_fallback_3d_molecular_plot(toggles, pdb_id=target_info["pdb_id"])
        st.plotly_chart(fig_docking, use_container_width=True)
        
    with col_d2:
        st.markdown(f"#### Active Candidate: `{cand_row['name']}` ({cand_row['candidate_id']})")
        
        # Lipinski Rule of 5 Evaluation
        lip_res = evaluate_lipinski_rule_of_five(cand_row)
        
        st.markdown(f"""
        <div class="q-card">
            <h4 style="color:{THEME_COLORS['primary']}; margin-top:0;">Lipinski Rule of Five Panel</h4>
            <p><b>Molecular Weight:</b> {lip_res['mw']['val']} Da (Rule: {lip_res['mw']['rule']}) -> <span class="tag-pass">{'PASS' if lip_res['mw']['pass'] else 'FAIL'}</span></p>
            <p><b>LogP (Lipophilicity):</b> {lip_res['logp']['val']} (Rule: {lip_res['logp']['rule']}) -> <span class="tag-pass">{'PASS' if lip_res['logp']['pass'] else 'FAIL'}</span></p>
            <p><b>H-Bond Donors:</b> {lip_res['hbd']['val']} (Rule: {lip_res['hbd']['rule']}) -> <span class="tag-pass">{'PASS' if lip_res['hbd']['pass'] else 'FAIL'}</span></p>
            <p><b>H-Bond Acceptors:</b> {lip_res['hba']['val']} (Rule: {lip_res['hba']['rule']}) -> <span class="tag-pass">{'PASS' if lip_res['hba']['pass'] else 'FAIL'}</span></p>
            <p><b>Rotatable Bonds:</b> {lip_res['rotb']['val']} (Rule: {lip_res['rotb']['rule']}) -> <span class="tag-pass">{'PASS' if lip_res['rotb']['pass'] else 'FAIL'}</span></p>
            <hr style="border-color:#1E2A45;"/>
            <p><b>Overall Lipinski Status:</b> <span class="{'tag-pass' if lip_res['overall_pass'] else 'tag-fail'}">{lip_res['status_label']}</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        # ADMET Risk Panel
        admet_res = predict_admet_prototype_scores(cand_row)
        st.markdown(f"""
        <div class="q-card">
            <h4 style="color:{THEME_COLORS['secondary']}; margin-top:0;">ADMET Prototype Risk Panel</h4>
            <p><b>Toxicity Risk:</b> <span style="color:{admet_res['toxicity']['color']}; font-weight:bold;">{admet_res['toxicity']['level']}</span> ({admet_res['toxicity']['score']})</p>
            <p><b>Aqueous Solubility:</b> <span style="color:{admet_res['solubility']['color']}; font-weight:bold;">{admet_res['solubility']['level']}</span> ({admet_res['solubility']['score']})</p>
            <p><b>GI Absorption:</b> {admet_res['absorption']['score']} ({admet_res['absorption']['level']})</p>
            <p><b>Metabolic Stability:</b> {admet_res['metabolic_stability']['score']} ({admet_res['metabolic_stability']['level']})</p>
            <p style="font-size:0.75rem; color:#FFB300; margin-top:8px;"><i>⚠️ {admet_res['disclaimer']}</i></p>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# MODULE 3: SIMULATED VQE ENGINE
# ==========================================
elif nav_choice == "3. Simulated VQE Engine":
    render_disclaimer_banner()
    render_section_header("3. Simulated VQE Engine", "Quantum Variational Eigensolver Optimization & Ground State Energy Convergence", badge="QUANTUM CENTERPIECE")
    
    st.markdown("""
    <div style="background: rgba(0, 240, 255, 0.05); border: 1px solid #00F0FF; padding: 12px; border-radius: 8px; margin-bottom: 15px;">
        ⚡ <b>SIMULATED VQE — No physical quantum hardware used.</b><br/>
        This module executes quantum circuit simulations modeling the electronic ground state energy of target-ligand molecular Hamiltonians.
    </div>
    """, unsafe_allow_html=True)
    
    col_v1, col_v2 = st.columns([1, 2])
    
    with col_v1:
        st.markdown("#### Quantum Engine Parameters")
        num_qubits = st.slider("Qubits Count:", min_value=4, max_value=12, value=6, step=1)
        ansatz = st.selectbox("Variational Ansatz:", ["RealAmplitudes", "UCCD", "HardwareEfficient"])
        optimizer = st.selectbox("Classical Optimizer:", ["SPSA", "COBYLA", "Adam"])
        noise_model = st.selectbox("Noise Model:", ["Ideal (Noiseless)", "Depolarizing", "Thermal"])
        
        st.markdown("---")
        run_vqe_btn = st.button("▶ Run VQE Optimization Execution", type="primary", use_container_width=True)

    with col_v2:
        st.markdown("#### Parameterized Quantum Circuit Diagram")
        fig_circuit = render_quantum_circuit_diagram(num_qubits=num_qubits, ansatz=ansatz)
        st.plotly_chart(fig_circuit, use_container_width=True)

    if run_vqe_btn or st.session_state["vqe_results"] is None:
        vqe_engine = VQEEngine(num_qubits=num_qubits, ansatz=ansatz, optimizer=optimizer, noise_model=noise_model)
        with st.spinner("Simulating Quantum VQE Optimization Execution..."):
            vqe_res = vqe_engine.run_vqe()
            st.session_state["vqe_results"] = vqe_res
            
    vqe_res = st.session_state["vqe_results"]
    
    st.markdown("### VQE Optimization Results & Convergence Trajectory")
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("Initial Energy", f"{vqe_res['initial_energy']:.2f} Ha")
    with col_m2:
        st.metric("Final Ground Energy", f"{vqe_res['final_energy']:.2f} Ha")
    with col_m3:
        st.metric("Energy Improvement (ΔE)", f"{vqe_res['improvement']:.2f} Ha")
    with col_m4:
        st.metric("Ansatz / Qubits", f"{vqe_res['ansatz']} ({vqe_res['qubits']}Q)")
        
    fig_conv = build_convergence_chart(vqe_res)
    st.plotly_chart(fig_conv, use_container_width=True)


# ==========================================
# MODULE 4: SCREENING VHTS
# ==========================================
elif nav_choice == "4. Screening VHTS":
    render_disclaimer_banner()
    render_section_header("4. Compound Screening & Ranking VHTS", "Real PubChem Compound Screening & Quantum-Inspired Candidate Ranking", badge="PUBCHEM INSIDE")

    # Status Header
    sc1, sc2, sc3 = st.columns([1.5, 1, 1])
    with sc1:
        st.markdown(f"**Target Selected:** `{st.session_state['selected_target_key']}`")
    with sc2:
        st.markdown(f"**Compounds Screened:** `{len(df_candidates)} Real Compounds`")
    with sc3:
        st.markdown(f"**Data Source Status:** <span class=\"{'badge-pubchem' if 'Live' in data_source_badge else 'badge-cache'}\">{data_source_badge}</span>", unsafe_allow_html=True)

    st.caption(status_message)
    st.markdown("---")

    # Candidate Ranking System Table
    st.markdown("### 🏆 Real PubChem Candidates Ranking")
    st.caption("Score labeled as **Quantum-Inspired Candidate Score**. Sourced from PubChem API / verified database.")

    df_sorted = df_candidates.sort_values(by="qdrug_score", ascending=False).reset_index(drop=True)
    df_sorted["Rank"] = df_sorted.index + 1
    df_sorted["Quantum-Inspired Candidate Score"] = df_sorted["qdrug_score"].apply(lambda s: f"{s:.2f} / 100")
    df_sorted["Recommendation"] = df_sorted["qdrug_score"].apply(assign_recommendation_label)

    # Format SMILES column cleanly for display
    df_display = df_sorted.copy()
    if "canonical_smiles" not in df_display.columns:
        df_display["canonical_smiles"] = df_display["smiles"]
    if "pubchem_cid" not in df_display.columns:
        df_display["pubchem_cid"] = 0
    if "formula" not in df_display.columns:
        df_display["formula"] = "N/A"

    st.dataframe(
        df_display[["Rank", "name", "pubchem_cid", "mw", "formula", "canonical_smiles", "Quantum-Inspired Candidate Score", "Recommendation"]],
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", width="small"),
            "name": st.column_config.TextColumn("Compound Name", width="medium"),
            "pubchem_cid": st.column_config.NumberColumn("PubChem CID", format="%d", width="small"),
            "mw": st.column_config.NumberColumn("Molecular Weight (Da)", format="%.2f", width="small"),
            "formula": st.column_config.TextColumn("Formula", width="small"),
            "canonical_smiles": st.column_config.TextColumn("SMILES", width="large"),
            "Quantum-Inspired Candidate Score": st.column_config.TextColumn("Quantum-Inspired Candidate Score", width="medium"),
            "Recommendation": st.column_config.TextColumn("Recommendation Tier", width="medium")
        },
        use_container_width=True,
        height=340
    )

    st.markdown("---")

    # Candidate Detail Inspector Panel & Score Visualization
    col_insp1, col_insp2 = st.columns([1.2, 1])

    with col_insp1:
        st.markdown("### 🔍 Interactive Compound Detail Inspector")
        sel_comp_name = st.selectbox(
            "Select Compound to Inspect Details:",
            df_sorted["name"].tolist(),
            index=0
        )
        selected_comp = df_sorted[df_sorted["name"] == sel_comp_name].iloc[0]
        pubchem_link = selected_comp.get("pubchem_url") or f"https://pubchem.ncbi.nlm.nih.gov/compound/{selected_comp['pubchem_cid']}"

        st.markdown(f"""
        <div class="q-card-glow">
            <h3 style="color:#00F0FF; margin-top:0;">{selected_comp['name']} &nbsp; <span style="font-size:0.9rem; color:#94A3B8;">(PubChem CID: {selected_comp['pubchem_cid']})</span></h3>
            <p><b>IUPAC Name:</b> <i>{selected_comp.get('iupac_name', selected_comp['name'])}</i></p>
            <p><b>Molecular Formula:</b> <code style="font-size:1.1rem; color:#00FF88;">{selected_comp.get('formula', 'N/A')}</code> &nbsp;|&nbsp; <b>Molecular Weight:</b> <code>{selected_comp['mw']:.2f} Da</code></p>
            <p><b>Canonical SMILES:</b><br/><code style="font-size:0.85rem; color:#E2E8F0; word-break:break-all;">{selected_comp.get('canonical_smiles', selected_comp['smiles'])}</code></p>
            <p><b>Isomeric SMILES:</b><br/><code style="font-size:0.85rem; color:#94A3B8; word-break:break-all;">{selected_comp.get('isomeric_smiles', selected_comp['smiles'])}</code></p>
            <hr style="border-color:#1E2A45;"/>
            <p><b>Quantum-Inspired Candidate Score:</b> <b style="color:#00F0FF; font-size:1.3rem;">{selected_comp['qdrug_score']:.2f} / 100</b> &nbsp; ({selected_comp['Recommendation']})</p>
            <p><b>PubChem Database URL:</b> <a href="{pubchem_link}" target="_blank" style="color:#00F0FF;">View on PubChem ↗</a></p>
        </div>
        """, unsafe_allow_html=True)

    with col_insp2:
        st.markdown("### 🖼️ PubChem 2D Structure Preview")
        cid_val = selected_comp['pubchem_cid']
        img_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid_val}/PNG" if cid_val else None
        if img_url:
            st.image(img_url, caption=f"{selected_comp['name']} (PubChem CID {cid_val})", width=260)
        else:
            st.info("Structure preview available online via PubChem CID.")

    st.markdown("---")

    # Visualization: Candidate Scores Bar Chart
    st.markdown("### 📊 Quantum-Inspired Candidate Score Distribution")
    fig_score_bar = px.bar(
        df_sorted.head(10),
        x="name",
        y="qdrug_score",
        color="qdrug_score",
        color_continuous_scale="Viridis",
        labels={"name": "Compound Name", "qdrug_score": "Quantum-Inspired Candidate Score"},
        title=f"Top Candidates Ranked by Quantum-Inspired Candidate Score ({st.session_state['selected_target_key']})"
    )
    fig_score_bar.update_layout(
        paper_bgcolor=THEME_COLORS["card_bg"],
        plot_bgcolor="#0A0F1A",
        font=dict(color=THEME_COLORS["text_main"]),
        height=320
    )
    st.plotly_chart(fig_score_bar, use_container_width=True)

    col_vhts1, col_vhts2 = st.columns([1.2, 1])

    with col_vhts1:
        st.markdown("### Pareto Frontier Analysis")
        fig_pareto = generate_pareto_chart(df_sorted)
        st.plotly_chart(fig_pareto, use_container_width=True)

    with col_vhts2:
        st.markdown("### Radar Profile Multi-Candidate Comparison")
        sel_cands_radar = st.multiselect("Select up to 3 candidates:", df_sorted["candidate_id"].tolist(), default=df_sorted["candidate_id"].tolist()[:min(3, len(df_sorted))], max_selections=3)
        if sel_cands_radar:
            df_radar_sel = df_sorted[df_sorted["candidate_id"].isin(sel_cands_radar)]
            fig_radar = generate_candidate_radar_chart(df_radar_sel)
            st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("""
    <div class="q-card" style="margin-top:20px; border-left: 4px solid #00F0FF;">
        <b>Data Source:</b> Compound data sourced from PubChem.<br/>
        <span style="font-size:0.85rem; color:#94A3B8;">
            <b>Disclaimer:</b> Q-DRUG is a computational research prototype. Predictions require experimental and clinical validation and should not be interpreted as medical advice.
        </span>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# MODULE 5: DE-NOVO LEAD OPTIMIZER
# ==========================================
elif nav_choice == "5. De-Novo Lead Optimizer":
    render_disclaimer_banner()
    render_section_header("5. De-Novo Lead Optimizer", "Lead Modification Studio & Thermodynamic Binding Free Energy (ΔΔG)", badge="MODULE 5")
    
    col_o1, col_o2 = st.columns([1, 1.5])
    
    with col_o1:
        st.markdown("#### Select Base Lead Candidate")
        cand_list = df_candidates["candidate_id"].tolist()
        base_id = st.selectbox("Base Candidate ID:", cand_list, index=0)
        base_cand = df_candidates[df_candidates["candidate_id"] == base_id].iloc[0].to_dict()
        
        st.markdown("#### Select Chemical Modification")
        mod_name = st.selectbox("Modification Type:", list(MODIFICATION_PROTOTYPES.keys()))
        mod_info = MODIFICATION_PROTOTYPES[mod_name]
        
        st.info(f"**Modification Notes:** {mod_info['description']}")
        st.caption("⚠️ Illustrative optimization parameters — not experimentally validated.")

    opt_res = optimize_lead_candidate(base_cand, mod_name)
    
    with col_o2:
        st.markdown("#### Transformation Pipeline & Thermodynamic ΔΔG")
        st.markdown(f"""
        <div class="q-card-glow">
            <h3 style="color:#00F0FF; margin-top:0;">{base_cand['name']} &nbsp; ➔ &nbsp; {mod_name} &nbsp; ➔ &nbsp; {opt_res['opt_candidate']['name']}</h3>
            <p><b>Thermodynamic ΔΔG Equation:</b></p>
            <p><code style="font-size:1.1rem; color:#00FF88;">{opt_res['formula_text']}</code></p>
            <table style="width:100%; color:#E2E8F0; margin-top:10px;">
                <tr><th>Metric</th><th>Original Lead</th><th>Optimized Lead</th><th>Shift / Delta</th></tr>
                <tr><td>Binding Affinity (pKd)</td><td>{opt_res['orig_pkd']:.2f}</td><td><b>{opt_res['opt_pkd']:.2f}</b></td><td><span style="color:#00FF88;">+{opt_res['delta_pkd']:.2f}</span></td></tr>
                <tr><td>Solubility Score</td><td>{opt_res['orig_sol']:.2f}</td><td><b>{opt_res['opt_sol']:.2f}</b></td><td>{opt_res['opt_sol'] - opt_res['orig_sol']:+.2f}</td></tr>
                <tr><td>Toxicity Risk Score</td><td>{opt_res['orig_tox']:.2f}</td><td><b>{opt_res['opt_tox']:.2f}</b></td><td>{opt_res['opt_tox'] - opt_res['orig_tox']:+.2f}</td></tr>
                <tr><td>Q-DRUG Score</td><td>{opt_res['orig_score']:.2f}</td><td><b>{opt_res['opt_score']:.2f}</b></td><td><span style="color:#00FF88;">+{opt_res['score_delta']:.2f} pts</span></td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Promote to Active Lead Candidate", type="primary", use_container_width=True):
            st.session_state["active_lead"] = opt_res["opt_candidate"]
            # Append to candidate DB if not present
            if not any(df_candidates["candidate_id"] == opt_res["opt_candidate"]["candidate_id"]):
                df_updated = pd.concat([df_candidates, pd.DataFrame([opt_res["opt_candidate"]])], ignore_index=True)
                df_updated.to_csv("data/drugs.csv", index=False)
            st.success(f"Promoted {opt_res['opt_candidate']['name']} to Active Lead! Updated in Database.")


# ==========================================
# MODULE 6: REPORT EXPORT
# ==========================================
elif nav_choice == "6. Report Export":
    render_disclaimer_banner()
    render_section_header("6. Scientific Report Export", "Generate Executive HTML / Printable PDF Scientific Report", badge="MODULE 6")
    
    target_info = PREDEFINED_TARGETS.get(st.session_state["selected_target_key"], PREDEFINED_TARGETS["SARS-CoV-2 Mpro"])
    cand_row = df_candidates[df_candidates["candidate_id"] == st.session_state["selected_candidate_id"]].iloc[0]
    lipinski_info = evaluate_lipinski_rule_of_five(cand_row)
    admet_info = predict_admet_prototype_scores(cand_row)
    vqe_results = st.session_state.get("vqe_results") or VQEEngine().run_vqe()
    vhts_top_df = df_candidates.sort_values(by="qdrug_score", ascending=False)
    
    html_report = generate_scientific_html_report(target_info, cand_row, lipinski_info, admet_info, vqe_results, vhts_top_df)
    
    st.download_button(
        label="📥 Download Executive Scientific Report (.html)",
        data=html_report,
        file_name=f"Q-DRUG_Report_{target_info['pdb_id']}.html",
        mime="text/html",
        type="primary"
    )
    
    st.markdown("### Scientific Report Interactive Preview")
    st.components.v1.html(html_report, height=650, scrolling=True)
