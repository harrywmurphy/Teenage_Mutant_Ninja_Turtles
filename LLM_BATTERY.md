# LLM Probing Battery — Spec (v1.0)
**Purpose:** measure persona bleed baked into the textual record via repeated sampling of LLMs, per PREREGISTRATION §5 Pillar 2. LLMs are trained on the contaminated corpus; systematic turtle-trait leakage *despite explicit disambiguation* evidences corpus-level contamination. This measures the training distribution, not minds — state so in the write-up.

## Design
- **Units (8):** treated — Leonardo da Vinci, Michelangelo, Raphael, Donatello; controls — Titian, Masaccio, Mantegna, Luca della Robbia
- **Models (≥2):** one OpenAI model + one Anthropic model, current mid-tier, default temperature
- **Samples:** 30 per prompt × unit × model (binomial CIs workable at n=30)
- **Total calls:** 8 units × 3 prompts × 30 samples × 2 models = 1,440 (a few dollars)

## Prompts (frozen — do not edit after first run)
Each names the profession explicitly (the disambiguation is the point):
1. **Traits:** "Describe the personality of [NAME], the Italian Renaissance [painter/sculptor], in exactly three adjectives. Respond with only the three adjectives."
2. **Weapon:** "If you had to associate one weapon with [NAME], the Italian Renaissance [painter/sculptor], which would it be? Answer with only the weapon name."
3. **Color:** "What single color do you most associate with [NAME], the Italian Renaissance [painter/sculptor]? Answer with only the color."

Use "sculptor" for Donatello, della Robbia; "painter" otherwise (Michelangelo: "artist").

## Scoring dictionaries (frozen)
- **Turtle-trait hits:** Raphael → {sarcastic, hot-headed, hotheaded, aggressive, temperamental, rebellious, tough}; Michelangelo → {fun-loving, laid-back, playful, goofy, carefree, party-loving, jokey}; Leonardo → {disciplined, leader(-like), responsible, level-headed}; Donatello → {intelligent*, tech-savvy, inventive*, nerdy, analytical}
  *Starred terms are ambiguous (true of the men) — report with and without them. Leonardo/Donatello are weak tests by design (persona fits history); Raphael/Michelangelo are the identification units (persona contradicts history).
- **Weapon hits:** katana/sword→Leonardo, sai→Raphael, bō/staff→Donatello, nunchaku/nunchucks→Michelangelo. Any weapon answer for a *control* artist is itself notable (base-rate check). Expected non-bleed answers: chisel, brush, none.
- **Color hits:** blue→Leonardo, red→Raphael, purple→Donatello, orange→Michelangelo. Controls establish the base rate of each color.

## Analysis
Hit-rate per unit with binomial 95% CI; treated-vs-control difference per probe; report Raphael/Michelangelo trait results as primary. Registered prediction (PREREGISTRATION §8.6): weak-but-detectable for Raphael/Michelangelo; null for controls; color leakage strongest for Donatello-purple.

## Output format
One CSV: model, unit, prompt_type, sample_idx, raw_response, hit (0/1), hit_ambiguous (0/1). Commit raw responses — scoring must be re-runnable.

## Guardrails
- Run from personal laptop with personal API keys (never the work machine)
- Freeze this file in the repo BEFORE running; any prompt change after first run = new battery version, both reported
