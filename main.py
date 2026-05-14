from fastmcp import FastMCP
from polygon import RESTClient
from dotenv import load_dotenv
import os
from typing import Dict, Any
from fastapi import FastAPI
import uvicorn

load_dotenv()

client = RESTClient(api_key=os.getenv("POLYGON_API_KEY"))

mcp = FastMCP()

@mcp.tool
def get_fundamentals(ticker: str) -> Dict[str, Any]:
    """Datos fundamentales para análisis SEPA/Minervini"""
    try:
        snapshot = client.get_snapshot(ticker.upper())
        return {
            "ticker": ticker.upper(),
            "market_cap": getattr(snapshot, 'market_cap', None),
            "eps_ttm": getattr(snapshot, 'eps_ttm', None),
            "revenue_growth": getattr(snapshot, 'revenue_growth', None),
            "profit_margin": getattr(snapshot, 'profit_margin', None),
            "message": "Datos listos para análisis SEPA/Minervini"
        }
    except Exception as e:
        return {"error": str(e)}

# Crear app FastAPI + MCP (obligatorio para Railway)
app = FastAPI()
app.mount("/", mcp.app)   # Esto es lo que faltaba

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
