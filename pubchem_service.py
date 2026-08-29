"""
PubChem REST API Service & Caching Layer for Q-DRUG Platform.
Provides real-world compound data fetching from PubChem PUG REST API,
disk-based caching, and local dataset fallback for offline hackathon demonstration.
"""

import os
import json
import time
import urllib.request
import urllib.parse
import pandas as pd

CACHE_FILE = os.path.join("data", "pubchem_cache.json")
BACKUP_CSV = os.path.join("data", "real_pubchem_compounds.csv")

# Target Query Keywords for PubChem PUG REST Search
TARGET_SEARCH_QUERIES = {
    "EGFR Kinase T790M": ["EGFR inhibitor", "erlotinib", "gefitinib", "osimertinib", "lapatinib", "afatinib", "dacomitinib"],
    "BRAF V600E": ["BRAF inhibitor", "vemurafenib", "dabrafenib", "encorafenib", "sorafenib", "regorafenib"],
    "VEGFR2 Receptor": ["VEGFR2 inhibitor", "sunitinib", "axitinib", "lenvatinib", "pazopanib", "cabozantinib", "nintedanib"],
    "HER2 / ERBB2": ["HER2 inhibitor", "tucatinib", "lapatinib", "neratinib", "pyrotinib", "mubritinib"],
    "SARS-CoV-2 Mpro": ["Mpro inhibitor", "nirmatrelvir", "ensitrelvir", "lufotrelvir", "boceprevir", "paxlovid"],
    "KRAS G12D": ["KRAS inhibitor", "adagrasib", "sotorasib", "kras g12d"],
    "Alzheimer's BACE1": ["BACE1 inhibitor", "verubecestat", "atabecestat", "elenbecestat"]
}

def load_cache():
    """Loads JSON cache from disk if available."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_cache(cache_data):
    """Saves cache JSON to disk."""
    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, indent=2)
    except Exception as e:
        print(f"Warning: Failed to save PubChem cache: {e}")

def load_backup_dataset():
    """Loads pre-bundled real PubChem compounds dataset."""
    if os.path.exists(BACKUP_CSV):
        try:
            df = pd.read_csv(BACKUP_CSV)
            return df.to_dict(orient="records")
        except Exception as e:
            print(f"Warning: Could not read backup CSV: {e}")
    return []

def fetch_pubchem_compound_properties_by_cids(cid_list):
    """
    Fetches real compound molecular properties from PubChem PUG REST API for a list of CIDs.
    URL: https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cids}/property/Title,IUPACName,MolecularFormula,MolecularWeight,CanonicalSMILES,IsomericSMILES/JSON
    """
    if not cid_list:
        return []
        
    cids_str = ",".join(str(c) for c in cid_list[:50])
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cids_str}/property/Title,IUPACName,MolecularFormula,MolecularWeight,CanonicalSMILES,IsomericSMILES/JSON"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Q-DRUG/2.0'}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=2.5) as response:
            data = json.loads(response.read().decode('utf-8'))
            props = data.get("PropertyTable", {}).get("Properties", [])
            results = []
            for p in props:
                cid = p.get("CID")
                title = p.get("Title") or f"PubChem CID {cid}"
                formula = p.get("MolecularFormula", "Unknown")
                mw = float(p.get("MolecularWeight", 0.0))
                can_smiles = p.get("CanonicalSMILES") or p.get("IsomericSMILES", "")
                iso_smiles = p.get("IsomericSMILES") or can_smiles
                iupac = p.get("IUPACName") or title
                
                results.append({
                    "cid": int(cid),
                    "name": title,
                    "pubchem_cid": int(cid),
                    "formula": formula,
                    "mw": mw,
                    "smiles": can_smiles,
                    "canonical_smiles": can_smiles,
                    "isomeric_smiles": iso_smiles,
                    "iupac_name": iupac,
                    "structure_img": f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG",
                    "pubchem_url": f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}",
                    "data_source": "PubChem API (Live)"
                })
            return results
    except Exception as e:
        print(f"PubChem API property fetch error: {e}")
        return []

def search_pubchem_cids_by_name(query_term):
    """
    Searches PubChem CIDs matching a query term.
    URL: https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{query}/cids/JSON
    """
    clean_query = urllib.parse.quote(query_term.strip())
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{clean_query}/cids/JSON"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Q-DRUG/2.0'}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=2.0) as response:
            data = json.loads(response.read().decode('utf-8'))
            cids = data.get("IdentifierList", {}).get("CID", [])
            return cids
    except Exception as e:
        print(f"PubChem CID search error for '{query_term}': {e}")
        return []

def fetch_compounds_for_target(target_name, max_results=30):
    """
    Fetches real PubChem compounds for a specific therapeutic target.
    Implements:
    1. Online PubChem REST API Query
    2. Local JSON Cache lookup
    3. Pre-bundled Backup Dataset Fallback
    Returns: (compounds_list, data_source_label, status_message)
    """
    cache = load_cache()
    
    # 1. Check cache first
    cache_key = f"target_{target_name}"
    if cache_key in cache:
        cached_entry = cache[cache_key]
        # Use cache if retrieved within last 24h
        if time.time() - cached_entry.get("timestamp", 0) < 86400:
            records = cached_entry.get("records", [])
            if records:
                return records, "Local Cache (PubChem Records)", f"Loaded {len(records)} cached PubChem records."

    # 2. Try online PubChem fetch
    queries = TARGET_SEARCH_QUERIES.get(target_name, [target_name])
    all_cids = []
    
    for q in queries:
        cids = search_pubchem_cids_by_name(q)
        for c in cids:
            if c not in all_cids:
                all_cids.append(c)
        if len(all_cids) >= max_results:
            break
            
    if all_cids:
        records = fetch_pubchem_compound_properties_by_cids(all_cids[:max_results])
        if records:
            # Save to cache
            cache[cache_key] = {
                "timestamp": time.time(),
                "records": records
            }
            save_cache(cache)
            return records, "PubChem Live API", f"Retrieved {len(records)} real compounds from PubChem API."
            
    # 3. Fallback to pre-bundled local dataset
    backup_records = load_backup_dataset()
    filtered_backup = [r for r in backup_records if r.get("target") == target_name]
    
    if not filtered_backup and backup_records:
        filtered_backup = backup_records[:max_results]
        
    if filtered_backup:
        formatted_backup = []
        for r in filtered_backup:
            formatted_backup.append({
                "cid": int(r.get("pubchem_cid", 0)),
                "name": str(r.get("name", "Unknown Compound")),
                "pubchem_cid": int(r.get("pubchem_cid", 0)),
                "formula": str(r.get("formula", "Unknown")),
                "mw": float(r.get("mw", 400.0)),
                "smiles": str(r.get("canonical_smiles", r.get("smiles", ""))),
                "canonical_smiles": str(r.get("canonical_smiles", r.get("smiles", ""))),
                "isomeric_smiles": str(r.get("isomeric_smiles", r.get("smiles", ""))),
                "iupac_name": str(r.get("iupac_name", r.get("name", ""))),
                "structure_img": f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{r.get('pubchem_cid')}/PNG",
                "pubchem_url": f"https://pubchem.ncbi.nlm.nih.gov/compound/{r.get('pubchem_cid')}",
                "data_source": "Local Dataset (PubChem Fallback)"
            })
        return formatted_backup, "Local PubChem Dataset (Fallback)", f"Loaded {len(formatted_backup)} real PubChem fallback records."

    return [], "No Data Available", "Failed to retrieve compound data."
