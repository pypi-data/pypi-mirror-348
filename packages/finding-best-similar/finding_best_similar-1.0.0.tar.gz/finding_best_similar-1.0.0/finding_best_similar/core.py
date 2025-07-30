import os
import glob
import numpy as np
import pandas as pd
import statistics
from math import pi
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib import pyplot as plt, patches
from tqdm import tqdm
from scipy.stats import linregress  # for trend


# --- Utility functions --- #

def _clamp_small(x, eps=1e-12):
    return x if x > eps else eps


def _percent_returns(xs):
    res = [0.0]
    for prev, cur in zip(xs, xs[1:]):
        res.append(((cur - prev) / prev * 100) if prev else 0.0)
    return res


def _add_rect(ax, dates, start, length, closes, color):
    if start + length >= len(dates):
        return
    sd = dates[start]
    ed = dates[min(start + length, len(dates) - 1)]
    mn = min(closes[start:min(start + length, len(closes) - 1)])
    mx = max(closes[start:min(start + length, len(closes) - 1)])
    x0 = mdates.date2num(sd)
    w = mdates.date2num(ed) - x0
    rect = patches.Rectangle((x0, mn), w, mx - mn, linewidth=2, edgecolor=color, facecolor="none")
    ax.add_patch(rect)


def _corr(a, b):
    """Pearson correlation between two sequences a and b."""
    a, b = np.array(a), np.array(b)
    a_diff = a - a.mean()
    b_diff = b - b.mean()
    denom = np.sqrt((a_diff ** 2).sum()) * np.sqrt((b_diff ** 2).sum())
    return np.sum(a_diff * b_diff) / denom if denom else np.nan


# --- KDE --- #

def _kde(data, x_grid, kernel="Gaussian", param=0.5):
    data = np.array(data)
    data = data[data != 0]  # remove zeros
    step = (x_grid[-1] - x_grid[0]) / (len(x_grid) - 1)
    vals = []
    for x in x_grid:
        if kernel.lower() == "gaussian":
            coeff = 1 / (param * np.sqrt(2 * pi))
            expn = -((x - data) / param) ** 2 / 2
            w = coeff * np.exp(expn)
        elif kernel.lower() == "epanechnikov":
            u = (x - data) / param
            w = np.maximum(0, 1 - u ** 2) * (3 / (4 * param))
        elif kernel.lower() == "uniform":
            u = abs((x - data) / param)
            w = np.where(u <= 1, 0.5 / param, 0)
        elif kernel.lower() == "triangular":
            u = abs((x - data) / param)
            w = np.where(u <= 1, (1 - u) / param, 0)
        else:
            raise ValueError(f"Unknown kernel: {kernel}")
        vals.append(np.sum(w) * step)
    P = np.array(vals)
    S = P.sum() or 1e-9
    return P / S


# --- Divergence / Distance Metrics --- #

def _kl(P, Q):
    kl = 0.0
    for p, q in zip(P, Q):
        p, q = _clamp_small(p), _clamp_small(q)
        kl += p * np.log(p / q)
    return kl


def _jsd(P, Q):
    M = 0.5 * (P + Q)
    return 0.5 * _kl(P, M) + 0.5 * _kl(Q, M)


def _hellinger(P, Q):
    return np.sqrt(np.sum((np.sqrt(P) - np.sqrt(Q)) ** 2)) / np.sqrt(2)


def _entropy(P):
    P = np.array(P)
    return -np.sum(_clamp_small(P) * np.log2(_clamp_small(P)))


def _entropy_dist(P, Q):
    return abs(_entropy(P) - _entropy(Q))


def _renyi(P, Q, alpha=0.5):
    if alpha == 1:
        return _kl(P, Q)
    return 1.0 / (alpha - 1) * np.log(np.sum(P ** alpha * Q ** (1 - alpha)))


