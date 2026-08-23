"""
De-Novo Lead Optimizer Engine for Q-DRUG Platform.
Performs chemical modification simulation (-F, -CONH2, -OH), calculates thermodynamic delta delta G,
solubility & toxicity shifts, and updates candidate rankings.
"""

import math
import numpy as np
from config import MODIFICATION_PROTOTYPES, DEFAULT_SCORING_WEIGHTS
from demo_data import calculate_qdrug_score

# Universal Gas Constant R (kcal / mol * K) and Standard Temp T = 298.15 K
# RT * ln(10) ≈ 1.364 kcal/mol (or 5.708 kJ/mol)
RT_LN10_KCAL = 1.364
RT_LN10_KJ = 5.708

def calculate_thermodynamic_delta_g(delta_pkd):
    """
    Calculates thermodynamic binding free energy shift delta delta G from delta pKd using:
    ΔΔG ≈ -RT ln(10) × ΔpKd
    """
    ddg_kcal = -RT_LN10_KCAL * delta_pkd
    ddg_kj = -RT_LN10_KJ * delta_pkd
    return round(ddg_kcal, 2), round(ddg_kj, 2)

def optimize_lead_candidate(base_candidate, mod_name):
    """
    Applies chemical modification to base candidate, recalculating pKd, ΔΔG, properties,
    and Q-DRUG score delta.
    """
    mod_info = MODIFICATION_PROTOTYPES.get(mod_name, MODIFICATION_PROTOTYPES["Fluorination (-F)"])
    delta_pkd = mod_info["delta_pkd"]
    sol_shift = mod_info["solubility_shift"]
    tox_shift = mod_info["toxicity_shift"]
    
    # Calculate energy & property shifts
    orig_pkd = float(base_candidate["binding_affinity"])
    opt_pkd = round(orig_pkd + delta_pkd, 2)
    
    ddg_kcal, ddg_kj = calculate_thermodynamic_delta_g(delta_pkd)
    
    orig_sol = float(base_candidate.get("solubility", 0.70))
    opt_sol = round(np.clip(orig_sol + sol_shift, 0.1, 0.99), 2)
    
    orig_tox = float(base_candidate.get("toxicity", 0.18))
    opt_tox = round(np.clip(orig_tox + tox_shift, 0.02, 0.95), 2)
    
    # Quantum energy improvement bonus from enhanced binding configuration
    orig_qe = float(base_candidate.get("quantum_energy", -160.0))
    opt_qe = round(orig_qe - (delta_pkd * 12.5), 2)
    
    # Construct optimized candidate dict
    opt_candidate = base_candidate.copy()
    opt_candidate["candidate_id"] = f"{base_candidate['candidate_id']}-OPT"
    opt_candidate["name"] = f"{base_candidate['name']} + {mod_name.split(' ')[0]}"
    opt_candidate["binding_affinity"] = opt_pkd
    opt_candidate["quantum_energy"] = opt_qe
    opt_candidate["solubility"] = opt_sol
    opt_candidate["toxicity"] = opt_tox
    opt_candidate["activity"] = round(min(0.98, float(base_candidate.get("activity", 0.85)) + 0.04), 2)
    opt_candidate["data_type"] = "demonstration / lead optimized"
    
    # Recalculate SMILES representation
    orig_smiles = base_candidate.get("smiles", "C1=CC=CC=C1")
    if "Fluorination" in mod_name:
        opt_candidate["smiles"] = orig_smiles + "F"
    elif "Amide" in mod_name:
        opt_candidate["smiles"] = orig_smiles + "C(=O)N"
    elif "Hydroxylation" in mod_name:
        opt_candidate["smiles"] = orig_smiles + "O"
        
    orig_score = float(base_candidate.get("qdrug_score", calculate_qdrug_score(base_candidate)))
    opt_score = calculate_qdrug_score(opt_candidate)
    opt_candidate["qdrug_score"] = opt_score
    
    score_delta = round(opt_score - orig_score, 2)
    
    return {
        "base_candidate": base_candidate,
        "opt_candidate": opt_candidate,
        "mod_name": mod_name,
        "mod_info": mod_info,
        "delta_pkd": delta_pkd,
        "ddg_kcal": ddg_kcal,
        "ddg_kj": ddg_kj,
        "orig_pkd": orig_pkd,
        "opt_pkd": opt_pkd,
        "orig_sol": orig_sol,
        "opt_sol": opt_sol,
        "orig_tox": orig_tox,
        "opt_tox": opt_tox,
        "orig_score": orig_score,
        "opt_score": opt_score,
        "score_delta": score_delta,
        "formula_text": f"ΔΔG ≈ -RT ln(10) × ΔpKd = -1.364 × {delta_pkd:.2f} = {ddg_kcal:.2f} kcal/mol ({ddg_kj:.2f} kJ/mol)",
        "disclaimer": "Illustrative optimization parameters — not experimentally validated."
    }
