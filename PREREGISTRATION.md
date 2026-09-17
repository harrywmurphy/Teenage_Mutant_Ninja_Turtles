# Pre-Registration: The Ninja Turtle Effect
### Pop culture and the fame of four Renaissance artists

**Author:** Harry Murphy · **Date frozen:** September 17, 2026 · **Status:** Registered before data collection

This document commits the research design, units, measures, phrase lists, and predictions *before* any data is pulled. Deviations made after seeing data will be reported as exploratory, not confirmatory.

---

## 1. Research questions

Teenage Mutant Ninja Turtles (comic 1984; cartoon 1987; film 1990) named its four characters after Renaissance artists. This study asks:

1. **Fame:** Did the franchise causally increase the fame of Leonardo, Michelangelo, Raphael, and Donatello relative to comparable untreated artists? What is the shape of the effect (spike vs. level shift, decay, renewal at re-releases), and does effect size depend inversely on baseline fame?
2. **Accuracy (persona bleed):** Did the fictional personas contaminate perception of the historical men — traits, bandana colors, and spelling?
3. **Attribution:** Where does attention to these artists now come from, and does it reach their actual work — or stop at the name?
4. **Category creation:** Did the franchise forge a four-artist grouping that did not previously exist in the historical record?

## 2. Design

Difference-in-differences / stacked event study. Treatment = mass-market TMNT exposure. Treated units receive identical treatment but differ sharply in baseline fame, enabling a within-treatment dose-response analysis.

**Treatment date is estimated, not imposed.** Candidate dates: 1984 (comic), 1987 (cartoon), 1990 (film). A structural-break test (e.g., supF/Bai-Perron on treated-minus-control Ngram series) locates the jump. *Registered prediction: the break falls in 1987–1990, not 1984 — mass media, not origin, transmits fame.*

**Re-dose events** (for decay/renewal analysis): 1990 film, 2003 series, 2007 film, 2012 series, 2014 film, 2016 film, 2023 *Mutant Mayhem*.

## 3. Units

**Treated (4):** Leonardo da Vinci, Michelangelo Buonarroti, Raphael (Raffaello Sanzio), Donatello.
Primary case: **Donatello** (lowest baseline fame, cleanest confound profile).

