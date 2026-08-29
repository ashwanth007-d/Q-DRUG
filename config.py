"""
Configuration and constants for Q-DRUG: Quantum-Assisted Drug Discovery Platform.
"""

APP_TITLE = "Q-DRUG"
APP_SUBTITLE = "Quantum-Assisted Drug Discovery & Lead Optimization Platform"
TAGLINE = "From Target Selection → Molecular Screening → Quantum Optimization → Lead Design"

# Color Palette (Futuristic Dark Biotech + Quantum Theme)
THEME_COLORS = {
    "background": "#0A0E17",
    "card_bg": "#12192A",
    "card_border": "#1E2A45",
    "primary": "#00F0FF",       # Quantum Cyan
    "secondary": "#8A2BE2",     # Deep Neon Purple
    "accent": "#FF007F",        # Vibrant Pink/Magenta
    "success": "#00FF88",       # Glowing Emerald Green
    "warning": "#FFB300",       # Amber
    "danger": "#FF3366",        # Neon Coral Red
    "text_main": "#E2E8F0",     # Off-white / Silver
    "text_muted": "#94A3B8",    # Muted Slate
    "highlight": "#38BDF8"
}

# Predefined Therapeutic Targets
PREDEFINED_TARGETS = {
    "EGFR Kinase T790M": {
        "pdb_id": "3W23",
        "name": "Epidermal Growth Factor Receptor Kinase (T790M Mutation)",
        "disease": "Non-Small Cell Lung Cancer (NSCLC)",
        "category": "Receptor Tyrosine Kinase / Oncology",
        "description": "Gatekeeper mutation T790M in EGFR kinase domain causing resistance to 1st/2nd generation TKIs. Targeted by covalent 3rd-gen inhibitors.",
        "active_residues": ["Met790", "Lys745", "Thr790", "Leu792", "Asp855"],
        "pocket_info": "ATP-binding cleft modified by bulky methionine gatekeeper residue.",
        "pocket_volume_text": "Pocket volume: Demo estimate / not experimentally validated",
        "pocket_volume_val": 915.0,
        "drugability_summary": "High drugability score (0.91). Targeted covalent binding pocket.",
        "default_ligand_name": "Osimertinib (CID 71496458)"
    },
    "BRAF V600E": {
        "pdb_id": "4S1Y",
        "name": "B-Raf Proto-Oncogene Serine/Threonine Kinase (V600E)",
        "disease": "Metastatic Melanoma & Colorectal Cancer",
        "category": "MAPK Pathway Kinase / Oncology",
        "description": "Valine-to-Glutamate oncogenic driver mutation at residue 600 locking BRAF into constitutively active monomeric kinase conformation.",
        "active_residues": ["Glu600", "Lys483", "Glu501", "Phe595", "Asp594"],
        "pocket_info": "ATP-binding cleft and DFG-out allosteric pocket.",
        "pocket_volume_text": "Pocket volume: Demo estimate / not experimentally validated",
        "pocket_volume_val": 880.0,
        "drugability_summary": "High drugability (0.94). Well-established ATP-competitive kinase target.",
        "default_ligand_name": "Vemurafenib (CID 42611257)"
    },
    "VEGFR2 Receptor": {
        "pdb_id": "4S15",
        "name": "Vascular Endothelial Growth Factor Receptor 2 (VEGFR2 / KDR)",
        "disease": "Tumor Angiogenesis & Solid Tumors",
        "category": "Angiogenesis Receptor / Oncology",
        "description": "Primary mediator of VEGF-driven tumor angiogenesis and vascular permeability. Key target for anti-angiogenic kinase inhibitors.",
        "active_residues": ["Glu885", "Lys868", "Cys919", "Asp1046", "Phe1047"],
        "pocket_info": "ATP-binding cleft and adjacent hydrophobic back pocket.",
        "pocket_volume_text": "Pocket volume: Demo estimate / not experimentally validated",
        "pocket_volume_val": 940.0,
        "drugability_summary": "High drugability (0.92). Hydrophobic back pocket supports Type-II inhibitors.",
        "default_ligand_name": "Axitinib (CID 6450551)"
    },
    "HER2 / ERBB2": {
        "pdb_id": "3RCD",
        "name": "Human Epidermal Growth Factor Receptor 2 (HER2 / ERBB2)",
        "disease": "HER2-Positive Breast Cancer & Gastric Cancer",
        "category": "Receptor Tyrosine Kinase / Oncology",
        "description": "Orphan receptor tyrosine kinase overexpressed in ~20% of breast cancers. Forms active heterodimers with EGFR and HER3.",
        "active_residues": ["Lys753", "Thr798", "Leu796", "Cys805", "Asp863"],
        "pocket_info": "Catalytic kinase domain with cysteine residue available for covalent coupling.",
        "pocket_volume_text": "Pocket volume: Demo estimate / not experimentally validated",
        "pocket_volume_val": 905.0,
        "drugability_summary": "High drugability (0.93). Target for dual EGFR/HER2 and selective HER2 inhibitors.",
        "default_ligand_name": "Tucatinib (CID 71496459)"
    },
    "SARS-CoV-2 Mpro": {
        "pdb_id": "6LU7",
        "name": "SARS-CoV-2 Main Protease (Mpro / 3CLpro)",
        "disease": "COVID-19 / Coronavirus Viral Infection",
        "category": "Viral Protease",
        "description": "Essential viral enzyme cleaving polyproteins during viral replication. Key therapeutic target for broad-spectrum coronavirus inhibitors.",
        "active_residues": ["His41", "Cys145", "Gly143", "Glu166"],
        "pocket_info": "Catalytic dyad Cys145-His41 in deep substrate binding cleft.",
        "pocket_volume_text": "Pocket volume: Demo estimate / not experimentally validated",
        "pocket_volume_val": 842.5,
        "drugability_summary": "High drugability score (0.88). Well-defined catalytic pocket with covalent coupling potential.",
        "default_ligand_name": "Nirmatrelvir (CID 155903259)"
    },
    "KRAS G12D": {
        "pdb_id": "7L10",
        "name": "KRAS Proto-Oncogene GTPase (G12D Mutation)",
        "disease": "Pancreatic, Colorectal & Lung Adenocarcinoma",
        "category": "Oncology / Small GTPase",
        "description": "Glycine-to-Aspartate point mutation at codon 12 locking KRAS into active GTP-bound signaling state.",
        "active_residues": ["Asp12", "Gly13", "Lys16", "Thr35", "Gln61"],
        "pocket_info": "Switch-II cryptic pocket adjacent to mutant Asp12 residue.",
        "pocket_volume_text": "Pocket volume: Demo estimate / not experimentally validated",
        "pocket_volume_val": 765.0,
        "drugability_summary": "High drugability (0.85). Unlocked via cryptic Switch-II pocket.",
        "default_ligand_name": "Adagrasib (CID 137452656)"
    },
    "Alzheimer's BACE1": {
        "pdb_id": "4B70",
        "name": "Beta-Secretase 1 (BACE1)",
        "disease": "Alzheimer's Disease & Neurodegeneration",
        "category": "Aspartyl Protease",
        "description": "Transmembrane aspartic protease responsible for cleavage of Amyloid Precursor Protein (APP) yielding toxic Amyloid-beta peptides.",
        "active_residues": ["Asp32", "Asp228", "Gly34", "Thr232", "Tyr71"],
        "pocket_info": "Large open catalytic cleft with catalytic dyad Asp32/Asp228.",
        "pocket_volume_text": "Pocket volume: Demo estimate / not experimentally validated",
        "pocket_volume_val": 1080.0,
        "drugability_summary": "Moderate drugability (0.75). Challenging large pocket requiring blood-brain barrier passage.",
        "default_ligand_name": "Verubecestat (CID 71732661)"
    }
}

