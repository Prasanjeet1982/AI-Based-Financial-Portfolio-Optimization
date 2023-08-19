from fastapi import FastAPI
from fastapi import Request, Form
from fastapi.responses import HTMLResponse
from app import optimize_portfolio

app = FastAPI()

@app.post("/")
async def optimize_portfolio_route(request: Request, tickers: str = Form(...)):
    return await optimize_portfolio(request, tickers)
