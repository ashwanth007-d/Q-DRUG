"""
Scientific Report Generator for Q-DRUG Platform.
Generates an executive scientific HTML report printable to PDF from browser or saveable as HTML.
Supports ReportLab when available with full fallback support.
"""

import os
import datetime
from config import APP_TITLE, APP_SUBTITLE, SCIENTIFIC_DISCLAIMER, THEME_COLORS

# Check ReportLab availability
HAS_REPORTLAB = False
try:
    import reportlab
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

def generate_scientific_html_report(target_info, candidate_row, lipinski_info, admet_info, vqe_results, vhts_top_df, lead_opt_results=None):
    """
    Generates a complete, styled HTML scientific report document printable directly to PDF.
    """
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    lead_opt_html = ""
    if lead_opt_results:
        lead_opt_html = f"""
        <div class="report-section">
            <h3>5. De-Novo Lead Optimization Results</h3>
            <p><b>Base Candidate:</b> {lead_opt_results['base_candidate']['name']} ({lead_opt_results['base_candidate']['candidate_id']})</p>
            <p><b>Chemical Modification Applied:</b> {lead_opt_results['mod_name']}</p>
            <table class="report-table">
                <tr><th>Metric</th><th>Original Lead</th><th>Optimized Lead</th><th>Shift / Delta</th></tr>
                <tr><td>Binding Affinity (pKd)</td><td>{lead_opt_results['orig_pkd']:.2f}</td><td><b>{lead_opt_results['opt_pkd']:.2f}</b></td><td><span style="color: #00FF88;">+{lead_opt_results['delta_pkd']:.2f} pKd</span></td></tr>
                <tr><td>Binding Free Energy (ΔΔG)</td><td>—</td><td><b>{lead_opt_results['ddg_kcal']:.2f} kcal/mol</b></td><td>{lead_opt_results['ddg_kj']:.2f} kJ/mol</td></tr>
                <tr><td>Solubility Score</td><td>{lead_opt_results['orig_sol']:.2f}</td><td><b>{lead_opt_results['opt_sol']:.2f}</b></td><td>{lead_opt_results['opt_sol'] - lead_opt_results['orig_sol']:+.2f}</td></tr>
                <tr><td>Toxicity Risk Score</td><td>{lead_opt_results['orig_tox']:.2f}</td><td><b>{lead_opt_results['opt_tox']:.2f}</b></td><td>{lead_opt_results['opt_tox'] - lead_opt_results['orig_tox']:+.2f}</td></tr>
                <tr><td>Q-DRUG Composite Score</td><td>{lead_opt_results['orig_score']:.2f}</td><td><b>{lead_opt_results['opt_score']:.2f}</b></td><td><span style="color: #00FF88;">+{lead_opt_results['score_delta']:.2f} pts</span></td></tr>
            </table>
            <p><i>Formula: {lead_opt_results['formula_text']}</i></p>
        </div>
        """

    top_vhts_rows = ""
    for idx, (_, row) in enumerate(vhts_top_df.head(6).iterrows(), 1):
        top_vhts_rows += f"""
        <tr>
            <td>{idx}</td>
            <td><b>{row['name']}</b> ({row['candidate_id']})</td>
            <td>{row['binding_affinity']:.2f}</td>
            <td>{row['quantum_energy']:.2f}</td>
            <td>{row['activity']:.2f}</td>
            <td>{row['toxicity']:.2f}</td>
            <td><b>{row['qdrug_score']:.2f}</b></td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Q-DRUG Executive Scientific Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
            background-color: #ffffff;
            color: #1e293b;
            line-height: 1.6;
            margin: 0;
            padding: 40px;
        }}
        .report-header {{
            border-bottom: 3px solid #00f0ff;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .report-header h1 {{
            margin: 0;
            font-size: 28px;
            color: #0f172a;
        }}
        .report-header .sub {{
            color: #64748b;
            font-size: 14px;
            margin-top: 5px;
        }}
        .report-section {{
            margin-bottom: 35px;
            page-break-inside: avoid;
        }}
        .report-section h3 {{
            border-left: 4px solid #7000ff;
            padding-left: 10px;
            font-size: 18px;
            color: #0f172a;
            margin-bottom: 12px;
        }}
        .report-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            font-size: 13px;
        }}
        .report-table th, .report-table td {{
            border: 1px solid #cbd5e1;
            padding: 8px 12px;
            text-align: left;
        }}
        .report-table th {{
            background-color: #f1f5f9;
            color: #334155;
            font-weight: 600;
        }}
        .card-box {{
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 15px;
            margin-top: 10px;
        }}
        .disclaimer-box {{
            background-color: #fffbeb;
            border: 1px solid #f59e0b;
            border-radius: 6px;
            padding: 15px;
            font-size: 12px;
            color: #b45309;
            margin-top: 30px;
        }}
        @media print {{
            body {{ padding: 0; }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>

    <div class="no-print" style="margin-bottom: 20px; text-align: right;">
        <button onclick="window.print()" style="background: #00f0ff; color: #0f172a; border: none; padding: 10px 20px; font-weight: bold; border-radius: 5px; cursor: pointer;">
            🖨️ Print / Save to PDF
        </button>
    </div>

    <div class="report-header">
        <h1>{APP_TITLE}: Quantum-Assisted Drug Discovery Report</h1>
        <div class="sub">{APP_SUBTITLE} | Generated: {now_str}</div>
    </div>

    <div class="report-section">
        <h3>1. Target Receptor Profile</h3>
        <div class="card-box">
            <p><b>Target Name:</b> {target_info.get('name', 'SARS-CoV-2 Mpro')}</p>
            <p><b>PDB Identifier:</b> <code style="background:#e2e8f0; padding:2px 6px; border-radius:4px;">{target_info.get('pdb_id', '6LU7')}</code></p>
            <p><b>Disease / Indication:</b> {target_info.get('disease', 'Viral Protease')}</p>
            <p><b>Binding Pocket Volume:</b> {target_info.get('pocket_volume_text', 'Demo estimate')} ({target_info.get('pocket_volume_val', 842.5)} Å³)</p>
            <p><b>Active Site Residues:</b> {", ".join(target_info.get('active_residues', ['His41', 'Cys145']))}</p>
        </div>
    </div>

    <div class="report-section">
        <h3>2. Top Candidate & Lipinski Rule of 5 Evaluation</h3>
        <p><b>Candidate Molecule:</b> {candidate_row.get('name', 'Nirmatrelvir-Q1')} (ID: {candidate_row.get('candidate_id', 'QD-101')})</p>
        <p><b>SMILES:</b> <code style="font-size:11px;">{candidate_row.get('smiles', '')}</code></p>
        <table class="report-table">
            <tr><th>Property</th><th>Value</th><th>Lipinski Threshold</th><th>Status</th></tr>
            <tr><td>Molecular Weight (MW)</td><td>{lipinski_info['mw']['val']} Da</td><td>&lt; 500 Da</td><td>{"PASS" if lipinski_info['mw']['pass'] else "FAIL"}</td></tr>
            <tr><td>LogP (Lipophilicity)</td><td>{lipinski_info['logp']['val']}</td><td>&lt; 5.0</td><td>{"PASS" if lipinski_info['logp']['pass'] else "FAIL"}</td></tr>
            <tr><td>H-Bond Donors (HBD)</td><td>{lipinski_info['hbd']['val']}</td><td>&le; 5</td><td>{"PASS" if lipinski_info['hbd']['pass'] else "FAIL"}</td></tr>
            <tr><td>H-Bond Acceptors (HBA)</td><td>{lipinski_info['hba']['val']}</td><td>&le; 10</td><td>{"PASS" if lipinski_info['hba']['pass'] else "FAIL"}</td></tr>
            <tr><td>Rotatable Bonds (RotB)</td><td>{lipinski_info['rotb']['val']}</td><td>&le; 10</td><td>{"PASS" if lipinski_info['rotb']['pass'] else "FAIL"}</td></tr>
        </table>
        <p><b>Overall Lipinski Rule:</b> <b>{lipinski_info['status_label']}</b></p>
    </div>

    <div class="report-section">
        <h3>3. Prototype ADMET Risk Profile</h3>
        <table class="report-table">
            <tr><th>ADMET Dimension</th><th>Predicted Value</th><th>Prototype Risk Level</th></tr>
            <tr><td>Toxicity Risk</td><td>{admet_info['toxicity']['score']}</td><td>{admet_info['toxicity']['level']}</td></tr>
            <tr><td>Solubility (LogS)</td><td>{admet_info['solubility']['score']}</td><td>{admet_info['solubility']['level']}</td></tr>
            <tr><td>GI Absorption</td><td>{admet_info['absorption']['score']}</td><td>{admet_info['absorption']['level']}</td></tr>
            <tr><td>Metabolic Stability (t½)</td><td>{admet_info['metabolic_stability']['score']}</td><td>{admet_info['metabolic_stability']['level']}</td></tr>
        </table>
        <p><i>Note: {admet_info['disclaimer']}</i></p>
    </div>

    <div class="report-section">
        <h3>4. Simulated VQE Quantum Ground State Engine Summary</h3>
        <div class="card-box">
            <p><b>Configured Qubits:</b> {vqe_results.get('qubits', 6)} Qubits</p>
            <p><b>Variational Ansatz:</b> {vqe_results.get('ansatz', 'RealAmplitudes')}</p>
            <p><b>Classical Optimizer:</b> {vqe_results.get('optimizer', 'SPSA')}</p>
            <p><b>Noise Model:</b> {vqe_results.get('noise_model', 'Ideal')}</p>
            <p><b>Initial Electronic Energy:</b> {vqe_results.get('initial_energy', -120.0)} Hartree</p>
            <p><b>Optimized Ground State Energy:</b> <b>{vqe_results.get('final_energy', -145.32)} Hartree</b></p>
            <p><b>Energy Improvement (ΔE):</b> <span style="color:green; font-weight:bold;">{vqe_results.get('improvement', 25.32)} Hartree</span></p>
            <p><i>Status: {vqe_results.get('disclaimer', 'SIMULATED VQE')}</i></p>
        </div>
    </div>

    {lead_opt_html}

    <div class="report-section">
        <h3>6. VHTS Top Candidates Ranking</h3>
        <table class="report-table">
            <tr><th>Rank</th><th>Candidate Name</th><th>Binding (pKd)</th><th>Quantum E (Ha)</th><th>Activity</th><th>Toxicity</th><th>Q-DRUG Score</th></tr>
            {top_vhts_rows}
        </table>
    </div>

    <div class="disclaimer-box">
        <b>SCIENTIFIC HONESTY & RESEARCH DISCLAIMER:</b><br/>
        {SCIENTIFIC_DISCLAIMER}
    </div>

</body>
</html>
"""
    return html_content
