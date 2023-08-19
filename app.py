from fastapi import Request, Form
from fastapi.responses import HTMLResponse
from data_collection import fetch_data
from portfolio_optimization import optimize_portfolio

app = FastAPI()

@app.post("/")
async def optimize_portfolio_route(request: Request, tickers: str = Form(...)):
    return await optimize_portfolio(request, tickers)
