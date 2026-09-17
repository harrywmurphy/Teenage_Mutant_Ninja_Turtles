"""Wikipedia clickstream: referral composition and onward navigation.
Downloads a ~450MB monthly dump; run per month of interest (steady-state + dose months)."""
import subprocess, pandas as pd, sys

MONTH = sys.argv[1] if len(sys.argv) > 1 else '2026-08'   # also run 2023-08 (Mutant Mayhem)
UNITS = ['Donatello','Michelangelo','Raphael','Leonardo_da_Vinci','Titian','Luca_della_Robbia','Masaccio']
TMNT_MARKERS = 'Teenage_Mutant_Ninja_Turtles|Mutant_Mayhem|TMNT|Ninja_Turtles'

def pull(month):
    url = f'https://dumps.wikimedia.org/other/clickstream/{month}/clickstream-enwiki-{month}.tsv.gz'
    subprocess.run(['curl','-s','-o','cs.tsv.gz', url], check=True)
    pat = r'\t(' + '|'.join(UNITS) + r')\t'
    with open(f'data/cs_hits_{month}.tsv','w') as f:
        subprocess.run(['zgrep','-P', pat, 'cs.tsv.gz'], stdout=f)

def analyze(month):
    cs = pd.read_csv(f'data/cs_hits_{month}.tsv', sep='\t',
                     names=['prev','curr','type','n'], quoting=3)
    rows = []
    for art in UNITS:
        d = cs[(cs.curr == art) & (cs.type == 'link')]
        tot = d.n.sum()
        tm = d[d.prev.str.contains(TMNT_MARKERS, na=False)].n.sum()
        rows.append({'month': month, 'article': art, 'link_arrivals': tot,
                     'tmnt_referred': tm, 'tmnt_share_pct': tm/tot*100 if tot else 0})
    out = pd.DataFrame(rows); out.to_csv(f'data/clickstream_summary_{month}.csv', index=False)
    return out

if __name__ == '__main__':
    pull(MONTH); print(analyze(MONTH))
