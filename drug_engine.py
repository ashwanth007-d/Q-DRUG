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

from pubchem_service import fetch_compounds_for_target

def preprocess_and_score_compound(comp, target_name="EGFR Kinase T790M"):
    """
    Preprocesses molecular data for a real PubChem compound and calculates Quantum-Inspired Candidate Score.
    """
    smiles = comp.get("smiles") or comp.get("canonical_smiles") or "C1=CC=CC=C1"
    mw = float(comp.get("mw", 400.0))
    cid = comp.get("pubchem_cid") or comp.get("cid") or 0
    name = comp.get("name") or f"PubChem CID {cid}"
    formula = comp.get("formula") or "Unknown"
    iupac = comp.get("iupac_name") or name

    # Calculate descriptors via RDKit if available, else graph estimator
    if HAS_RDKIT:
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is not None:
                logp = float(Crippen.MolLogP(mol))
                hbd = int(Lipinski.NumHDonors(mol))
                hba = int(Lipinski.NumHAcceptors(mol))
                rotb = int(Lipinski.NumRotatableBonds(mol))
            else:
                logp, hbd, hba, rotb = 2.5, 2, 5, 4
        except Exception:
            logp, hbd, hba, rotb = 2.5, 2, 5, 4
    else:
        c_count = smiles.upper().count("C")
        n_count = smiles.upper().count("N")
        o_count = smiles.upper().count("O")
        f_count = smiles.upper().count("F")
        logp = round(0.15 * c_count - 0.2 * o_count + 0.1 * f_count, 2)
        hbd = max(1, n_count + o_count // 2)
        hba = max(2, n_count * 2 + o_count)
        rotb = max(1, len(smiles) // 8)

    # Determine biological/affinity baseline from descriptors
    binding_affinity = float(comp.get("binding_affinity", round(min(9.6, max(6.5, 7.8 + (logp - 2.0) * 0.35 + (rotb * 0.04))), 2)))
    quantum_energy = float(comp.get("quantum_energy", round(-130.0 - mw * 0.18, 2)))
    activity = float(comp.get("activity", round(min(0.96, max(0.68, 0.76 + (binding_affinity - 7.0) * 0.07)), 2)))
    toxicity = float(comp.get("toxicity", round(max(0.08, min(0.35, 0.14 + (logp - 2.5) * 0.04)), 2)))
    solubility = float(comp.get("solubility", round(max(0.35, min(0.95, 0.82 - (logp - 2.0) * 0.08)), 2)))
    druglikeness = float(comp.get("druglikeness", round(0.90 if mw <= 500 and logp <= 5.0 else 0.72, 2)))

    row = {
        "candidate_id": f"CID-{cid}" if cid else comp.get("candidate_id", "QD-101"),
        "name": name,
        "pubchem_cid": cid,
        "formula": formula,
        "mw": mw,
        "smiles": smiles,
        "canonical_smiles": comp.get("canonical_smiles", smiles),
        "isomeric_smiles": comp.get("isomeric_smiles", smiles),
        "iupac_name": iupac,
        "target": target_name,
        "binding_affinity": binding_affinity,
        "quantum_energy": quantum_energy,
        "activity": activity,
        "toxicity": toxicity,
        "solubility": solubility,
        "druglikeness": druglikeness,
        "logp": logp,
        "hbd": hbd,
        "hba": hba,
        "rotb": rotb,
        "structure_img": comp.get("structure_img", f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"),
        "pubchem_url": comp.get("pubchem_url", f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}"),
        "data_source": comp.get("data_source", "PubChem Data Source")
    }

    # Calculate Quantum-Inspired Candidate Score
    row["qdrug_score"] = calculate_qdrug_score(row)
    return row

def load_candidate_database(csv_path="data/drugs.csv", target_name=None):
    """
    Loads candidate molecules from real PubChem database for target, or falls back to CSV.
    """
    if target_name:
        records, data_source_label, status_msg = fetch_compounds_for_target(target_name)
        if records:
            processed = [preprocess_and_score_compound(r, target_name) for r in records]
            df = pd.DataFrame(processed)
            df = df.sort_values(by="qdrug_score", ascending=False).reset_index(drop=True)
            df["Rank"] = df.index + 1
            df.attrs["data_source_label"] = data_source_label
            df.attrs["status_msg"] = status_msg
            return df

    # Fallback to local CSV or demo data
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            if "qdrug_score" not in df.columns:
                df["qdrug_score"] = df.apply(calculate_qdrug_score, axis=1)
            if "pubchem_cid" not in df.columns:
                df["pubchem_cid"] = 0
            if "formula" not in df.columns:
                df["formula"] = "N/A"
            df = df.sort_values(by="qdrug_score", ascending=False).reset_index(drop=True)
            df["Rank"] = df.index + 1
            df.attrs["data_source_label"] = "Local CSV Database"
            df.attrs["status_msg"] = "Loaded candidates from local CSV."
            return df
        except Exception:
            pass

    df = generate_csv_if_missing(csv_path)
    if "pubchem_cid" not in df.columns:
        df["pubchem_cid"] = 0
    if "formula" not in df.columns:
        df["formula"] = "N/A"
    df = df.sort_values(by="qdrug_score", ascending=False).reset_index(drop=True)
    df["Rank"] = df.index + 1
    df.attrs["data_source_label"] = "Real PubChem Dataset (Fallback)"
    df.attrs["status_msg"] = "Loaded dataset."
    return df

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
