import numpy as np
import pandas as pd

# PortfolioBacktester class for backtesting portfolio strategies
class PortfolioBacktester:
    def __init__(self, returns, weights, initial_value=1_000_000, start_date=None, end_date=None):
        self.weights = weights
        self.returns = returns
        self.initial_value = initial_value
        self.start_date = start_date
        self.end_date = end_date
        self.daily_returns = None
        self.equity_curve = None

    def run(self):
        assert np.isclose(self.weights.sum(), 1), "Weights must sum to 1"
        assert (self.weights >= 0).all(), "Weights must be non-negative"
        self.daily_returns = self.returns @ self.weights
        equity_curve = pd.Series((1 + self.daily_returns).cumprod() * self.initial_value)
        drawdown = equity_curve / equity_curve.cummax() - 1
        self.drawdown = drawdown
        self.max_drawdown = drawdown.min()
        self.equity_curve = equity_curve
        downside_returns = self.daily_returns[self.daily_returns < 0]
        self.var_95 = -np.percentile(self.daily_returns, 5)
        self.cvar_95 = -downside_returns[downside_returns <= -self.var_95].mean()
        return self

    def summary(self, risk_free_rate=0.03):
        if self.equity_curve is None:
            raise ValueError("Equity curve not found. Please run backtest first.")
        total_return = self.equity_curve.iloc[-1] / self.equity_curve.iloc[0] - 1
        cagr = (self.equity_curve.iloc[-1] / self.equity_curve.iloc[0]) ** (1 / (len(self.equity_curve) / 252)) - 1
        volatility = self.daily_returns.std() * np.sqrt(252)
        sharpe = (self.daily_returns.mean() * 252 - risk_free_rate) / volatility

        summary_dict = {
            'Total Return': total_return,
            'CAGR': cagr,
            'Volatility': volatility,
            'Sharpe Ratio': sharpe,
            'Max Drawdown': self.max_drawdown,
            'CVaR (95%)': self.cvar_95
        }

        return summary_dict
