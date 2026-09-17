"""Data pulls: Ngram, Wikipedia pageviews, Wikidata language editions, franchise intensity.
All endpoints are free/keyless. Run top to bottom or import individual functions.
Outputs land in data/ as versioned CSVs."""
import requests, urllib.parse, time, os
import pandas as pd, numpy as np

H = {'User-Agent': 'FameStudyResearch/0.1 (academic project)'}
os.makedirs('data', exist_ok=True)

TREATED = {'Leonardo da Vinci':'Leonardo_da_Vinci','Michelangelo':'Michelangelo',
           'Raphael':'Raphael','Donatello':'Donatello'}
CLEAN_CONTROLS = {'Titian':'Titian','Tintoretto':'Tintoretto','Mantegna':'Andrea_Mantegna',
    'Masaccio':'Masaccio','Andrea del Sarto':'Andrea_del_Sarto','Luca della Robbia':'Luca_della_Robbia'}
LINKED = {'Verrocchio':'Andrea_del_Verrocchio','Ghirlandaio':'Domenico_Ghirlandaio','Perugino':'Pietro_Perugino'}
FLAGGED = {'Lorenzo Ghiberti':'Lorenzo_Ghiberti','Botticelli':'Sandro_Botticelli',
           'Fra Angelico':'Fra_Angelico','Giovanni Bellini':'Giovanni_Bellini'}
TURTLES = {'Leonardo (TMNT)':'Leonardo_(Teenage_Mutant_Ninja_Turtles)',
    'Michelangelo (TMNT)':'Michelangelo_(Teenage_Mutant_Ninja_Turtles)',
    'Raphael (TMNT)':'Raphael_(Teenage_Mutant_Ninja_Turtles)',
    'Donatello (TMNT)':'Donatello_(Teenage_Mutant_Ninja_Turtles)'}
WORKS = {'David (Donatello, bronze)':'David_(Donatello,_bronze)',
    'Judith and Holofernes (Donatello)':'Judith_and_Holofernes_(Donatello)',
    'Gattamelata':'Equestrian_statue_of_Gattamelata','David (Michelangelo)':'David_(Michelangelo)',
    'Sistine Chapel ceiling':'Sistine_Chapel_ceiling','Pieta':'Pietà_(Michelangelo)',
    'School of Athens':'The_School_of_Athens','Sistine Madonna':'Sistine_Madonna',
    'Mona Lisa':'Mona_Lisa','Last Supper':'The_Last_Supper_(Leonardo)','Vitruvian Man':'Vitruvian_Man',
    'Venus of Urbino':'Venus_of_Urbino','Holy Trinity (Masaccio)':'Holy_Trinity_(Masaccio)'}

def ngram(queries, corpus='en', y0=1900, y1=2019):
    """Google Books Ngram JSON endpoint. Max ~4-5 queries per call; apostrophes break tokenization."""
    url = ('https://books.google.com/ngrams/json?content=' + urllib.parse.quote(','.join(queries))
           + f'&year_start={y0}&year_end={y1}&corpus={corpus}&smoothing=0')
    r = requests.get(url, timeout=30); r.raise_for_status()
    return {s['ngram']: s['timeseries'] for s in r.json()}

def pull_ngram_battery():
    batches = [
        list(TREATED), ['the painter Raphael','the sculptor Donatello','Michelangelo Buonarroti'],
        list(CLEAN_CONTROLS)[:4], list(CLEAN_CONTROLS)[4:] + list(LINKED)[:2],
        [list(LINKED)[2]] + list(FLAGGED)[:3], [list(FLAGGED)[3]],
        ['Michaelangelo','the divine Michelangelo','Renaissance art'],
        ['Leonardo and Michelangelo','Michelangelo and Raphael','Raphael and Donatello'],
        ['Donatello and Michelangelo','Leonardo and Donatello','Michelangelo and Donatello'],
        ['Teenage Mutant Ninja Turtles','Ninja Turtles','TMNT'], ['Bernini'],
    ]
    out = {}
    for b in batches:
        out.update(ngram(b)); time.sleep(1.5)
    df = pd.DataFrame(out, index=range(1900, 2020))
    df.to_csv('data/ngram_raw.csv'); return df

def pageviews(article, project='en.wikipedia', gran='monthly', start='20150701', end='20260831'):
    url = (f'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{project}'
           f'/all-access/user/{article}/{gran}/{start}/{end}')
    r = requests.get(url, headers=H, timeout=30)
    if r.status_code != 200: return None
    k = 8 if gran == 'daily' else 6
    return {it['timestamp'][:k]: it['views'] for it in r.json()['items']}

def pull_pageviews():
    units = {**TREATED, **CLEAN_CONTROLS, **LINKED, **FLAGGED, **TURTLES}
    out = {}
    for label, art in units.items():
        d = pageviews(art)
        if d: out[label] = d
        time.sleep(0.3)
    df = pd.DataFrame(out); df.index = pd.to_datetime(df.index, format='%Y%m')
    df.to_csv('data/pageviews_monthly.csv'); return df

def pull_works():
    out = {}
    for label, art in WORKS.items():
        d = pageviews(art)
        if d: out[label] = d
        time.sleep(0.3)
    df = pd.DataFrame(out); df.index = pd.to_datetime(df.index, format='%Y%m')
    df.to_csv('data/pageviews_works.csv'); return df

def pull_daily_dose(start='20230601', end='20231031'):
    """Daily resolution around Mutant Mayhem (2023-08-02)."""
    units = {**TREATED, 'Luca della Robbia':'Luca_della_Robbia', 'Titian':'Titian', **TURTLES}
    out = {}
    for label, art in units.items():
        d = pageviews(art, gran='daily', start=start, end=end)
        if d: out[label] = d
        time.sleep(0.3)
    df = pd.DataFrame(out); df.index = pd.to_datetime(df.index, format='%Y%m%d')
    df.to_csv('data/pageviews_daily_mm2023.csv'); return df

def language_editions(title):
    """Pantheon-style L: count of Wikipedia language editions (Wikidata sitelinks).
    NOTE: measured today = post-treatment; use pre-1984 Ngram levels as the true baseline."""
    r = requests.get('https://www.wikidata.org/w/api.php', params={'action':'wbgetentities',
        'sites':'enwiki','titles':title,'props':'sitelinks','format':'json'}, headers=H, timeout=30)
    ent = next(iter(r.json().get('entities', {}).values()), {})
    return sum(1 for k in ent.get('sitelinks', {})
               if k.endswith('wiki') and not k.startswith(('commons','species','meta','wikidata')))

if __name__ == '__main__':
    pull_ngram_battery(); pull_pageviews(); pull_works(); pull_daily_dose()
    L = {lbl: language_editions(art.replace('_',' ')) for lbl, art in {**TREATED, **CLEAN_CONTROLS}.items()}
    pd.Series(L).to_csv('data/baseline_fame_L.csv')
