import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt
from io import StringIO
from pandas import DataFrame

def optimize_portfolio(request, tickers):
    from data_collection import fetch_data
    
    # Data Preprocessing
    historical_data = fetch_data(tickers, start_date, end_date)
    returns = historical_data.pct_change().dropna()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    risk_free_rate = 0.02

    # Portfolio Optimization
    weights = cp.Variable(len(assets))
    expected_return = mean_returns @ weights
    risk = cp.quad_form(weights, cov_matrix)
    objective = cp.Maximize(expected_return - risk_free_rate * risk)
    constraints = [cp.sum(weights) == 1, weights >= 0]
    problem = cp.Problem(objective, constraints)
    problem.solve()

    optimal_weights = weights.value

    # Visualization
    target_returns = np.linspace(mean_returns.min(), mean_returns.max(), num=100)
    efficient_portfolios = []
    for target_return in target_returns:
        constraints = [cp.sum(weights) == 1, expected_return == target_return, weights >= 0]
        problem = cp.Problem(cp.Minimize(risk), constraints)
        problem.solve()
        efficient_portfolios.append((target_return, np.sqrt(risk.value)))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter([p[1] for p in efficient_portfolios], [p[0] for p in efficient_portfolios], marker='o')
    ax.set_xlabel('Risk (Standard Deviation)')
    ax.set_ylabel('Expected Return')
    ax.set_title('Efficient Frontier')
    plt.grid(True)

    img_buf = StringIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    plt.close()

    return HTMLResponse(content=f"<img src='data:image/png;base64,{img_buf.getvalue()}'/>")