# Scoring Formula Weights (Total = 1.0)
DEFAULT_SCORING_WEIGHTS = {
    "binding": 0.30,       # Binding affinity (pKd / log scale)
    "activity": 0.20,      # Biological activity estimate
    "druglikeness": 0.15,  # QED / Lipinski compliance score
    "solubility": 0.15,    # Aqueous solubility score (LogS converted)
    "toxicity_penalty": 0.10, # Toxicity penalty (1 - tox_risk)
    "quantum_score": 0.10  # VQE Ground state energy optimization bonus
}

# De-Novo Lead Modification Prototype Parameters
# IMPORTANT: These values are ONLY demonstration assumptions.
MODIFICATION_PROTOTYPES = {
    "Fluorination (-F)": {
        "delta_pkd": 0.45,
        "solubility_shift": -0.15,
        "toxicity_shift": -0.05,
        "description": "Adds lipophilic fluoromethyl group enhancing hydrophobic interaction with pocket side-chains."
    },
    "Amide Coupling (-CONH2)": {
        "delta_pkd": 0.32,
        "solubility_shift": +0.30,
        "toxicity_shift": 0.00,
        "description": "Introduces polar hydrogen bond donor/acceptor backbone enhancing solubility and hinge H-bonds."
    },
    "Hydroxylation (-OH)": {
        "delta_pkd": 0.25,
        "solubility_shift": +0.45,
        "toxicity_shift": -0.02,
        "description": "Appends hydroxyl group creating targeted hydrogen bonding with active-site catalytic residues."
    }
}

# Scientific Honesty Disclaimer Text
SCIENTIFIC_DISCLAIMER = (
    "DEMO ASSUMPTION & PREDICTIVE SCORES DISCLAIMER:\n"
    "Q-DRUG is a computational research prototype designed for hackathon demonstration. "
    "All ADMET values, VQE simulations, binding affinities, and chemical optimization delta values "
    "represent predictive/simulated prototype models and demonstration assumptions. "
    "They do NOT constitute experimental biological validation or clinical efficacy evidence."
)
