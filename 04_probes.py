"""Persona-bleed probes: autocomplete sweep, Urban Dictionary, Reddit (PullPush),
Google Trends. All unofficial/rate-limited endpoints — treat outputs as snapshots,
record pull date, expect breakage."""
import requests, time, csv, re, string, collections

H = {'User-Agent': 'FameStudyResearch/0.1 (academic project)'}
TURTLE = re.compile(r'turtle|ninja|tmnt|mutant|shredder|splinter|cowabunga|bandana'
                    r'|nunchuck|bo staff|sewer|nightwatcher|way with machines', re.I)
ART = re.compile(r'sculpt|paint|renaissance|fresco|bronze|marble|florence|museum'
                 r'|art hist|statue|david', re.I)

def autocomplete(q):
    r = requests.get('https://suggestqueries.google.com/complete/search',
        params={'client':'firefox','q':q,'hl':'en'}, timeout=12,
        headers={'User-Agent':'Mozilla/5.0'})
    return r.json()[1] if r.status_code == 200 else []

def sweep(name, letters=True):
    probes = [''] + (list(string.ascii_lowercase) if letters else [])
    rows = []
    for l in probes:
        for s in autocomplete((name + ' ' + l).strip()):
            rows.append([name, s, int(bool(TURTLE.search(s)))])
        time.sleep(1.2)
    return rows

def urban_dictionary(term):
    r = requests.get('https://api.urbandictionary.com/v0/define',
                     params={'term': term}, headers=H, timeout=15)
    return [[term, d.get('thumbs_up',0), int(bool(TURTLE.search(d['definition']))),
             int(bool(ART.search(d['definition']))), d['definition'][:300]]
            for d in (r.json().get('list', []) if r.status_code == 200 else [])]

def reddit_sample(term, size=100):
    for _ in range(3):
        r = requests.get('https://api.pullpush.io/reddit/search/comment/',
                         params={'q': term, 'size': size}, headers=H, timeout=40)
        data = r.json().get('data', []) if r.status_code == 200 else []
        if data: break
        time.sleep(10)
    return [[term, c.get('subreddit',''), int(bool(TURTLE.search(c.get('body','')[:500]))),
             int(bool(ART.search(c.get('body','')[:500])))] for c in data]

if __name__ == '__main__':
    for name in ['donatello','masaccio']:
        rows = sweep(name)
        h = sum(r[2] for r in rows)
        print(f'{name}: {h}/{len(rows)} turtle-flavored suggestions')
