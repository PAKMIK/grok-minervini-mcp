from fastmcp import FastMCP
from polygon import RESTClient
from dotenv import load_dotenv
import os
from typing import Dict, Any
load_dotenv()
client = RESTClient(api_key=os.getenv("POLYGON_API_KEY"))
mcp = FastMCP()
@mcp.tool
def get_fundamentals(ticker: str) -> Dict[str, Any]:
    """Datos fundamentales para analizar empresas (EPS, ventas, márgenes) estilo Minervini"""
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

if __name__ == "__main__":
    print("🚀 SEPA Minervini Fundamentals MCP corriendo en puerto 8000")
    mcp.run(port=8000)
