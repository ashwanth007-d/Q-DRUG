# Q-DRUG: Quantum-Assisted Drug Discovery & Lead Optimization Platform

**Q-DRUG** is a complete, hackathon-ready computational research platform that integrates classical cheminformatics, 3D molecular docking evaluation, simulated quantum variational eigensolvers (VQE), and de-novo chemical lead optimization into a unified futuristic web interface.

---

## 🧬 Key Platform Modules

1. **Target Receptor Hub**: Explore 4 therapeutic disease targets (SARS-CoV-2 Mpro, EGFR Kinase T790M, Alzheimer's BACE1, KRAS G12D) with active-site residue analysis and custom PDB retrieval.
2. **3D Docking Studio**: Interactive 3D molecular visualization with display toggles (Ribbon, Surface Pocket, Spacefill, Ligand, Active Residues), Lipinski Rule of Five PASS/FAIL panel, and ADMET prototype risk scores.
3. **Simulated VQE Engine**: Quantum computing centerpiece modeling electronic ground state energy optimization over 4–12 qubits with RealAmplitudes, UCCD, or HardwareEfficient ansatzes and live convergence animation.
4. **Virtual High-Throughput Screening (VHTS)**: Multi-objective candidate ranking on Pareto Frontiers (Binding Affinity vs Quantum Energy), 6-axis Radar comparison, and custom SMILES molecule input parser.
5. **De-Novo Lead Optimizer**: Chemical modification studio (-F, -CONH2, -OH) calculating thermodynamic binding free energy shifts $\Delta\Delta G \approx -RT \ln(10) \times \Delta pKd$ and active lead promotion.
6. **Judge Demo Tour + Report Export**: Interactive 4-step hackathon presentation walkthrough and executive scientific report generator printable to PDF.

---

## 🚀 Quick Start Guide

### Installed Dependencies
```bash
pip install streamlit pandas numpy scikit-learn plotly
```

### Running the Application
```bash
streamlit run app.py
```

---

## ⚠️ Scientific Honesty & Disclaimer

All computational outputs, simulated VQE runs, prototype ADMET scores, and lead optimization delta values represent **predictive / simulated prototype models and demonstration assumptions**. They do NOT constitute experimental biological validation or clinical efficacy evidence.

* **Simulated VQE**: Models quantum eigensolver optimization without claiming physical quantum advantage or physical hardware execution.
* **Graceful Fallbacks**: The platform operates seamlessly even when optional scientific packages (`rdkit`, `qiskit`, `py3Dmol`, `reportlab`) are unavailable.