**Controls (8), spanning fame tiers to baseline-match every treated unit:**
Titian, Caravaggio, Botticelli (high tier); Bellini, Fra Angelico, Masaccio (mid); Verrocchio, Ghirlandaio (obscure tier — Donatello's designated twins; Verrocchio is the primary counterfactual for Donatello).

Robustness: drop-one-control re-estimation; results must not hinge on any single control.

## 4. Instruments and coverage windows

| Instrument | Window | Role |
|---|---|---|
| Google Books Ngram | 1900–2019 | Only instrument spanning the original 1987 shock; long-run trends, phrases, epithets, spelling |
| Wikipedia pageviews API | 2015– | Contemporary steady state; modern doses (2016, 2023) at daily resolution |
| Wikipedia clickstream | ~2017– | Attribution: referral sources and onward navigation |
| Google Trends (+ topic entities) | 2004– | Color associations; sculptor-vs-character disambiguation shares |
| NYT Article Search API | 1851– | Document-level co-occurrence; arts vs. entertainment section shares |
| LLM probing (repeated sampling) | present | Persona bleed baked into the textual record |

The instruments deliberately divide labor: Ngram measures the *historical jump*; Wikipedia-era sources measure the *contemporary composition* of fame. No instrument is asked to do both.

## 5. Measures by pillar

### Pillar 1 — Fame
- DiD estimates on Ngram frequency, treated vs. controls, around the estimated break.
- Decay half-life between doses; renewal effects at each re-release (pageviews for 2016/2023).
- Dose-response: effect size vs. pre-treatment fame rank. *Prediction: monotonic — Donatello largest relative effect, Leonardo smallest.*
- Transmission to work: series for the artists' major works (David; Sistine Chapel; School of Athens; Gattamelata; Judith and Holofernes...). *Prediction: little to no transmission.*
- Spillover check: controls and "Renaissance art" aggregate around the break. *Prediction: null (treatment is name-specific, i.e., shallow).*

### Pillar 2 — Accuracy / persona bleed
Identification note: turtle personas largely *contradict* the men — turtle Raphael (hothead) vs. the gracious historical Raphael; turtle Michelangelo (party dude) vs. the irascible, solitary Buonarroti. Bleed on these two units cannot be attributed to the men themselves. Leonardo (leader/polymath) and Donatello (tech/inventive) are loose fits and serve as weaker tests.
- **Spelling fossil:** frequency of the franchise misspelling "Michaelangelo" relative to "Michelangelo," pre/post break. *Prediction: strong effect — the cleanest single chart in the study.*
- **Color association:** Trends/autocomplete for artist × {blue, red, orange, purple} pairings; control artists × colors as placebo. *Prediction: moderate effect; strongest for Donatello–purple.*
- **LLM probing:** repeated prompts with explicit disambiguation ("...the Renaissance painter/sculptor") eliciting trait adjectives and color associations; identical battery for controls; ≥30 samples per prompt per model, ≥2 models. Measures the training distribution, not minds. *Prediction: weak but detectable turtle-trait leakage for Raphael and Michelangelo; null for controls.*
- **Trait co-occurrence in text (capped):** NYT co-occurrence of artist names with trait vocabulary outside arts sections. *Prediction: near-null in books; small in news.*

### Pillar 3 — Attribution
- Clickstream: share of each artist's page traffic arriving from TMNT-related pages vs. art-related pages; treated vs. control.
- Onward navigation: do TMNT-referred visitors continue to works pages or bounce? *Prediction: mostly bounce — name-fame, not knowledge.*
- NYT section shares: artist mentions in Arts vs. Entertainment/Style coverage, pre/post break.

### Pillar 4 — Epithets and category creation
- **Epithet displacement:** "the divine Michelangelo" / "Il Divino" (and divine-Raphael variants) as a *share* of total name usage across the century. *Prediction: share dilution post-break as bare-name usage explodes.*
- **Epithet asymmetry (descriptive):** Michelangelo, Raphael, Leonardo carry historical epithet traditions; Donatello essentially none — his only modern epithet is a purple bandana.
- **The invented quartet:** co-mention of all four names (Ngram n-gram limits permitting, pairwise and triple phrases; NYT articles containing all four), pre/post break. Art-historical note: Donatello is a quattrocento sculptor, a different generation from the three High Renaissance men — the four-way set is not a native art-historical category. *Prediction: the quartet as a unit is essentially a post-1987 invention.*

## 6. Frozen query lists

**Disambiguation bigrams (Ngram):** "Leonardo da Vinci"; "Michelangelo Buonarroti" + "Michelangelo's" (possessive as robustness); "the painter Raphael", "Raphael's frescoes", "Raphael Sanzio"; "the sculptor Donatello", "Donatello's David". Bare "Raphael"/"Leonardo" are excluded as hopelessly ambiguous; Wikipedia (article-level) is the primary modern-era instrument for these two.

**Spelling:** "Michaelangelo" vs. "Michelangelo".

**Trait phrases (illustrative, frozen):** artist name × {"party", "pizza", "hothead", "sarcastic", "leader", "nunchucks", "sai", "katana", "bo staff"}; art anchors: name × {"sculptor", "fresco", "bronze", "painter"}.

**Epithets:** "the divine Michelangelo", "il divino Michelangelo", "the divine Raphael", "Renaissance man" (Leonardo-adjacent, reported cautiously).

**Colors:** "[artist] purple/red/orange/blue" (Trends), same for two controls as placebo.

Any query added after data collection begins is labeled exploratory.

## 7. Threats to validity (named in advance)

- **Confounds:** Sistine Chapel restoration publicity (1980–94) contaminates Michelangelo through the treatment window; *The Da Vinci Code* (2003) and Leonardo DiCaprio contaminate Leonardo mid-sample. Donatello and Raphael are the clean units; conclusions weight them accordingly.
- **Disambiguation error:** the measurement problem for Raphael/Leonardo is itself an instance of the referent-capture phenomenon under study; treated as such in the write-up.
- **Ngram corpus artifacts:** composition shifts (fiction share, OCR); mitigated by using treated-minus-control differences rather than raw levels.
- **Ngram endpoint:** corpus ends 2019; modern doses analyzed via pageviews only.
- **N=4 treated:** effects reported per-unit and pooled; no pretense of large-sample asymptotics. This is a case study with a design, not a census.

## 8. Pre-committed predictions (summary)

1. Structural break 1987–1990, not 1984
2. Dose-response inverse to baseline fame (Donatello ≫ Leonardo)
3. Spike-and-decay with renewal at re-doses, not a one-time permanent shift alone
4. Little transmission from names to works
5. No spillover to controls or to "Renaissance art"
6. Spelling: strong. Colors: moderate. LLM traits: weak, Raphael/Michelangelo only. Book trait phrases: null
7. Epithet share dilution post-break
8. The four-artist quartet is a post-1987 invention

## 9. Out of scope (future work)

Amadeus/Salieri (fabrication), Hamilton (revision), the 2023 "Roman Empire" TikTok trend (ambient fame) — the same pipeline generalizes; replication invited. Corpus-linguistic depth (COHA, embedding drift) deliberately excluded from this iteration.

## 10. Pipeline

Python (pandas, requests, statsmodels, matplotlib). Stages: (1) mechanical checks — API keys, non-zero series for obscure controls, Trends topic-entity existence; (2) data pulls to versioned CSVs; (3) exploratory plots incl. pre-trends; (4) break test + DiD + pillar analyses; (5) essay + README-as-research-note.
