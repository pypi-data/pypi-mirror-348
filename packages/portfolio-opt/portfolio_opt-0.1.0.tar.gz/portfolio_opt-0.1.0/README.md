# 📈 Portfolio Optimization & Backtesting

A lightweight and modular framework for backtesting quantitative portfolio strategies using **configurable rebalancing (annual / 6‑month / quarterly)**, **efficient frontier analysis**, and **Sharpe ratio optimization**.

---

## 📖 Documentation

Explore the full documentation here: 📘 [Read the Docs](https://ohmji.github.io/portfolio-optimization)

## 📦 Installation

```bash
pip install portfolio-opt
# or, with Poetry
poetry add portfolio-opt
```

---

## 🚀 Features

- ✅ Downloads historical stock data from Yahoo Finance via `vectorbt`
- ✅ Samples 10,000 random portfolios per rebalance period
- ✅ Selects the **maximum Sharpe ratio portfolio** each rebalance period
- ✅ Flexible `--rebalance` flag (`A`, `6M`, `Q`/ `3M`) to control rebalancing frequency
- ✅ Computes and plots the **Efficient Frontier** using `cvxpy`
- ✅ Tracks performance vs. benchmark (`SPY`)
- ✅ Exports detailed reports: PNG plots and CSV summaries

---

## 🗂️ Project Structure

```
portfolio-opt/
├── src/
│   └── portfolio_opt/
│       ├── __init__.py
│       ├── main.py               # CLI + library entry points
│       ├── portfolio_backtester.py
│       └── portfolio_plotter.py
├── reports/                      # Auto‑generated plots (.png)
└── exports/                      # Auto‑generated summaries (.csv)
```

| Module                     | Description                                         |
|---------------------------|-----------------------------------------------------|
| `main.py`                 | Coordinates data loading, optimization, backtest    |
| `portfolio_backtester.py` | Runs backtests and computes risk/return metrics     |
| `portfolio_plotter.py`    | All portfolio and asset visualizations              |

---

## 🛠️ Tools & Libraries

| Tool            | Role                                  |
|-----------------|----------------------------------------|
| Python 3.13     | Core language                         |
| Poetry          | Dependency & environment management   |
| vectorbt        | Market data ingestion & helpers       |
| cvxpy           | Portfolio optimization engine         |
| pandas / numpy  | Data analysis                         |
| matplotlib      | Chart rendering                       |

---

## ⚡ Quick Start

```bash
# Run via the CLI (recommended)
portfolio-opt --tickers AAPL MSFT NVDA --start-date 2020-01-01 --end-date 2024-12-31 --rebalance 6M

# Or call programmatically
python - << 'PY'
from portfolio_opt.main import run_annual_rebalanced_backtest

run_annual_rebalanced_backtest(
    tickers=["AAPL", "MSFT", "NVDA"],
    start_date="2020-01-01",
    end_date="2024-12-31",
)
PY
```

### Output Files:
| Folder | Output |
|--------|--------|
| `reports/` | Efficient frontier charts, equity curves, drawdown |
| `exports/` | CSV files for annual summaries, weights, benchmark |

---

## ⚙️ Configuration Tips

| Feature | How to change |
|--------|----------------|
| Tickers | `--tickers` CLI flag **or** pass `tickers=[...]` to `run_annual_rebalanced_backtest` |
| Risk‑Free Rate | `--rf` CLI flag **or** `risk_free_rate=` param |
| Portfolio Samples | `--num-ports` CLI flag |
| Rebalance Frequency | `--rebalance` CLI flag (`A`, `6M`, `Q`/ `3M`) **or** function param `rebalance_freq=` |
| Date Range | `--start-date` / `--end-date` flags or function params |

---

## 🔧 Possible Extensions

1. **Live Trading** – Integrate with live modules from `vectorbt` or `QuantConnect`
2. **Factor Models** – Score stocks on valuation, momentum, etc., instead of random
3. **Risk Constraints** – Add CVaR, max drawdown, or concentration limits
4. **Visualization Dashboard** – Use Streamlit, Dash, or Jupyter for dynamic charts

---

## 📜 License

**MIT License** – Free to use and modify. Attribution appreciated.

---

> _"In investing, what is comfortable is rarely profitable." – Robert Arnott_

Enjoy building your own quantitative strategies! 🎯