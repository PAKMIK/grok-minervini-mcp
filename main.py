# cache-bust: force clean rebuild to ensure all dependencies are installed
from fastmcp import FastMCP
from fastapi import FastAPI
from polygon import RESTClient
from dotenv import load_dotenv
import os
from typing import Dict, Any

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

app = FastAPI(title="SEPA Minervini Fundamentals MCP")
app.mount("/", mcp.http_app())

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 SEPA Minervini Fundamentals MCP corriendo en puerto {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
