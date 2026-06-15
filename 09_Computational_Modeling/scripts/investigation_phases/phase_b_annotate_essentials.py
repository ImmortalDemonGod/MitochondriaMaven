"""
Phase B.1 — Annotate all 145 mouse essential genes via MyGene.info API.

Produces essential_genes_annotated.csv with:
  ensembl_id, gene_symbol, full_name, uniprot_id,
  GO biological process, molecular function, cellular component,
  OMIM/disease associations (from disease_associations field if present)

MyGene.info is free, no API key required. Rate-limited to ~1000 req/hr.
"""

import sys
from pathlib import Path
# Bootstrap: locate paths.py walking up the directory tree
_here = Path(__file__).resolve().parent
for _p in [_here, _here.parent, _here.parent.parent, _here.parent.parent.parent]:
    if (_p / "paths.py").exists():
        if str(_p) not in sys.path:
            sys.path.insert(0, str(_p))
        break
from paths import MODEL_PATH, RESULTS_DIR, SUPP_TABLE_PATH, MITOMAMMAL_DIR, results_path



import json
import time
import os
import requests
import pandas as pd

ESSENTIALS_PATH = results_path("phase_b", "essential_dispensable_partition.json")
KO_SCORES_PATH = results_path("phase_b", "gene_knockout_scores_v2.csv")
OUT_PATH = results_path("phase_b", "essential_genes_annotated.csv")

MYGENE_BATCH_URL = "https://mygene.info/v3/gene"


def annotate_batch(ensembl_ids, species='mouse', batch_size=50):
    """Batch annotate a list of Ensembl mouse IDs via MyGene.info."""
    records = []
    for i in range(0, len(ensembl_ids), batch_size):
        batch = ensembl_ids[i:i + batch_size]
        print(f"  Batch {i//batch_size + 1}: {len(batch)} IDs ...", end=' ', flush=True)

        params = {
            'q': ','.join(batch),
            'scopes': 'ensembl.gene',
            'species': species,
            'fields': ('symbol,name,alias,uniprot.Swiss-Prot,'
                       'go.BP.term,go.MF.term,go.CC.term,'
                       'pathway.kegg.name,pathway.reactome.name,'
                       'summary,generif,interpro.short_desc,'
                       'pfam,MIM,disease_ontology,uniprot.subcellular_locations'),
            'size': 1,
        }

        try:
            r = requests.post(MYGENE_BATCH_URL, json={
                'ids': ','.join(batch),
                'scopes': 'ensembl.gene',
                'species': species,
                'fields': params['fields'],
            }, timeout=30)
            r.raise_for_status()
            data = r.json()
            print(f"got {len(data)} results")
            for entry in data:
                records.append(entry)
        except Exception as e:
            print(f"ERROR: {e}")
            for b in batch:
                records.append({'query': b, 'error': str(e)})

        time.sleep(0.5)  # be polite

    return records


def _safe_get(d, *keys, default=''):
    """Nested dict get with sensible default."""
    for k in keys:
        if d is None:
            return default
        if isinstance(d, list) and d:
            d = d[0]
        if isinstance(d, dict):
            d = d.get(k)
    return d if d is not None else default


def go_terms(entry, category):
    """Extract list of GO terms for BP/MF/CC."""
    go = entry.get('go', {})
    if not isinstance(go, dict):
        return ''
    cat = go.get(category, [])
    if isinstance(cat, dict):
        cat = [cat]
    return '; '.join([g.get('term', '') for g in cat[:5] if isinstance(g, dict)])