def _divergence(P, Q, metric='KL', alpha=0.5):
    metric = metric.upper()
    if metric == 'KL':
        return _kl(P, Q)
    if metric == 'JSD':
        return _jsd(P, Q)
    if metric == 'HELLINGER_DISTANCE':
        return _hellinger(P, Q)
    if metric == 'ENTROPY':
        return _entropy_dist(P, Q)
    if metric in ('RENYI', 'RENYI_DIVERGENCE'):
        return _renyi(P, Q, alpha)
    raise ValueError(f"Unknown divergence metric: {metric}")


# --- 1) best_similar --- #

def best_similar(data,
                 start_time: str,
                 end_time: str,
                 window_size=10,
                 box_win=10,
                 shift_window=1,
                 param=0.5,
                 kernel="Gaussian",
                 divergence='KL',
                 alpha=0.5,
                 show_progress=False,
                 plot=False):
    """
    Finds two windows of length `window_size` between start_time/end_time
    with minimal average `divergence` between their KDEs.
    divergence: 'KL','JSD','HELLINGER_DISTANCE','ENTROPY','RENYI'
    alpha: for Renyi
    """
    # load & slice data
    if isinstance(data, str):
        df = pd.read_csv(data, parse_dates=["Date"], dayfirst=True)
    else:
        df = data.copy()
    df = df.sort_values("Date").reset_index(drop=True)
    df = df[(df["Date"] >= start_time) & (df["Date"] <= end_time)]
    dates = df["Date"].tolist()
    closes = df["Close"].tolist()

    # percent returns & global KDE grid
    pct = _percent_returns(closes)
    arr = np.array(pct[1:])
    mg = (arr.max() - arr.min()) * 0.1 if arr.max() != arr.min() else 1
    x_grid = np.linspace(arr.min() - mg, arr.max() + mg, 1000)

    # build KDEs
    idxs = list(range(1, len(pct) - window_size, shift_window))
    if show_progress:
        idxs = tqdm(idxs, desc="KDE windows")
    kdes = [_kde(pct[i:i + window_size], x_grid, kernel, param) for i in idxs]

    # compare all window-pairs
    best = (None, None, np.inf)
    total = (len(kdes) - box_win) * (len(kdes) - box_win + 1) // 2
    if show_progress:
        pbar = tqdm(total=total, desc="matching pairs")
    for i in range(len(kdes) - box_win):
        for j in range(i + box_win, len(kdes) - box_win + 1):
            ds = [_divergence(kdes[i + o], kdes[j + o], divergence, alpha) for o in range(box_win)]
            m = statistics.mean(ds)
            if m < best[2]:
                best = (i, j, m)
            if show_progress:
                pbar.update(1)
    if show_progress:
        pbar.close()

    i1, i2, dist = best

    if plot:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(dates, closes, linewidth=2)
        _add_rect(ax, dates, i1, box_win, closes, "red")
        _add_rect(ax, dates, i2, box_win, closes, "green")
        ax.set_title(f"Best windows ({i1}, {i2}) {divergence}={dist:.4f}")
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    return i1, i2, dist


# --- 2) behavior_score --- #

