"""
3D Docking Studio & Receptor Hub Engine for Q-DRUG Platform.
Handles PDB structures, 3D visualization, Lipinski Rule of 5 evaluation, and ADMET risk analysis.
"""

import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Check py3Dmol availability
HAS_PY3DMOL = False
try:
    import py3Dmol
    HAS_PY3DMOL = True
except ImportError:
    HAS_PY3DMOL = False

from config import PREDEFINED_TARGETS, THEME_COLORS

def fetch_pdb_structure_info(pdb_id):
    """
    Attempts online fetch of PDB structure summary from RCSB PDB API.
    Provides robust fallback when offline or when retrieval fails.
    """
    clean_id = pdb_id.strip().upper()
    
    # Check predefined targets first
    for t_key, t_data in PREDEFINED_TARGETS.items():
        if t_data["pdb_id"] == clean_id:
            return {
                "status": "Success (Predefined Target)",
                "pdb_id": clean_id,
                "name": t_data["name"],
                "residues_count": 306 if clean_id == "6LU7" else (285 if clean_id == "3W23" else 390),
                "atoms_count": 2450 if clean_id == "6LU7" else (2280 if clean_id == "3W23" else 3100),
                "resolution": "2.16 Å",
                "experimental_method": "X-RAY DIFFRACTION",
                "pocket_volume_text": t_data["pocket_volume_text"],
                "pocket_volume_val": t_data["pocket_volume_val"],
                "active_residues": t_data["active_residues"],
                "is_custom": False
            }
            
    # Custom PDB retrieval attempt
    if len(clean_id) != 4 or not clean_id.isalnum():
        return {
            "status": "Error: Invalid PDB ID format. Must be 4 alphanumeric characters (e.g. 1HSG, 6LU7).",
            "pdb_id": clean_id,
            "is_custom": True,
            "success": False
        }
        
    try:
        import urllib.request
        url = f"https://files.rcsb.org/download/{clean_id}.pdb"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=4) as response:
            lines = response.read().decode('utf-8').splitlines()
            atom_lines = [l for l in lines if l.startswith("ATOM")]
            res_set = set(l[17:26] for l in atom_lines)
            
            return {
                "status": "Successfully Fetched Online PDB",
                "pdb_id": clean_id,
                "name": f"Custom PDB Structure ({clean_id})",
                "residues_count": len(res_set) if res_set else 240,
                "atoms_count": len(atom_lines) if atom_lines else 1850,
                "resolution": "2.00 Å (estimated)",
                "experimental_method": "X-RAY DIFFRACTION",
                "pocket_volume_text": "Pocket volume: Demo estimate / not experimentally validated",
                "pocket_volume_val": round(800.0 + len(res_set) * 1.2, 1),
                "active_residues": ["Res101", "Res145", "Res210"],
                "is_custom": True,
                "success": True
            }
    except Exception:
        # Offline or connection failed fallback
        return {
            "status": "Offline / Structure Retrieval Fallback (Synthetic Profile)",
            "pdb_id": clean_id,
            "name": f"Custom Target Structure ({clean_id})",
            "residues_count": 310,
            "atoms_count": 2420,
            "resolution": "2.10 Å (estimated)",
            "experimental_method": "X-RAY DIFFRACTION / SIMULATED",
            "pocket_volume_text": "Pocket volume: Demo estimate / not experimentally validated",
            "pocket_volume_val": 850.0,
            "active_residues": ["Site-1", "Site-2", "Site-3"],
            "is_custom": True,
            "success": True
        }

