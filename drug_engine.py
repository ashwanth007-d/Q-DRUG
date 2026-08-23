"""
Virtual High-Throughput Screening (VHTS) Engine for Q-DRUG Platform.
Manages candidate screening, SMILES validation, Pareto frontier analysis, and radar charts.
Supports RDKit when available, with a robust fallback chemical estimator engine.
"""

import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from config import DEFAULT_SCORING_WEIGHTS, THEME_COLORS
from demo_data import generate_csv_if_missing, calculate_qdrug_score

# Check RDKit availability
HAS_RDKIT = False
try:
    import rdkit
    from rdkit import Chem
    from rdkit.Chem import Descriptors, Crippen, Lipinski
    HAS_RDKIT = True
except ImportError:
    HAS_RDKIT = False

def load_candidate_database(csv_path="data/drugs.csv"):
    """
    Loads candidate molecules database from CSV or generates initial dataset if missing.
    """
    if not os.path.exists(csv_path):
        return generate_csv_if_missing(csv_path)
    try:
        df = pd.read_csv(csv_path)
        # Ensure qdrug_score column exists
        if "qdrug_score" not in df.columns:
            df["qdrug_score"] = df.apply(calculate_qdrug_score, axis=1)
        return df
    except Exception:
        return generate_csv_if_missing(csv_path)

def assign_recommendation_label(score):
    """
    Assigns recommendation tier based on Q-DRUG score.
    """
    score = float(score)
    if score >= 85.0:
        return "Highly Promising"
    elif score >= 78.0:
        return "Promising"
    elif score >= 70.0:
        return "Moderate"
    else:
        return "Low Priority"

def compute_pareto_frontier(df):
    """
    Identifies Pareto-optimal candidates maximizing Binding Affinity and Quantum Energy Optimization.
    """
    pts = df[["binding_affinity", "quantum_energy"]].values
    pareto_mask = np.ones(len(pts), dtype=bool)
    
    for i, p in enumerate(pts):
        for j, q in enumerate(pts):
            if i != j:
                # We want higher binding_affinity AND lower quantum_energy (more negative)
                if q[0] >= p[0] and q[1] <= p[1] and (q[0] > p[0] or q[1] < p[1]):
                    pareto_mask[i] = False
                    break
    return pareto_mask

def generate_pareto_chart(df):
    """
    Generates interactive Plotly scatter plot for Pareto Frontier (Binding Affinity vs Quantum Energy).
    """
    df_chart = df.copy()
    df_chart["pareto_optimal"] = compute_pareto_frontier(df_chart)
    df_chart["recommendation"] = df_chart["qdrug_score"].apply(assign_recommendation_label)
    
    fig = go.Figure()
    
    # Non-Pareto points
    non_pareto = df_chart[~df_chart["pareto_optimal"]]
    fig.add_trace(go.Scatter(
        x=non_pareto["binding_affinity"],
        y=non_pareto["quantum_energy"],
        mode="markers",
        name="Screened Candidates",
        marker=dict(size=10, color=THEME_COLORS["primary"], opacity=0.6),
        text=non_pareto["name"],
        customdata=non_pareto[["candidate_id", "qdrug_score", "recommendation"]],
        hovertemplate="<b>%{text}</b> (%{customdata[0]})<br/>Binding Affinity: %{x:.2f} pKd<br/>Quantum Energy: %{y:.2f} Hartree<br/>Q-DRUG Score: %{customdata[1]} (%{customdata[2]})<extra></extra>"
    ))
    
    # Pareto frontier points
    pareto = df_chart[df_chart["pareto_optimal"]].sort_values(by="binding_affinity")
    fig.add_trace(go.Scatter(
        x=pareto["binding_affinity"],
        y=pareto["quantum_energy"],
        mode="markers+lines",
        name="★ Pareto Optimal Lead Frontier",
        marker=dict(size=14, color=THEME_COLORS["accent"], symbol="star"),
        line=dict(color=THEME_COLORS["accent"], width=2.5, dash="dash"),
        text=pareto["name"],
        customdata=pareto[["candidate_id", "qdrug_score", "recommendation"]],
        hovertemplate="<b>★ PARETO LEAD: %{text}</b><br/>Binding Affinity: %{x:.2f} pKd<br/>Quantum Energy: %{y:.2f} Hartree<br/>Q-DRUG Score: %{customdata[1]}<extra></extra>"
    ))
    
    fig.update_layout(
        title=dict(text="VHTS Pareto Frontier: Binding Affinity vs Quantum Optimization Energy", font=dict(size=15, color=THEME_COLORS["text_main"])),
        xaxis_title="Binding Affinity (pKd — Higher is Stronger)",
        yaxis_title="Quantum Ground State Energy (Hartree — More Negative is Optimal)",
        paper_bgcolor=THEME_COLORS["card_bg"],
        plot_bgcolor="#0A0F1A",
        font=dict(color=THEME_COLORS["text_main"]),
        xaxis=dict(gridcolor="#1E293B"),
        yaxis=dict(gridcolor="#1E293B"),
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def generate_candidate_radar_chart(selected_df):
    """
    Generates 6-axis Plotly Radar Chart comparing up to 3 candidate molecules across 6 metrics.
    """
    categories = ["Activity", "Binding Affinity", "Solubility", "Drug-likeness", "Toxicity Safety", "Quantum Score"]
    
    fig = go.Figure()
    
    colors = [THEME_COLORS["primary"], THEME_COLORS["secondary"], THEME_COLORS["success"]]
    
    for idx, (_, row) in enumerate(selected_df.iterrows()):
        norm_binding = float(np.clip((row["binding_affinity"] - 5.0) / 5.0, 0.0, 1.0))
        act = float(row["activity"])
        sol = float(row["solubility"])
        dl = float(row["druglikeness"])
        tox_safety = float(np.clip(1.0 - row["toxicity"], 0.0, 1.0))
        qe_score = float(np.clip((-row["quantum_energy"] - 100.0) / 200.0, 0.0, 1.0))
        
        r_values = [act, norm_binding, sol, dl, tox_safety, qe_score]
        r_values.append(r_values[0])  # Close loop
        cat_closed = categories + [categories[0]]
        
        color = colors[idx % len(colors)]
        
        fig.add_trace(go.Scatterpolar(
            r=r_values,
            theta=cat_closed,
            fill='toself',
            name=f"{row['name']} ({row['candidate_id']})",
            line=dict(color=color, width=2.5),
            fillcolor=f"rgba({int(color[1:3],16) if len(color)==7 else 0}, 240, 255, 0.15)"
        ))
        
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1.0], gridcolor="#1E293B", tickfont=dict(size=9)),
            angularaxis=dict(gridcolor="#1E293B", tickfont=dict(color=THEME_COLORS["text_main"], size=11)),
            bgcolor="#0A0F1A"
        ),
        paper_bgcolor=THEME_COLORS["card_bg"],
        font=dict(color=THEME_COLORS["text_main"]),
        title=dict(text="Multi-Candidate Profile Radar Comparison", font=dict(size=14, color=THEME_COLORS["text_main"])),
        margin=dict(l=40, r=40, t=50, b=40),
        showlegend=True
    )
    return fig

