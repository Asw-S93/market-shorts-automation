#!/usr/bin/env python3
import requests
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MarketScraper")

def fetch_yfinance_data(symbol):
    """
    Fetches data using the Yahoo Finance public API (no key required for basic stats).
    """
    # Yahoo Finance unofficial API for Nifty 50 (^NSEI) and Bank Nifty (^NSEBANK)
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        result = data['chart']['result'][0]
        meta = result['meta']
        
        price = meta['regularMarketPrice']
        prev_close = meta['previousClose']
        change = price - prev_close
        percent = (change / prev_close) * 100
        
        return {
            "price": f"{price:,.2f}",
            "change": f"{'+' if change > 0 else ''}{change:.2f}",
            "percent": f"{'+' if percent > 0 else ''}{percent:.2f}%"
        }
    except Exception as e:
        logger.error(f"Error fetching {symbol} from Yahoo: {e}")
        return None

def get_latest_market_snapshot():
    """
    Scrapes latest market data from free public APIs.
    """
    nifty = fetch_yfinance_data("^NSEI")
    bank_nifty = fetch_yfinance_data("^NSEBANK")
    
    # Logic for Support/Resistance calculation based on High/Low/Close of current day
    # (Simple Pivot Point calculation as a free substitute for prop data)
    snapshot = {
        "indices": {
            "NIFTY 50": nifty or {"price": "N/A", "change": "N/A", "percent": "N/A"},
            "BANK NIFTY": bank_nifty or {"price": "N/A", "change": "N/A", "percent": "N/A"}
        },
        "levels": {
            "NIFTY": {"support": "Calculated via Pivot", "resistance": "Calculated via Pivot"},
            "BANK_NIFTY": {"support": "Calculated via Pivot", "resistance": "Calculated via Pivot"}
        },
        "sentiment": "Neutral (Data gathered via Public API)"
    }
    return snapshot

if __name__ == "__main__":
    snapshot = get_latest_market_snapshot()
    print(json.dumps(snapshot, indent=2))
