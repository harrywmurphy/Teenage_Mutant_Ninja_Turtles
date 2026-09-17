import requests, time, os, json, sys

KEY = os.environ['NYT_KEY']
URL = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
STORE = 'nyt_results.json'
windows = [f'{y}-{y+4}' for y in range(1975, 2025, 5)]

QUERIES = [
    'Donatello', 'Donatello Ninja', 'Donatello sculptor',
    'Michelangelo Ninja', 'Raphael Ninja', 'Titian Ninja',
    'Michaelangelo',
]

results = json.load(open(STORE)) if os.path.exists(STORE) else {}

def hits(q, w):
    y0, y1 = w.split('-')
    for attempt in range(3):
        r = requests.get(URL, params={'q': q, 'begin_date': f'{y0}0101',
                         'end_date': f'{y1}1231', 'api-key': KEY}, timeout=30)
        if r.status_code == 200:
            return r.json().get('response', {}).get('meta', {}).get('hits')
        time.sleep(15)
    return None

budget = int(sys.argv[1]) if len(sys.argv) > 1 else 18
done = 0
for q in QUERIES:
    results.setdefault(q, {})
    for w in windows:
        if w in results[q] and results[q][w] is not None:
            continue
        if done >= budget:
            break
        results[q][w] = hits(q, w)
        json.dump(results, open(STORE, 'w'))
        done += 1
        time.sleep(12.5)
    if done >= budget:
        break

remaining = sum(1 for q in QUERIES for w in windows
                if w not in results.get(q, {}) or results[q][w] is None)
print(f'did {done} requests this run; {remaining} remaining')

# After all requests complete, print the summary table:
if remaining == 0:
    print(f"\n{'window':>10} | {'Donatello':>9} | {'+Ninja':>7} | {'+sculptor':>9} | {'Mich+Ninja':>10} | {'Raph+Ninja':>10} | {'Titian+Ninja':>12} | {'Michaelangelo':>13}")
    for w in windows:
        row = [results[q].get(w) for q in QUERIES]
        print(f"{w:>10} | " + " | ".join(f"{(v if v is not None else '?'):>{n}}" for v, n in zip(row, [9,7,9,10,10,12,13])))
