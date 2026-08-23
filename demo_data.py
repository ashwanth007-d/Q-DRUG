"""
Demo Data Generator for Q-DRUG Platform.
Generates candidate molecules database with clear demonstration data markers.
"""

import os
import pandas as pd
import numpy as np

# Sample dataset of 25 therapeutic candidate molecules with SMILES and baseline properties
INITIAL_CANDIDATES = [
    {
        "candidate_id": "QD-101",
        "name": "Nirmatrelvir-Q1",
        "target": "SARS-CoV-2 Mpro",
        "smiles": "CC1(C2C1C(N(C2)C(=O)C(C(C)(C)C)NC(=O)C(F)(F)F)C(=O)NC(CC3CCNC3=O)C#N)C",
        "binding_affinity": 8.85,
        "quantum_energy": -145.32,
        "activity": 0.92,
        "toxicity": 0.12,
        "solubility": 0.81,
        "druglikeness": 0.88,
        "mw": 499.53,
        "logp": 1.85,
        "hbd": 3,
        "hba": 7,
        "rotb": 6,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-102",
        "name": "Osimertinib-Q2",
        "target": "EGFR Kinase T790M",
        "smiles": "CN1CCN(CC1)C2=CC(=C(C=C2)NC(=O)C=C)NC3=NC=CC(=N3)C4=CN(C5=CC=CC=C54)C",
        "binding_affinity": 9.15,
        "quantum_energy": -210.65,
        "activity": 0.95,
        "toxicity": 0.18,
        "solubility": 0.74,
        "druglikeness": 0.91,
        "mw": 499.61,
        "logp": 3.42,
        "hbd": 2,
        "hba": 8,
        "rotb": 7,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-103",
        "name": "Verubecestat-Q3",
        "target": "Alzheimer's BACE1",
        "smiles": "CC1(N=C(NC1=O)N)C2=C(C=CC(=C2)NC(=O)C3=NC=C(C=C3)C(F)(F)F)F",
        "binding_affinity": 8.40,
        "quantum_energy": -188.40,
        "activity": 0.86,
        "toxicity": 0.15,
        "solubility": 0.78,
        "druglikeness": 0.85,
        "mw": 409.34,
        "logp": 2.10,
        "hbd": 3,
        "hba": 6,
        "rotb": 3,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-104",
        "name": "MRTX-G12D-Q4",
        "target": "KRAS G12D",
        "smiles": "CN1CCN(CC1)C2=CC=C(C=C2)C3=C4C=C(C=CC4=NC(=N3)NC5=CC=C(C=C5)F)N",
        "binding_affinity": 9.05,
        "quantum_energy": -195.80,
        "activity": 0.93,
        "toxicity": 0.14,
        "solubility": 0.72,
        "druglikeness": 0.89,
        "mw": 468.53,
        "logp": 3.15,
        "hbd": 2,
        "hba": 6,
        "rotb": 5,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-105",
        "name": "Cov-Protease-Inh-A",
        "target": "SARS-CoV-2 Mpro",
        "smiles": "CC(C)CC(C(=O)NC(C1CCCCC1)C(=O)NC#N)NC(=O)OCC2=CC=CC=C2",
        "binding_affinity": 7.95,
        "quantum_energy": -120.15,
        "activity": 0.80,
        "toxicity": 0.22,
        "solubility": 0.68,
        "druglikeness": 0.82,
        "mw": 443.54,
        "logp": 2.90,
        "hbd": 3,
        "hba": 5,
        "rotb": 8,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-106",
        "name": "Gefitinib-V2",
        "target": "EGFR Kinase T790M",
        "smiles": "COC1=C(C=C2C(=C1)N=CN=C2NC3=CC(=C(C=C3)F)Cl)OCCCN4CCOCC4",
        "binding_affinity": 7.80,
        "quantum_energy": -175.20,
        "activity": 0.78,
        "toxicity": 0.25,
        "solubility": 0.65,
        "druglikeness": 0.84,
        "mw": 446.90,
        "logp": 3.20,
        "hbd": 1,
        "hba": 7,
        "rotb": 7,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-107",
        "name": "Atabecestat-A",
        "target": "Alzheimer's BACE1",
        "smiles": "CC1(N=C(NC1=O)N)C2=C(C=CC(=C2)NC(=O)C3=CN=CC(=C3)F)F",
        "binding_affinity": 8.10,
        "quantum_energy": -165.75,
        "activity": 0.83,
        "toxicity": 0.19,
        "solubility": 0.75,
        "druglikeness": 0.87,
        "mw": 359.31,
        "logp": 1.75,
        "hbd": 3,
        "hba": 5,
        "rotb": 3,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-108",
        "name": "Sotorasib-K2",
        "target": "KRAS G12D",
        "smiles": "CC1=C(C=C(C=C1)C2=C3C(=NC(=N2)N4CCCC4C#N)C=CC(=O)N3C)F",
        "binding_affinity": 8.65,
        "quantum_energy": -182.30,
        "activity": 0.89,
        "toxicity": 0.16,
        "solubility": 0.70,
        "druglikeness": 0.88,
        "mw": 424.47,
        "logp": 2.85,
        "hbd": 0,
        "hba": 6,
        "rotb": 3,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-109",
        "name": "Ritonav-Mpro-Lead",
        "target": "SARS-CoV-2 Mpro",
        "smiles": "CC(C)C1=NC(=CS1)CN(C)C(=O)NC(C(C)C)C(=O)NC(CC2=CC=CC=C2)CC(C(CC3=CC=CC=C3)NC(=O)OCC4=CN=CS4)O",
        "binding_affinity": 8.25,
        "quantum_energy": -240.10,
        "activity": 0.85,
        "toxicity": 0.30,
        "solubility": 0.55,
        "druglikeness": 0.65,
        "mw": 720.95,
        "logp": 4.80,
        "hbd": 4,
        "hba": 9,
        "rotb": 18,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-110",
        "name": "Erlotinib-E3",
        "target": "EGFR Kinase T790M",
        "smiles": "COCCOC1=C(C=C2C(=C1)C(=NC=N2)NC3=CC=CC(=C3)C#C)OCCOC",
        "binding_affinity": 7.50,
        "quantum_energy": -160.40,
        "activity": 0.75,
        "toxicity": 0.20,
        "solubility": 0.80,
        "druglikeness": 0.86,
        "mw": 393.44,
        "logp": 2.70,
        "hbd": 1,
        "hba": 6,
        "rotb": 8,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-111",
        "name": "Elenbecestat-B2",
        "target": "Alzheimer's BACE1",
        "smiles": "CC1(N=C(NC1=O)N)C2=CC(=CC=C2)C3=CN=C(C=C3)C(F)(F)F",
        "binding_affinity": 8.00,
        "quantum_energy": -150.90,
        "activity": 0.81,
        "toxicity": 0.17,
        "solubility": 0.73,
        "druglikeness": 0.85,
        "mw": 341.32,
        "logp": 1.95,
        "hbd": 3,
        "hba": 4,
        "rotb": 2,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-112",
        "name": "Adagrasib-K12",
        "target": "KRAS G12D",
        "smiles": "CC(C)N1CCN(CC1)C2=NC=NC3=C2C=C(C=C3)C4=C(C=CC=C4Cl)Cl",
        "binding_affinity": 8.80,
        "quantum_energy": -205.10,
        "activity": 0.90,
        "toxicity": 0.21,
        "solubility": 0.65,
        "druglikeness": 0.83,
        "mw": 427.37,
        "logp": 3.90,
        "hbd": 0,
        "hba": 5,
        "rotb": 4,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-113",
        "name": "Ensitrelvir-M1",
        "target": "SARS-CoV-2 Mpro",
        "smiles": "CC1=CN=C(C(=N1)NC2=CC(=CC=C2)F)C3=CN(N=C3)CC4=CC=C(C=C4)F",
        "binding_affinity": 8.70,
        "quantum_energy": -170.80,
        "activity": 0.91,
        "toxicity": 0.10,
        "solubility": 0.82,
        "druglikeness": 0.90,
        "mw": 403.39,
        "logp": 2.65,
        "hbd": 1,
        "hba": 6,
        "rotb": 5,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-114",
        "name": "Brigatinib-E4",
        "target": "EGFR Kinase T790M",
        "smiles": "CN1CCN(CC1)C2=CC=C(C=C2)NC3=NC=C(C(=N3)Cl)C4=C(C=CC=C4P(=O)(C)C)Cl",
        "binding_affinity": 8.90,
        "quantum_energy": -225.40,
        "activity": 0.92,
        "toxicity": 0.24,
        "solubility": 0.60,
        "druglikeness": 0.79,
        "mw": 584.05,
        "logp": 3.75,
        "hbd": 1,
        "hba": 6,
        "rotb": 6,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-115",
        "name": "Lanabecestat-L1",
        "target": "Alzheimer's BACE1",
        "smiles": "CC1(N=C(NC1=O)N)C2=CC(=CC=C2)C3=CN=C(C=C3)C#N",
        "binding_affinity": 7.75,
        "quantum_energy": -140.25,
        "activity": 0.77,
        "toxicity": 0.13,
        "solubility": 0.85,
        "druglikeness": 0.89,
        "mw": 298.32,
        "logp": 1.45,
        "hbd": 3,
        "hba": 4,
        "rotb": 2,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-116",
        "name": "K-Ras-Binder-X7",
        "target": "KRAS G12D",
        "smiles": "CC1=C(C=CC=C1)C2=NC(=NC=C2)NC3=CC=C(C=C3)S(=O)(=O)N",
        "binding_affinity": 7.45,
        "quantum_energy": -135.60,
        "activity": 0.74,
        "toxicity": 0.18,
        "solubility": 0.79,
        "druglikeness": 0.86,
        "mw": 341.40,
        "logp": 2.10,
        "hbd": 2,
        "hba": 5,
        "rotb": 4,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-117",
        "name": "Lufotrelvir-L2",
        "target": "SARS-CoV-2 Mpro",
        "smiles": "CC(C)CC(C(=O)NC(C1CCCCC1)C(=O)NC(C2CCNC2=O)C#N)NC(=O)OCC3=CC=CC=C3",
        "binding_affinity": 8.55,
        "quantum_energy": -180.90,
        "activity": 0.88,
        "toxicity": 0.15,
        "solubility": 0.77,
        "druglikeness": 0.87,
        "mw": 512.65,
        "logp": 2.60,
        "hbd": 3,
        "hba": 6,
        "rotb": 10,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-118",
        "name": "Dacomitinib-D1",
        "target": "EGFR Kinase T790M",
        "smiles": "COC1=C(C=C2C(=C1)N=CN=C2NC3=CC(=C(C=C3)F)Cl)OCC=CC(=O)N4CCCC4",
        "binding_affinity": 8.30,
        "quantum_energy": -198.70,
        "activity": 0.84,
        "toxicity": 0.28,
        "solubility": 0.62,
        "druglikeness": 0.81,
        "mw": 469.94,
        "logp": 3.65,
        "hbd": 1,
        "hba": 6,
        "rotb": 8,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-119",
        "name": "BACE-Inhibitor-CX",
        "target": "Alzheimer's BACE1",
        "smiles": "CC1(C2=CC(=CC=C2)C3=CN=CC=C3)N=C(NC1=O)N",
        "binding_affinity": 7.60,
        "quantum_energy": -132.10,
        "activity": 0.76,
        "toxicity": 0.11,
        "solubility": 0.88,
        "druglikeness": 0.91,
        "mw": 281.31,
        "logp": 1.30,
        "hbd": 3,
        "hba": 3,
        "rotb": 2,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-120",
        "name": "KRAS-SwitchII-S9",
        "target": "KRAS G12D",
        "smiles": "CN1CCN(CC1)C2=C(C=C(C=C2)Cl)C3=NC(=NC=C3)NC4=CC=C(C=C4)F",
        "binding_affinity": 8.20,
        "quantum_energy": -168.30,
        "activity": 0.82,
        "toxicity": 0.19,
        "solubility": 0.71,
        "druglikeness": 0.85,
        "mw": 412.87,
        "logp": 3.40,
        "hbd": 1,
        "hba": 5,
        "rotb": 4,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-121",
        "name": "Boceprevir-M2",
        "target": "SARS-CoV-2 Mpro",
        "smiles": "CC(C)(C)NC(=O)C1C2CC3C(C2)C31C(=O)NC(C(C(C)(C)C)NC(=O)NC(C)(C)C)C(=O)C(=O)N",
        "binding_affinity": 7.30,
        "quantum_energy": -155.00,
        "activity": 0.72,
        "toxicity": 0.26,
        "solubility": 0.66,
        "druglikeness": 0.75,
        "mw": 519.68,
        "logp": 2.45,
        "hbd": 4,
        "hba": 5,
        "rotb": 9,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-122",
        "name": "Afatinib-A3",
        "target": "EGFR Kinase T790M",
        "smiles": "CN(C)CC=CC(=O)NC1=C(C=C2C(=C1)N=CN=C2NC3=CC(=C(C=C3)Cl)F)OCC4CCOC4",
        "binding_affinity": 8.60,
        "quantum_energy": -215.80,
        "activity": 0.87,
        "toxicity": 0.27,
        "solubility": 0.64,
        "druglikeness": 0.80,
        "mw": 485.94,
        "logp": 3.30,
        "hbd": 1,
        "hba": 7,
        "rotb": 8,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-123",
        "name": "Umibecestat-U1",
        "target": "Alzheimer's BACE1",
        "smiles": "CC1(N=C(NC1=O)N)C2=C(C=CC(=C2)NC(=O)C3=CN=C(C=C3)C(F)F)F",
        "binding_affinity": 8.25,
        "quantum_energy": -162.40,
        "activity": 0.85,
        "toxicity": 0.14,
        "solubility": 0.79,
        "druglikeness": 0.88,
        "mw": 377.31,
        "logp": 1.80,
        "hbd": 3,
        "hba": 5,
        "rotb": 3,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-124",
        "name": "KRAS-G12D-Lead-99",
        "target": "KRAS G12D",
        "smiles": "CC1=CC=C(C=C1)C2=NC(=NC=C2)N3CCN(CC3)C4=CC=CC=C4F",
        "binding_affinity": 8.75,
        "quantum_energy": -189.50,
        "activity": 0.89,
        "toxicity": 0.16,
        "solubility": 0.76,
        "druglikeness": 0.87,
        "mw": 390.46,
        "logp": 3.10,
        "hbd": 0,
        "hba": 5,
        "rotb": 3,
        "data_type": "demonstration"
    },
    {
        "candidate_id": "QD-125",
        "name": "Paxlovid-Analog-X",
        "target": "SARS-CoV-2 Mpro",
        "smiles": "CC1(C2C1C(N(C2)C(=O)C(C(C)(C)C)NC(=O)C(F)F)C(=O)NC(CC3CCNC3=O)C#N)C",
        "binding_affinity": 8.95,
        "quantum_energy": -152.10,
        "activity": 0.94,
        "toxicity": 0.11,
        "solubility": 0.84,
        "druglikeness": 0.90,
        "mw": 481.54,
        "logp": 1.70,
        "hbd": 3,
        "hba": 6,
        "rotb": 6,
        "data_type": "demonstration"
    }
]

