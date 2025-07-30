
"""Main CLI and programmatic entry point for portfolio-opt.

Exposes `run_annual_rebalanced_backtest` for library usage and provides
a thin command‑line interface via the ``portfolio-opt`` console script.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

import cvxpy as cp
import numpy as np
import pandas as pd
import vectorbt as vbt

from portfolio_opt.portfolio_backtester import PortfolioBacktester
from portfolio_opt.portfolio_plotter import PortfolioPlotter


# ---------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------
def construct_efficient_frontier(
    returns: pd.DataFrame,
    tickers: List[str],
    num_points: int = 100,
) -> tuple[list[float], list[float]]:
    """Compute efficient‑frontier coordinates (expected return, volatility)."""
    mus = (returns.mean() * 252).values
    cov = returns.cov().values * 252
    target_returns = np.linspace(mus.min(), mus.max(), num_points)

    ef_returns, ef_vols = [], []
    for target in target_returns:
        w = cp.Variable(len(tickers))
        risk = cp.quad_form(w, cov)
        constraints = [
            cp.sum(w) == 1,
            w >= 0,
            mus @ w >= target,
        ]
        try:
            prob = cp.Problem(cp.Minimize(risk), constraints)
            prob.solve()
            if w.value is None:
                raise ValueError("Infeasible solution")
            ef_returns.append(target)
            ef_vols.append(np.sqrt(risk.value))
        except Exception as exc:
            print(f"⚠️  Optimization failed at target {target:.4f}: {exc}")
            continue
    return ef_returns, ef_vols


def summarize_equity_curve(
    equity_curve: pd.Series,
    returns: pd.DataFrame,
    risk_free_rate: float,
):
    """Return a summary dictionary and the underlying PortfolioBacktester."""
    weights = np.ones(len(returns.columns)) / len(returns.columns)
    bt = PortfolioBacktester(
        returns,
        weights,
        initial_value=equity_curve.iloc[0],
    ).run()
    bt.equity_curve = equity_curve
    summary = bt.summary(risk_free_rate=risk_free_rate)
    return summary, bt


def format_summary_df(df: pd.DataFrame, percent_cols: set[str]) -> pd.DataFrame:
    """Nicely format %, float columns for CSV/stdout."""
    formatted = df.copy()
    for col in formatted.columns:
        formatted[col] = formatted[col].apply(
            (lambda x: f"{x:.2%}") if col in percent_cols else (lambda x: f"{x:.4f}")
        )
    return formatted


# ---------------------------------------------------------------------
# Core routine
# ---------------------------------------------------------------------
def run_annual_rebalanced_backtest(
    tickers: List[str],
    start_date: str,
    end_date: str,
    benchmark_ticker: str = "SPY",
    initial_value: float = 1_000_000,
    risk_free_rate: float = 0.03,
    num_random_ports: int = 10_000,
    seed: int = 42,
    rebalance_freq: str = "YE",  # "YE"=yearly, "6M"=semi‑annual, "3M" or "Q"=quarterly
) -> None:
    """Run a max‑Sharpe backtest with configurable rebalancing frequency (`A`, `6M`, `Q`/`3M`)."""
    # Prepare output dirs
    Path("reports/efficient_frontier").mkdir(parents=True, exist_ok=True)
    Path("exports").mkdir(exist_ok=True)

    if rebalance_freq not in {"YE", "6M", "Q", "3M"}:
        raise ValueError("rebalance_freq must be one of 'YE', '6M', 'Q', or '3M'")

    # Market data
    price = (
        vbt.YFData.download(tickers, start=start_date, end=end_date)
        .get("Close")
        .dropna(how="any")
    )
    benchmark_price = (
        vbt.YFData.download(benchmark_ticker, start=start_date, end=end_date)
        .get("Close")
        .dropna()
    )
    benchmark_returns = benchmark_price.pct_change(fill_method=None).dropna().to_frame(
        name=benchmark_ticker
    )
    returns = price.pct_change(fill_method=None).dropna(how="any")

    print("\n📅 Running annual rebalancing backtest...")
    np.random.seed(seed)
    all_equity = pd.Series(dtype=float)
    yearly_summaries: dict[int, dict] = {}
    annual_weights: dict[int, dict[str, float]] = {}

    # -----------------------------------------------------------------
    # Period‑by‑period optimisation & backtest (frequency = rebalance_freq)
    # -----------------------------------------------------------------
    period_groups = returns.groupby(pd.Grouper(freq=rebalance_freq))
    for period_start, period_returns in period_groups:
        if period_returns.empty or len(period_returns) < 50:
            continue

        # Human‑readable label (used for dict keys & filenames)
        if rebalance_freq == "YE":
            label = str(period_start.year)
        else:
            label = f"{period_start.strftime('%Y%m%d')}_{period_returns.index[-1].strftime('%Y%m%d')}"

        # Random portfolios for this period
        weights = np.random.dirichlet(np.ones(len(tickers)), size=num_random_ports)
        port_returns = np.dot(weights, period_returns.mean()) * 252
        port_vols = (
            np.sqrt(np.diag(weights @ period_returns.cov().values @ weights.T))
            * np.sqrt(252)
        )
        sharpe = (port_returns - risk_free_rate) / port_vols
        max_idx = sharpe.argmax()
        opt_weights = weights[max_idx]
        annual_weights[label] = dict(zip(tickers, opt_weights))

        # Efficient frontier plot
        ef_ret, ef_vol = construct_efficient_frontier(period_returns, tickers)
        PortfolioPlotter.plot_efficient_frontier(
            port_vols,
            port_returns,
            sharpe,
            ef_vol,
            ef_ret,
            max_idx,
            filename=f"reports/efficient_frontier/efficient_frontier_{label}.png",
        )

        # Backtest with optimal weights
        init_val = all_equity.iloc[-1] if not all_equity.empty else initial_value
        bt = PortfolioBacktester(period_returns, opt_weights, initial_value=init_val).run()
        all_equity = (
            pd.concat([all_equity, bt.equity_curve])
            if not all_equity.empty
            else bt.equity_curve
        )
        yearly_summaries[label] = bt.summary(risk_free_rate=risk_free_rate)

    # Plots & exports
    margin = {y: np.sum(np.square(list(w.values()))) for y, w in annual_weights.items()}
    PortfolioPlotter.plot_portfolio_margin(margin)
    PortfolioPlotter.plot_portfolio_allocation(annual_weights)
    PortfolioPlotter.plot_equity_curve(all_equity)
    PortfolioPlotter.plot_equity_vs_benchmark(all_equity, benchmark_price)

    all_equity.to_csv("exports/annual_rebalanced_equity.csv")

    percent_cols = {"Total Return", "CAGR", "Volatility", "Max Drawdown", "CVaR (95%)"}
    summary, _ = summarize_equity_curve(
        all_equity,
        all_equity.pct_change().dropna().to_frame(name="Portfolio"),
        risk_free_rate,
    )
    format_summary_df(pd.DataFrame([summary]), percent_cols).to_csv(
        "exports/full_backtest_summary.csv", index=False
    )

    bench_bt = PortfolioBacktester(
        benchmark_returns, np.array([1.0]), initial_value=initial_value
    ).run()
    format_summary_df(
        pd.DataFrame([bench_bt.summary(risk_free_rate=risk_free_rate)]), percent_cols
    ).to_csv("exports/benchmark_summary.csv", index=False)

    format_summary_df(pd.DataFrame(yearly_summaries).T, percent_cols).to_csv(
        "exports/annual_summary.csv"
    )
    if annual_weights:
        pd.DataFrame(annual_weights).T.to_csv("exports/annual_weights.csv")

    # Console output
    print("\n📊 Backtest Summary (Annual Rebalanced Portfolio):")
    for k, v in summary.items():
        print(f"{k}: {v:.2%}" if k in percent_cols else f"{k}: {v:.4f}")
    print("\n📊 Benchmark Summary:")
    print(
        format_summary_df(
            pd.DataFrame([bench_bt.summary(risk_free_rate=risk_free_rate)]),
            percent_cols,
        ).to_string(index=False)
    )
    print("\n📊 Annual Summary:")
    print(
        format_summary_df(pd.DataFrame(yearly_summaries).T, percent_cols).to_string()
    )
    if annual_weights:
        print("\n📊 Annual Portfolio Weights:")
        print(pd.DataFrame(annual_weights).T)


# ---------------------------------------------------------------------
# CLI wrapper
# ---------------------------------------------------------------------
def main() -> None:
    """CLI entry point for the ``portfolio-opt`` console script."""
    parser = argparse.ArgumentParser(
        description="Run an annual rebalanced max‑Sharpe backtest."
    )
    parser.add_argument(
        "--tickers",
        nargs="+",
        default=[
            "AAPL",
            "MSFT",
            "AMZN",
            "META",
            "GOOGL",
            "NVDA",
            "BRK-B",
            "V",
            "JNJ",
            "HCA",
        ],
        help="Tickers to include in the universe.",
    )
    parser.add_argument("--start-date", default="2019-01-01", help="Start date (YYYY-MM-DD).")
    parser.add_argument("--end-date", default="2024-12-31", help="End date (YYYY-MM-DD).")
    parser.add_argument("--benchmark", default="SPY", help="Benchmark ticker.")
    parser.add_argument("--initial-value", type=float, default=1_000_000, help="Initial capital.")
    parser.add_argument("--rf", type=float, default=0.03, help="Annualised risk‑free rate.")
    parser.add_argument(
        "--num-ports",
        type=int,
        default=10_000,
        help="Number of random portfolios sampled each year.",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument(
        "--rebalance",
        default="YE",
        choices=["YE", "6M", "Q", "3M"],
        help="Rebalance frequency: A=annual (default), 6M=semi‑annual, Q or 3M=quarterly.",
    )
    args = parser.parse_args()

    run_annual_rebalanced_backtest(
        tickers=args.tickers,
        start_date=args.start_date,
        end_date=args.end_date,
        benchmark_ticker=args.benchmark,
        initial_value=args.initial_value,
        risk_free_rate=args.rf,
        num_random_ports=args.num_ports,
        seed=args.seed,
        rebalance_freq=args.rebalance,
    )


if __name__ == "__main__":
    main()