def generate_fallback_3d_molecular_plot(toggles, pdb_id="6LU7"):
    """
    Generates a 3D Plotly visual representation of protein ribbon, active site pocket,
    spacefill atoms, and docked ligand when py3Dmol is absent or as standard interactive view.
    """
    fig = go.Figure()
    
    np.random.seed(hash(pdb_id) % 1000)
    
    # 1. Protein Alpha-Helix Backbone (Ribbon representation)
    if toggles.get("Ribbon", True):
        t = np.linspace(0, 4 * np.pi, 80)
        x_rib = 12 * np.cos(t)
        y_rib = 12 * np.sin(t)
        z_rib = np.linspace(-15, 15, 80)
        
        fig.add_trace(go.Scatter3d(
            x=x_rib, y=y_rib, z=z_rib,
            mode='lines',
            name='Protein Ribbon Backbone',
            line=dict(color=THEME_COLORS['primary'], width=8),
            hoverinfo='name'
        ))
        
        # Second helix chain
        x_rib2 = 8 * np.cos(t + np.pi/2)
        y_rib2 = 8 * np.sin(t + np.pi/2)
        z_rib2 = np.linspace(-12, 12, 80)
        fig.add_trace(go.Scatter3d(
            x=x_rib2, y=y_rib2, z=z_rib2,
            mode='lines',
            name='Secondary Beta Chain',
            line=dict(color=THEME_COLORS['secondary'], width=6),
            hoverinfo='name'
        ))

    # 2. Surface Pocket Mesh Representation
    if toggles.get("Surface Pocket", True):
        u = np.linspace(0, 2 * np.pi, 20)
        v = np.linspace(0, np.pi, 20)
        x_p = 5 * np.outer(np.cos(u), np.sin(v))
        y_p = 5 * np.outer(np.sin(u), np.sin(v))
        z_p = 4 * np.outer(np.ones(np.size(u)), np.cos(v))
        
        fig.add_trace(go.Mesh3d(
            x=x_p.flatten(), y=y_p.flatten(), z=z_p.flatten(),
            alphahull=5,
            opacity=0.25,
            color=THEME_COLORS['accent'],
            name='Binding Pocket Surface',
            hoverinfo='name'
        ))

    # 3. Spacefill Residue Spheres
    if toggles.get("Spacefill", False):
        n_spheres = 40
        x_sp = np.random.uniform(-10, 10, n_spheres)
        y_sp = np.random.uniform(-10, 10, n_spheres)
        z_sp = np.random.uniform(-10, 10, n_spheres)
        
        fig.add_trace(go.Scatter3d(
            x=x_sp, y=y_sp, z=z_sp,
            mode='markers',
            name='Spacefill Atoms',
            marker=dict(size=9, color='#475569', opacity=0.7),
            hoverinfo='name'
        ))

    # 4. Binding Site Residues
    if toggles.get("Binding Site Residues", True):
        x_res = [2.1, -1.8, 0.5, -2.5]
        y_res = [1.5, 2.8, -3.1, -1.2]
        z_res = [3.0, -1.5, 0.8, 2.2]
        labels = ["His41 (Catalytic)", "Cys145 (Catalytic)", "Gly143", "Glu166"]
        
        fig.add_trace(go.Scatter3d(
            x=x_res, y=y_res, z=z_res,
            mode='markers+text',
            name='Active Site Residues',
            marker=dict(size=12, color=THEME_COLORS['success'], symbol='diamond'),
            text=labels,
            textposition="top center",
            hoverinfo='text'
        ))

    # 5. Docked Ligand Molecule Representation
    if toggles.get("Ligand", True):
        x_lig = [0.5, 1.2, 0.8, -0.4, -0.9, 0.1, 0.5]
        y_lig = [0.2, 0.8, 1.9, 1.5, 0.3, -0.8, 0.2]
        z_lig = [0.1, -0.5, 0.2, 0.7, 0.4, -0.2, 0.1]
        
        # Ligand bonds
        fig.add_trace(go.Scatter3d(
            x=x_lig, y=y_lig, z=z_lig,
            mode='lines+markers',
            name='Docked Ligand Pose',
            line=dict(color=THEME_COLORS['warning'], width=7),
            marker=dict(size=10, color=THEME_COLORS['warning']),
            hoverinfo='name'
        ))

    fig.update_layout(
        title=dict(text=f"Interactive 3D Docking Representation — Target {pdb_id}", font=dict(size=14, color=THEME_COLORS['text_main'])),
        scene=dict(
            xaxis=dict(showbackground=False, gridcolor="#1E293B", title="X (Å)"),
            yaxis=dict(showbackground=False, gridcolor="#1E293B", title="Y (Å)"),
            zaxis=dict(showbackground=False, gridcolor="#1E293B", title="Z (Å)"),
            bgcolor="#0A0F1A"
        ),
        paper_bgcolor=THEME_COLORS["card_bg"],
        font=dict(color=THEME_COLORS["text_main"]),
        margin=dict(l=0, r=0, t=30, b=0),
        height=520
    )
    return fig

