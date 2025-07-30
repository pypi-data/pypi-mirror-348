from datetime import datetime
from typing import Dict, Any, List
import yfinance as yf
from .interfaces import MyShareData, InvalidSymbolError, DataSourceError

class YahooData(MyShareData):
    """Implementation of MyShareData using yfinance."""

    def validate_symbol(self, symbol: str) -> bool:
        try:
            ticker = yf.Ticker(symbol)
            # Try to fetch info to validate the symbol
            info = ticker.info
            return True
        except:
            return False

    def get_stock_history(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        period: str = "daily",
        adjust: str = "",
        market: str = "SH"
    ) -> List[Dict[str, Any]]:
        try:
            # Convert YYYYMMDD to YYYY-MM-DD for yfinance
            start = datetime.strptime(start_date, "%Y%m%d").strftime("%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y%m%d").strftime("%Y-%m-%d")
            
            # Map period to yfinance interval
            interval_map = {
                "daily": "1d",
                "weekly": "1wk",
                "monthly": "1mo"
            }
            interval = interval_map.get(period, "1d")
            
            ticker = yf.Ticker(symbol)
            df = ticker.history(start=start, end=end, interval=interval)
            
            result = []
            for date, row in df.iterrows():
                result.append({
                    "symbol": symbol,
                    "market": market,
                    "date": date,
                    "open": float(row["Open"]),
                    "close": float(row["Close"]),
                    "high": float(row["High"]),
                    "low": float(row["Low"]),
                    "volume": float(row["Volume"]),
                    "source": "yahoo"
                })
            return result
        except Exception as e:
            raise DataSourceError(f"Error fetching data from Yahoo Finance: {str(e)}")

    def get_exchange_rate(self, symbol: str) -> float:
        try:
            # Yahoo uses -=X suffix for forex pairs
            ticker = yf.Ticker(f"{symbol}=X")
            data = ticker.history(period="1d")
            if data.empty:
                raise InvalidSymbolError(f"Currency pair {symbol} not found")
            return float(data['Close'].iloc[-1])
        except Exception as e:
            raise DataSourceError(f"Error fetching exchange rate from Yahoo Finance: {str(e)}")
        
    def get_stock_prices(
        self,
        symbols: List[str],
        market: str = "SH"
    ) -> Dict[str, Any]:
        try:
            prices = {}
            for symbol in symbols:
                ticker = yf.Ticker(symbol)
                data = ticker.history(period="1d")
                if data.empty:
                    raise InvalidSymbolError(f"Invalid symbol: {symbol}")
                prices[symbol] = float(data['Close'].iloc[-1])
            return prices
        except Exception as e:
            raise DataSourceError(f"Error fetching stock prices from Yahoo Finance: {str(e)}")