def parse_and_score_custom_smiles(smiles_str, target_name="SARS-CoV-2 Mpro"):
    """
    Validates custom SMILES string, calculates chemical descriptors using RDKit or fallback graph estimator,
    and returns parsed candidate dictionary.
    """
    clean_smiles = smiles_str.strip()
    if not clean_smiles:
        return {"error": "SMILES string cannot be empty."}
        
    if HAS_RDKIT:
        try:
            mol = Chem.MolFromSmiles(clean_smiles)
            if mol is None:
                return {"error": f"Invalid chemical SMILES syntax: '{clean_smiles}' could not be parsed by RDKit."}
            mw = float(Descriptors.MolWt(mol))
            logp = float(Crippen.MolLogP(mol))
            hbd = int(Lipinski.NumHDonors(mol))
            hba = int(Lipinski.NumHAcceptors(mol))
            rotb = int(Lipinski.NumRotatableBonds(mol))
        except Exception as e:
            return {"error": f"RDKit parse error: {str(e)}"}
    else:
        # Fallback chemical graph estimator when RDKit absent
        if len(clean_smiles) < 3 or not any(c in clean_smiles for c in ["C", "c", "N", "n", "O", "o"]):
            return {"error": f"Invalid SMILES string syntax: '{clean_smiles}' does not contain recognized chemical symbols."}
            
        c_count = clean_smiles.upper().count("C")
        n_count = clean_smiles.upper().count("N")
        o_count = clean_smiles.upper().count("O")
        f_count = clean_smiles.upper().count("F")
        
        mw = round(c_count * 12.01 + n_count * 14.01 + o_count * 16.0 + f_count * 19.0 + 50.0, 2)
        logp = round(0.15 * c_count - 0.2 * o_count + 0.1 * f_count, 2)
        hbd = max(1, n_count + o_count // 2)
        hba = max(2, n_count * 2 + o_count)
        rotb = max(1, len(clean_smiles) // 8)

    # Estimate prototype properties
    binding_affinity = round(min(9.5, max(6.0, 7.5 + (logp - 2.0) * 0.4 + (rotb * 0.05))), 2)
    quantum_energy = round(-120.0 - mw * 0.2, 2)
    activity = round(min(0.96, max(0.65, 0.75 + (binding_affinity - 7.0) * 0.08)), 2)
    toxicity = round(max(0.05, min(0.40, 0.15 + (logp - 3.0) * 0.05)), 2)
    solubility = round(max(0.30, min(0.95, 0.80 - (logp - 2.0) * 0.1)), 2)
    druglikeness = round(0.85 if mw <= 500 and logp <= 5 else 0.65, 2)
    
    cand = {
        "candidate_id": f"CUSTOM-{np.random.randint(100, 999)}",
        "name": f"Custom Lead ({clean_smiles[:10]}...)",
        "target": target_name,
        "smiles": clean_smiles,
        "binding_affinity": binding_affinity,
        "quantum_energy": quantum_energy,
        "activity": activity,
        "toxicity": toxicity,
        "solubility": solubility,
        "druglikeness": druglikeness,
        "mw": mw,
        "logp": logp,
        "hbd": hbd,
        "hba": hba,
        "rotb": rotb,
        "data_type": "demonstration / user input"
    }
    cand["qdrug_score"] = calculate_qdrug_score(cand)
    return cand
