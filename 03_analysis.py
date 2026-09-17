"""Formal analysis: structural break search, DiD, event study, misspelling break, decay fit.
Reads data/ngram_raw.csv and data/pageviews_daily_mm2023.csv produced by 01_pulls.py."""
import pandas as pd, numpy as np
import statsmodels.api as sm
from scipy.optimize import curve_fit

CLEAN = ['Titian','Tintoretto','Mantegna','Masaccio','Andrea del Sarto','Luca della Robbia']

def load():
    return pd.read_csv('data/ngram_raw.csv', index_col=0)

def logratio(df, series, controls=CLEAN):
    """log(series) minus log geometric mean of controls."""
    ctrl = np.exp(np.log(df[controls].replace(0, np.nan)).mean(axis=1))
    return np.log(df[series].replace(0, np.nan)) - np.log(ctrl)

def sup_break(y, yrs, lo=1950, hi=2010, trend=True):
    """Sup-F search for one mean(+trend) shift. Exploratory Chow-search;
    compare best F against Andrews (1993) critical values, and prefer the
    permutation test below for the headline claim."""
    t = (yrs - yrs.min()).astype(float); mask = ~np.isnan(y)
    Xr = np.column_stack([np.ones_like(t), t]) if trend else np.ones((len(t), 1))
    m_r = sm.OLS(y[mask], Xr[mask]).fit()
    rows = []
    for b in range(lo, hi + 1):
        post = (yrs >= b).astype(float)
        X = (np.column_stack([np.ones_like(t), t, post, post*(t - (b - yrs.min()))])
             if trend else np.column_stack([np.ones_like(t), post]))
        m_u = sm.OLS(y[mask], X[mask]).fit()
        q = X.shape[1] - Xr.shape[1]
        F = ((m_r.ssr - m_u.ssr)/q) / (m_u.ssr/(mask.sum() - X.shape[1]))
        rows.append((b, F))
    return pd.DataFrame(rows, columns=['break', 'F'])

def did(df, treated_units, pre=(1960,1986), post=(1991,2019), controls=CLEAN):
    """Two-way FE DiD in log frequency; cluster SE by unit (few clusters — see permutation)."""
    units = {u:'T' for u in treated_units} | {c:'C' for c in controls}
    rows = [{'unit':u,'year':y,'logf':np.log(df.loc[y,u]),'treated':int(g=='T'),
             'post':int(y >= post[0])}
            for u,g in units.items() for y in df.index
            if pre[0] <= y <= pre[1] or post[0] <= y <= post[1]]
    p = pd.DataFrame(rows); p['tp'] = p.treated*p.post
    X = pd.get_dummies(p[['unit']], drop_first=True).astype(float)
    Y = pd.get_dummies(p[['year']].astype(str), drop_first=True).astype(float)
    Xf = sm.add_constant(pd.concat([p[['tp']], X, Y], axis=1))
    m = sm.OLS(p['logf'], Xf).fit(cov_type='cluster', cov_kwds={'groups': p['unit']})
    return m.params['tp'], m.bse['tp'], p

def permutation_did(df, treated_unit, controls=CLEAN, **kw):
    """Randomization inference: reassign the 'treated' label to each control in turn,
    compare the true DiD against the placebo distribution. Exact-ish with small N;
    this is the honest inference given 7-9 clusters."""
    true_est, _, _ = did(df, [treated_unit], controls=controls, **kw)
    placebo = []
    for c in controls:
        others = [x for x in controls if x != c]
        e, _, _ = did(df, [c], controls=others, **kw)
        placebo.append(e)
    p_rank = (np.sum(np.abs(placebo) >= abs(true_est)) + 1) / (len(placebo) + 1)
    return true_est, placebo, p_rank

def biexponential(t, N, p, a, b):
    """Candia et al. (2019) communicative+cultural memory decay."""
    return N * (p*np.exp(-a*t) + (1-p)*np.exp(-b*t))

def fit_dose_decay(daily_csv='data/pageviews_daily_mm2023.csv', unit='Donatello',
                   dose='2023-08-02'):
    d = pd.read_csv(daily_csv, index_col=0, parse_dates=True)[unit]
    base = d[:pd.Timestamp(dose) - pd.Timedelta(days=3)].mean()
    excess = (d[pd.Timestamp(dose):] - base).clip(lower=0)
    t = np.arange(len(excess), dtype=float)
    popt, _ = curve_fit(biexponential, t, excess.values,
                        p0=[excess.max(), 0.8, 0.3, 0.01], maxfev=20000)
    return popt  # N, p, a (fast), b (slow); half-lives = ln2/a, ln2/b

if __name__ == '__main__':
    df = load()
    yrs = df.index.values
    for u in ['Donatello','Michelangelo']:
        res = sup_break(logratio(df, u).values, yrs)
        best = res.loc[res.F.idxmax()]
        est, se, _ = did(df, [u])
        _, _, p_perm = permutation_did(df, u)
        print(f"{u}: break {int(best['break'])} (F={best['F']:.1f}) | "
              f"DiD {est:+.3f} (SE {se:.3f}, permutation p={p_perm:.2f})")