def evaluate_lipinski_rule_of_five(candidate_row):
    """
    Evaluates Lipinski Rule of 5 parameters and returns PASS/FAIL status.
    Rules:
    - Molecular Weight < 500 Da
    - LogP < 5.0
    - H-Bond Donors <= 5
    - H-Bond Acceptors <= 10
    - Rotatable Bonds <= 10
    """
    mw = float(candidate_row.get("mw", 450.0))
    logp = float(candidate_row.get("logp", 2.5))
    hbd = int(candidate_row.get("hbd", 2))
    hba = int(candidate_row.get("hba", 6))
    rotb = int(candidate_row.get("rotb", 5))

    mw_pass = mw <= 500.0
    logp_pass = logp <= 5.0
    hbd_pass = hbd <= 5
    hba_pass = hba <= 10
    rotb_pass = rotb <= 10

    violations = sum([not mw_pass, not logp_pass, not hbd_pass, not hba_pass, not rotb_pass])
    overall_pass = violations <= 1  # 0 or 1 violation permitted in drug-like space

    return {
        "mw": {"val": round(mw, 2), "rule": "< 500 Da", "pass": mw_pass},
        "logp": {"val": round(logp, 2), "rule": "< 5.0", "pass": logp_pass},
        "hbd": {"val": hbd, "rule": "≤ 5", "pass": hbd_pass},
        "hba": {"val": hba, "rule": "≤ 10", "pass": hba_pass},
        "rotb": {"val": rotb, "rule": "≤ 10", "pass": rotb_pass},
        "violations": violations,
        "overall_pass": overall_pass,
        "status_label": "PASSED (Rule of 5)" if overall_pass else f"FAILED ({violations} Violations)"
    }

def predict_admet_prototype_scores(candidate_row):
    """
    Generates prototype ADMET risk predictions.
    IMPORTANT: Explicitly labeled as simulated/predicted values.
    """
    tox = float(candidate_row.get("toxicity", 0.15))
    sol = float(candidate_row.get("solubility", 0.75))
    act = float(candidate_row.get("activity", 0.85))
    
    # Prototype Toxicity risk level
    if tox < 0.18:
        tox_level = "LOW RISK"
        tox_color = THEME_COLORS["success"]
    elif tox < 0.28:
        tox_level = "MODERATE RISK"
        tox_color = THEME_COLORS["warning"]
    else:
        tox_level = "HIGH RISK"
        tox_color = THEME_COLORS["danger"]

    # Prototype Aqueous Solubility
    if sol > 0.70:
        sol_level = "HIGH (LogS > -3.0)"
        sol_color = THEME_COLORS["success"]
    elif sol > 0.50:
        sol_level = "MODERATE (LogS -4.5 to -3.0)"
        sol_color = THEME_COLORS["warning"]
    else:
        sol_level = "POOR (LogS < -4.5)"
        sol_color = THEME_COLORS["danger"]

    # Prototype GI Absorption
    gi_absorp = round(min(98.5, 65.0 + sol * 25.0 + (1.0 - tox) * 10.0), 1)
    
    # Prototype Metabolic Stability (Half-life t1/2)
    t_half = round(2.5 + act * 6.0 + sol * 2.0, 1)

    return {
        "toxicity": {"score": round(tox, 2), "level": tox_level, "color": tox_color},
        "solubility": {"score": round(sol, 2), "level": sol_level, "color": sol_color},
        "absorption": {"score": f"{gi_absorp}%", "level": "HIGH GI ABSORPTION" if gi_absorp > 75 else "MODERATE GI ABSORPTION"},
        "metabolic_stability": {"score": f"{t_half} hrs", "level": "STABLE (t½ > 4h)" if t_half > 4 else "MODERATE CLEARANCE"},
        "disclaimer": "Predicted / simulated prototype values — not clinical evidence."
    }