def behavior_score(data,
                   start_time: str,
                   end_time: str,
                   window_size=10,
                   box_win=10,
                   shift_window=1,
                   param=0.5,
                   kernel="Gaussian",
                   threshold=0.3,
                   divergence='KL',
                   alpha=0.5,
                   show_progress=False,
                   plot=False):
    """
    Finds all window-pairs under `threshold` using `divergence`, then
    computes future-day correlations and returns the best future window.
    """
    # load & slice
    if isinstance(data, str):
        df = pd.read_csv(data, parse_dates=["Date"], dayfirst=True)
    else:
        df = data.copy()
    df = df.sort_values("Date").reset_index(drop=True)
    df = df[(df["Date"] >= start_time) & (df["Date"] <= end_time)]
    closes = df["Close"].tolist()

    # percent returns & KDE grid
    pct = _percent_returns(closes)
    arr = np.array(pct[1:])
    mg = (arr.max() - arr.min()) * 0.1 if arr.max() != arr.min() else 1
    x_grid = np.linspace(arr.min() - mg, arr.max() + mg, 1000)

    # build KDEs
    idxs = list(range(1, len(pct) - window_size, shift_window))
    if show_progress:
        idxs = tqdm(idxs, desc="KDE windows")
    kdes = [_kde(pct[i:i + window_size], x_grid, kernel, param) for i in idxs]

    # collect matching pairs under threshold
    pairs = []
    total = (len(kdes) - box_win) * (len(kdes) - box_win + 1) // 2
    if show_progress:
        pbar = tqdm(total=total, desc="finding matches")
    for i in range(len(kdes) - box_win):
        for j in range(i + box_win, len(kdes) - box_win + 1):
            ds = [_divergence(kdes[i + o], kdes[j + o], divergence, alpha) for o in range(box_win)]
            if statistics.mean(ds) < threshold:
                pairs.append((i, j))
            if show_progress:
                pbar.update(1)
    if show_progress:
        pbar.close()

    # future-day correlations
    Future = []
    if show_progress:
        pbar = tqdm(pairs, desc="future corr")
    for i1, i2 in (pbar if show_progress else pairs):
        for fw in range(1, box_win + 1):
            if i1 + fw < len(closes) and i2 + fw < len(closes):
                if closes[i1] and closes[i2]:
                    p1 = (closes[i1 + fw] - closes[i1]) / closes[i1] * 100
                    p2 = (closes[i2 + fw] - closes[i2]) / closes[i2] * 100
                    Future.append((fw, p1, p2))
    if show_progress:
        pbar.close()

    # aggregate correlations
    corr_map = {}
    for day, p1, p2 in Future:
        corr_map.setdefault(day, []).append((p1, p2))
    days = sorted(corr_map)
    corrs = [_corr(*zip(*corr_map[d])) for d in days] if days else []

    # pick best
    if corrs:
        idx_best = int(np.nanargmax(corrs))
        best_day, best_corr = days[idx_best], corrs[idx_best]
    else:
        best_day, best_corr = None, None

    if plot and corrs:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(days, corrs, linewidth=2)
        ax.set_xlabel("Future Days")
        ax.set_ylabel("Correlation")
        ax.set_title(f"Best corr={best_corr:.2f} at {best_day}d")
        ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
        plt.tight_layout()
        plt.show()

    return best_day, best_corr


# --- 3) match_interval_across --- #

