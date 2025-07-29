from typing import Optional
import webbrowser

from mcp.server.fastmcp import FastMCP

# Server setup
mcp = FastMCP("mercuryo-oor-server")

def validate_type(type_: str) -> None:
    if type_ not in ("buy", "sell"):
        raise ValueError("type must be 'buy' or 'sell'")

def validate_float(val: Optional[object], name: str) -> Optional[float]:
    if val is None:
        return None
    try:
        return float(val)
    except Exception:
        raise ValueError(f"{name} must be a float if provided")

@mcp.tool()
async def mercuryo_exchange_crypto(
    type: str,
    currency: str,
    fiat_currency: str,
    fiat_amount: Optional[float] = None,
    amount: Optional[float] = None,
) -> dict:
    """
    Open Mercuryo exchange in the browser for buying or selling crypto.
    Parameters:
      - type: 'buy' or 'sell' (required)
      - currency: short crypto name (e.g., 'eth', 'btc') (required)
      - fiat_currency: e.g., 'eur', 'usd' (required)
      - fiat_amount: float, optional
      - amount: float, optional
    """
    # Validation
    validate_type(type)
    if not currency:
        raise ValueError("currency is required")
    if not fiat_currency:
        raise ValueError("fiat_currency is required")
    fiat_amount = validate_float(fiat_amount, "fiat_amount")
    amount = validate_float(amount, "amount")

    # Build query params
    params = [
        ("type", type),
        ("currency", currency),
        ("fiat_currency", fiat_currency),
    ]
    if fiat_amount is not None:
        params.append(("fiat_amount", str(fiat_amount)))
    if amount is not None:
        params.append(("amount", str(amount)))
    query = "&".join(f"{k}={v}" for k, v in params)
    url = f"https://exchange.mercuryo.io?{query}"

    # Open browser
    webbrowser.open(url)

    return {"success": True, "url": url}

if __name__ == "__main__":
    mcp.run(transport='stdio')