def main():
    with open(ESSENTIALS_PATH) as f:
        partition = json.load(f)
    essential_ids = partition['essential_mouse_genes']
    print(f"Annotating {len(essential_ids)} essential mouse genes")

    records = annotate_batch(essential_ids, species='mouse')

    # Join with KO impact data
    ko_df = pd.read_csv(KO_SCORES_PATH)
    ko_map = {row['gene_id']: row for _, row in ko_df.iterrows()}

    rows = []
    for entry in records:
        query = entry.get('query', '')
        if entry.get('notfound'):
            rows.append({
                'ensembl_id': query,
                'found': False,
                'gene_symbol': '',
                'full_name': '',
                'uniprot': '',
                'GO_biological_process': '',
                'GO_molecular_function': '',
                'GO_cellular_component': '',
                'kegg_pathways': '',
                'reactome_pathways': '',
                'omim': '',
                'subcellular_location': '',
                'pfam_domains': '',
                'summary': '',
                'atp_impact_pct': ko_map.get(query, {}).get('atp_impact_pct', 0),
                'complex': ko_map.get(query, {}).get('complex', 'Other'),
            })
            continue

        # Extract fields
        symbol = entry.get('symbol', '')
        name = entry.get('name', '')
        uniprot = _safe_get(entry, 'uniprot', 'Swiss-Prot', default='')
        if isinstance(uniprot, list):
            uniprot = uniprot[0] if uniprot else ''

        bp = go_terms(entry, 'BP')
        mf = go_terms(entry, 'MF')
        cc = go_terms(entry, 'CC')

        kegg = entry.get('pathway', {}).get('kegg', [])
        if isinstance(kegg, dict):
            kegg = [kegg]
        kegg_str = '; '.join([k.get('name', '') for k in kegg[:3] if isinstance(k, dict)])

        reactome = entry.get('pathway', {}).get('reactome', [])
        if isinstance(reactome, dict):
            reactome = [reactome]
        reactome_str = '; '.join([k.get('name', '') for k in reactome[:3] if isinstance(k, dict)])

        mim = entry.get('MIM', '')
        if isinstance(mim, list):
            mim = '; '.join(map(str, mim[:3]))

        subloc = entry.get('uniprot', {})
        if isinstance(subloc, list):
            subloc = subloc[0] if subloc else {}
        subloc = subloc.get('subcellular_locations', '') if isinstance(subloc, dict) else ''
        if isinstance(subloc, list):
            subloc = '; '.join(str(s) for s in subloc[:3])

        pfam = entry.get('pfam', [])
        if isinstance(pfam, dict):
            pfam = [pfam]
        elif isinstance(pfam, str):
            pfam = [{'id': pfam}]
        pfam_str = '; '.join([p.get('id', '') if isinstance(p, dict) else str(p) for p in pfam[:3]])

        summary = entry.get('summary', '')[:300]

        ko_data = ko_map.get(query, {})

        rows.append({
            'ensembl_id': query,
            'found': True,
            'gene_symbol': symbol,
            'full_name': name,
            'uniprot': uniprot if isinstance(uniprot, str) else '',
            'GO_biological_process': bp,
            'GO_molecular_function': mf,
            'GO_cellular_component': cc,
            'kegg_pathways': kegg_str,
            'reactome_pathways': reactome_str,
            'omim': str(mim)[:200],
            'subcellular_location': str(subloc)[:200],
            'pfam_domains': pfam_str,
            'summary': summary,
            'atp_impact_pct': ko_data.get('atp_impact_pct', 0),
            'complex': ko_data.get('complex', 'Other'),
        })

    df = pd.DataFrame(rows)
    df = df.sort_values('atp_impact_pct', ascending=False)
    df.to_csv(OUT_PATH, index=False)

    found_count = df['found'].sum()
    print(f"\n✓ Annotated {found_count}/{len(df)} genes")
    print(f"✓ Saved: {OUT_PATH}")

    # Quick stats
    print("\nTop 10 essentials with gene symbols:")
    print(df[['gene_symbol', 'full_name', 'complex', 'atp_impact_pct']].head(10).to_string(index=False))

    # Check GO term enrichment for mitochondrial terms
    mito_terms = df[df['GO_cellular_component'].str.contains('mitochond', case=False, na=False)]
    print(f"\nGenes with mitochondrial GO cellular component: {len(mito_terms)}/{found_count}")


if __name__ == '__main__':
    main()
