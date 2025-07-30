import matplotlib.pyplot as plt
import pandas as pd
import os

class PortfolioPlotter:
    @staticmethod
    def _savefig(filename: str):
        """Helper to ensure the target directory exists before saving a figure."""
        if filename:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
        plt.savefig(filename)

    @staticmethod
    def plot_drawdown(drawdown):
        plt.figure(figsize=(10, 4))
        drawdown.plot(title='Drawdown of Max Sharpe Portfolio', color='blue')
        plt.ylabel('Drawdown')
        plt.xlabel('Date')
        plt.grid(True)
        plt.tight_layout()
        PortfolioPlotter._savefig("reports/drawdown_plot.png")
        plt.close()

    @staticmethod
    def plot_equity_curve(equity_curve):
        drawdown = equity_curve / equity_curve.cummax() - 1
        fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

        # Plot equity curve
        axs[0].plot(equity_curve, color='green')
        axs[0].set_title('Equity Curve of Max Sharpe Portfolio')
        axs[0].set_ylabel('Portfolio Value')
        axs[0].grid(True)

        # Plot drawdown
        axs[1].plot(drawdown, color='red')
        axs[1].set_title('Drawdown Curve')
        axs[1].set_ylabel('Drawdown')
        axs[1].set_xlabel('Date')
        axs[1].grid(True)

        plt.tight_layout()
        PortfolioPlotter._savefig("reports/equity_and_drawdown_plot.png")
        plt.close()

    @staticmethod
    def plot_efficient_frontier(port_vols, port_returns, sharpe_ratios, ef_vols, ef_returns, max_sharpe_idx, filename="reports/efficient_frontier_plot.png"):
        plt.figure(figsize=(10, 6))
        plt.scatter(port_vols, port_returns, c=sharpe_ratios, cmap='viridis', alpha=0.6)
        plt.colorbar(label='Sharpe Ratio')
        plt.scatter(port_vols[max_sharpe_idx], port_returns[max_sharpe_idx], c='red', label='Max Sharpe', s=100)
        plt.plot(ef_vols, ef_returns, color='black', label='Efficient Frontier', linewidth=2)
        plt.xlabel('Volatility')
        plt.ylabel('Expected Return')
        plt.legend()
        plt.title('Efficient Frontier with Random Portfolios')
        plt.grid(True)
        PortfolioPlotter._savefig(filename)
        plt.close()

    @staticmethod
    def plot_asset_prices(price):
        plt.figure(figsize=(12, 6))
        price.plot(title="Asset Prices Over Time")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.grid(True)
        plt.tight_layout()
        PortfolioPlotter._savefig("reports/asset_prices_plot.png")
        plt.close()

    @staticmethod
    def plot_portfolio_margin(margin_per_year, filename="reports/portfolio_margin_per_year.png"):
        margin_series = pd.Series(margin_per_year).sort_index()
        plt.figure(figsize=(10, 4))
        margin_series.plot(kind='bar', title='Portfolio Margin (Concentration) Per Year')
        plt.ylabel('Margin (Σ weights²)')
        plt.xlabel('Year')
        plt.grid(True)
        plt.tight_layout()
        PortfolioPlotter._savefig(filename)
        plt.close()

    @staticmethod
    def plot_portfolio_allocation(annual_weights, filename="reports/portfolio_allocation_per_year.png"):
        weights_df = pd.DataFrame(annual_weights).T.sort_index()
        plt.figure(figsize=(12, 6))
        weights_df.plot(kind='bar', stacked=True)
        plt.title("Annual Portfolio Allocation (Stock Weights)")
        plt.ylabel("Weight")
        plt.xlabel("Year")
        plt.legend(title="Ticker", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        PortfolioPlotter._savefig(filename)
        plt.close()

    @staticmethod
    def plot_equity_vs_benchmark(equity_curve, benchmark_price, filename="reports/equity_vs_benchmark_plot.png"):
        plt.figure(figsize=(12, 6))
        norm_equity = equity_curve / equity_curve.iloc[0]
        norm_benchmark = benchmark_price / benchmark_price.iloc[0]
        norm_equity.plot(label="Portfolio")
        norm_benchmark.plot(label="SPY Benchmark")
        plt.title("Portfolio vs. Benchmark (SPY)")
        plt.ylabel("Normalized Value")
        plt.xlabel("Date")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        PortfolioPlotter._savefig(filename)
        plt.close()