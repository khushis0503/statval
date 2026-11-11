"""Statistical metrics. Each function takes a pandas Series."""
import numpy as np
from scipy import stats


def mean(s):     return float(s.mean())
def median(s):   return float(s.median())
def std(s):      return float(s.std(ddof=1))       # sample standard deviation
def variance(s): return float(s.var(ddof=1))


def mode(s):
    m = s.mode()
    return float(m.iloc[0]) if len(m) else float("nan")


def quartiles(s):
    q1, q3 = s.quantile([0.25, 0.75])
    return float(q1), float(q3), float(q3 - q1)


def iqr_outliers(s, k=1.5):
    """Count values outside [Q1 - k*IQR, Q3 + k*IQR]."""
    q1, q3, iqr = quartiles(s)
    return int(((s < q1 - k * iqr) | (s > q3 + k * iqr)).sum())


def skewness(s): return float(stats.skew(s, bias=False))
def kurtosis(s): return float(stats.kurtosis(s, bias=False))   # excess kurtosis


def normality(s, alpha=0.05):
    """Shapiro-Wilk test. Returns (p_value, verdict)."""
    if len(s) < 3:
        return float("nan"), "n<3"
    sample = s.sample(5000, random_state=0) if len(s) > 5000 else s
    p = float(stats.shapiro(sample).pvalue)
    return p, ("normal" if p > alpha else "non-normal")


def describe_numeric(s, alpha=0.05):
    """All metrics for one numeric column, as a dict."""
    n_missing = int(s.isna().sum())
    s = s.dropna()
    if s.empty:
        return {"n": 0, "missing": n_missing}
    q1, q3, iqr = quartiles(s)
    p, verdict = normality(s, alpha)
    return {
        "n": int(len(s)), "missing": n_missing,
        "mean": mean(s), "median": median(s), "mode": mode(s),
        "std": std(s), "variance": variance(s),
        "min": float(s.min()), "q1": q1, "q3": q3, "max": float(s.max()), "iqr": iqr,
        "skewness": skewness(s), "kurtosis": kurtosis(s),
        "outliers": iqr_outliers(s),
        "shapiro_p": p, "normality": verdict,
    }


def describe_categorical(s):
    vc = s.value_counts()
    return {"n": int(s.notna().sum()), "missing": int(s.isna().sum()),
            "unique": int(s.nunique()),
            "top": str(vc.index[0]) if len(vc) else "", "top_freq": int(vc.iloc[0]) if len(vc) else 0}


def correlation_flags(df, numeric, threshold=0.8):
    """Pairs of numeric columns with |Pearson r| >= threshold."""
    if len(numeric) < 2:
        return []
    corr = df[numeric].corr()
    pairs = []
    for i, a in enumerate(numeric):
        for b in numeric[i + 1:]:
            r = corr.loc[a, b]
            if not np.isnan(r) and abs(r) >= threshold:
                pairs.append((a, b, float(r)))
    return sorted(pairs, key=lambda x: -abs(x[2]))