def calculate_qdrug_score(row, weights=None):
    """
    Calculates multi-factor Q-DRUG score:
    Weighted combination of binding affinity, activity, druglikeness, solubility,
    1 - toxicity penalty, and normalized quantum energy optimization bonus.
    """
    if weights is None:
        from config import DEFAULT_SCORING_WEIGHTS
        weights = DEFAULT_SCORING_WEIGHTS
    
    # Normalize binding affinity (typical range 5.0 to 10.0 -> 0.0 to 1.0)
    norm_binding = np.clip((row["binding_affinity"] - 5.0) / 5.0, 0.0, 1.0)
    
    # Activity, druglikeness, solubility are already 0..1
    act = float(row.get("activity", 0.5))
    dl = float(row.get("druglikeness", 0.5))
    sol = float(row.get("solubility", 0.5))
    
    # Toxicity penalty (1.0 = safe, 0.0 = toxic)
    tox = float(row.get("toxicity", 0.2))
    tox_safety = np.clip(1.0 - tox, 0.0, 1.0)
    
    # Quantum energy bonus (more negative quantum ground state energy is better optimization)
    # Range typically -300 to -100 Hartree
    qe = float(row.get("quantum_energy", -150.0))
    norm_quantum = np.clip((-qe - 100.0) / 200.0, 0.0, 1.0)
    
    score = (
        weights["binding"] * norm_binding +
        weights["activity"] * act +
        weights["druglikeness"] * dl +
        weights["solubility"] * sol +
        weights["toxicity_penalty"] * tox_safety +
        weights["quantum_score"] * norm_quantum
    ) * 100.0
    
    return round(float(score), 2)

def generate_csv_if_missing(csv_path="data/drugs.csv"):
    """
    Generates data/drugs.csv if it does not exist.
    """
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df = pd.DataFrame(INITIAL_CANDIDATES)
    df["qdrug_score"] = df.apply(calculate_qdrug_score, axis=1)
    df.to_csv(csv_path, index=False)
    return df

if __name__ == "__main__":
    df = generate_csv_if_missing()
    print(f"Generated demo dataset with {len(df)} candidate molecules.")