def match_interval_across(data,
                          target_start: str,
                          target_end: str,
                          search_data=None,
                          search_start: str = None,
                          search_end: str = None,
                          future_win: int = 10,
                          param: float = 0.5,
                          kernel: str = "Gaussian",
                          divergence='KL',
                          alpha=0.5,
                          show_progress: bool = False,
                          plot: bool = False):
    """
    Matches the slice [target_start:target_end] from `data` against one or more
    series in `search_data` (file, dir, DataFrame or list), using `divergence`.
    Returns (best_source, best_idx, best_dist, metrics).
    """
    # load reference series
    if isinstance(data, str):
        df_ref = pd.read_csv(data, parse_dates=["Date"], dayfirst=True).sort_values("Date").reset_index(drop=True)
    else:
        df_ref = data.copy().sort_values("Date").reset_index(drop=True)

    # default scan bounds
    if search_start is None:
        search_start = df_ref["Date"].min()
    if search_end is None:
        search_end = df_ref["Date"].max()

    # slice target
    mask_t = (df_ref["Date"] >= target_start) & (df_ref["Date"] <= target_end)
    df_t = df_ref.loc[mask_t].reset_index(drop=True)
    closes_t = df_t["Close"].tolist()
    pct_t = _percent_returns(closes_t)
    L = len(pct_t)

    # global KDE for target
    arr = np.array(pct_t[1:]) if L > 1 else np.zeros(1)
    mg = (arr.max() - arr.min()) * 0.1 if arr.max() != arr.min() else 1
    x_grid = np.linspace(arr.min() - mg, arr.max() + mg, 1000)
    kde_t = _kde(pct_t, x_grid, kernel, param)

    # build source list
    if search_data is None or isinstance(search_data, (str, pd.DataFrame)):
        sources = [search_data or data]
    elif isinstance(search_data, list):
        sources = search_data
    else:
        raise ValueError("`search_data` must be filepath, dir, DataFrame or list thereof")

    expanded = []
    for s in sources:
        if isinstance(s, str) and os.path.isdir(s):
            expanded += sorted(glob.glob(os.path.join(s, "*.csv")))
        else:
            expanded.append(s)
    sources = expanded

    # scan for best match
    best = (None, None, np.inf)
    iterable = tqdm(sources, desc="Scanning") if show_progress else sources
    for src in iterable:
        try:
            if isinstance(src, str):
                df = pd.read_csv(src, parse_dates=["Date"], dayfirst=True)
            else:
                df = src.copy()
        except Exception:
            continue
        if "Date" not in df.columns:
            continue
        df = df.sort_values("Date").reset_index(drop=True)
        df_s = df[(df["Date"] >= search_start) & (df["Date"] <= search_end)].reset_index(drop=True)
        closes = df_s["Close"].tolist()
        pct = _percent_returns(closes)
        for i in range(0, len(pct) - L + 1):
            kde_i = _kde(pct[i: i + L], x_grid, kernel, param)
            d = _divergence(kde_t, kde_i, divergence, alpha)
            if d < best[2]:
                best = (src, i, d)

    best_src, best_idx, best_dist = best
    if best_src is None:
        raise ValueError("No matching interval found.")

    # future metrics
    if isinstance(best_src, str):
        df_m = pd.read_csv(best_src, parse_dates=["Date"], dayfirst=True)
    else:
        df_m = best_src.copy()
    df_m = df_m.sort_values("Date").reset_index(drop=True)
    c = df_m["Close"].tolist()
    last = best_idx + L - 1

    daily = []
    for day in range(1, future_win + 1):
        if last + day < len(c) and c[last] != 0:
            daily.append((c[last + day] - c[last + day - 1]) / c[last + day - 1] * 100)

    percent = daily[future_win - 1] if len(daily) >= future_win else float("nan")
    sum_ret = sum(daily)
    y = [c[last + day] for day in range(future_win + 1) if last + day < len(c)]
    slope = linregress(list(range(len(y))), y).slope if len(y) > 1 else 0
    trend = int(np.sign(slope))
    metrics = {"percent": percent, "sum": sum_ret, "trend": trend}

    # optional combined plot
    if plot:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # overlay reference & matched
        ax1.plot(df_ref["Date"], df_ref["Close"], label="Reference", linewidth=2)
        ax1.plot(df_m["Date"], df_m["Close"], alpha=0.3, label="Scan series", linewidth=1)

        dm = df_m["Date"].tolist()[best_idx: best_idx + L]
        cm = df_m["Close"].tolist()[best_idx: best_idx + L]
        ax1.plot(dm, cm, linewidth=2, label="Matched")

        # highlight boxes
        start_idx = df_ref.index[mask_t][0]
        _add_rect(ax1, df_ref["Date"].tolist(), start_idx, L, df_ref["Close"].tolist(), "red")
        _add_rect(ax1, df_m["Date"].tolist(), best_idx, L, df_m["Close"].tolist(), "green")

        ax1.set_title("Reference & Matched Intervals")
        ax1.legend()

        # future daily returns
        ax2.plot(range(1, len(daily) + 1), daily, marker="o", linewidth=2)
        ax2.set_xlabel("Day After Match")
        ax2.set_ylabel("Daily % Return")
        ax2.set_title(f"Future (sum={sum_ret:.2f}%, trend={trend})")
        ax2.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

        plt.tight_layout()
        plt.show()

    return best_src, best_idx, best_dist, metrics
