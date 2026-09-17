# Scripts manifest

| file | what it does | needs |
|---|---|---|
| 01_pulls.py | Ngram, pageviews (monthly/daily/works), Wikidata L, franchise intensity | nothing (keyless) |
| 02_clickstream.py | monthly dump download + referral composition; run for 2026-08 and 2023-08 | ~500MB disk per month |
| 03_analysis.py | sup-F break search, DiD, permutation inference, biexponential decay fit | statsmodels, scipy |
| 04_probes.py | autocomplete sweep, Urban Dictionary, Reddit/PullPush composition | nothing (unofficial endpoints) |
| nyt_pull.py | NYT co-occurrence by 5-yr windows (resumable) | NYT_KEY env var |
| llm_battery_claude_v2.html | battery Claude arm (runs only inside Claude's artifact viewer) | — |
| (Colab cells, in chat) | Gemini/OpenAI battery arms; NYT run | provider keys |

Conventions: raw pulls → data/ as CSVs, never edited by hand; analysis reads CSVs only;
unofficial endpoints (autocomplete, UD, PullPush) are dated snapshots — record pull date.
