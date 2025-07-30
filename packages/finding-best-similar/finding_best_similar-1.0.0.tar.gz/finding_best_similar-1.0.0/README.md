# Finding Best Similar (FBS) Method
## Ali Forouzan, Hadi Sadoghi Yazdi

A Python package for finding similar patterns in time series data using Kernel Density Estimation (KDE) and computing future-trend behavior factors.

## Installation

```bash
pip install finding_best_similar
```

## Features

- 🔍 **Windowed KDE** for time series percent-returns  
- 🔗 **Pattern matching** via customizable divergence metrics (KL, JSD, Hellinger, Entropy, Renyi)  
- 📈 **Behavior scoring** by correlating future percent-return trajectories  
- 📊 **Built-in plotting** of raw series, matched intervals, and future trends  

## Quick Start

```python
import finding_best_similar

# 1) Match an 11-day slice (2021-06-01 → 2021-06-11) against the same file,
#    using Jensen–Shannon divergence (alpha only matters for Renyi)
best_file, idx, dist, metrics = finding_best_similar.match_interval_across(
    "formatted_price.csv",
    target_start="2021-06-01",
    target_end="2021-06-11",
    search_start="2020-06-12",
    search_end="2021-06-11",
    future_win=10,
    divergence="JSD",
    alpha=0.5,  # ignored for JSD
    show_progress=True,
    plot=True,
)
print("Matched file:      ", best_file)
print("Match starts at idx:", idx)
print(f"JSD distance:       {dist:.4f}")
print("Future metrics:     ", metrics)
# → metrics == {'percent': …, 'sum': …, 'trend': …}

# 2) Find best-similar windows in the same file using Hellinger distance
i1, i2, dist = finding_best_similar.best_similar(
    "formatted_price.csv",
    start_time="2019-06-11",
    end_time="2020-06-11",
    divergence="HELLINGER_DISTANCE",
    show_progress=True,
    plot=True,
)
print(f"Best windows at {i1} & {i2}, Hellinger={dist:.4f}")

# 3) Compute behavior score with Renyi divergence (α=0.8)
best_day, best_corr = finding_best_similar.behavior_score(
    "formatted_price.csv",
    start_time="2019-06-11",
    end_time="2020-06-11",
    threshold=0.3,
    divergence="RENYI",
    alpha=0.8,
    show_progress=True,
    plot=True,
)
print(f"Best future window: {best_day} days (corr = {best_corr:.2f})")
```

### Explanation of Outputs

- **percent**: percent change on the _future_win_-th day after match  
- **sum**: sum of daily percent-returns over that horizon  
- **trend**: sign of linear slope through future prices (1 = up, 0 = neutral, –1 = down)  

## Requirements

- **Python** 
- **NumPy**
- **pandas** 
- **matplotlib**
- **tqdm**
- **scipy** 

## License

This project is licensed under the MIT License.
