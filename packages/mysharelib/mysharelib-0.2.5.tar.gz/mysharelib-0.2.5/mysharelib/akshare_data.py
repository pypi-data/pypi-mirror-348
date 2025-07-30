import pandas as pd
from datetime import datetime
from typing import Dict, Any, List
import akshare as ak
from .interfaces import MyShareData, InvalidSymbolError, DataSourceError
from .utils import normalize_symbol, get_symbol_base
from .ak_data import get_stock_history, get_exchange_rates, get_stock_spot

class AKShareData(MyShareData):
    """Implementation of MyShareData using AKShare."""

    def validate_symbol(self, symbol: str) -> bool:
        try:
            symbol, symbol_f, market = normalize_symbol(symbol)
            return True
        except ValueError:
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
            return get_stock_history(symbol, start_date, end_date, period, adjust, market)
        except Exception as e:
            raise DataSourceError(f"Error fetching data from AKShare: {str(e)}")

    def get_exchange_rate(self, symbol: str) -> float:
        try:
            # AKShare uses different format for exchange rates
            rates = get_exchange_rates()
            return rates[symbol]
        except Exception as e:
            raise DataSourceError(f"Error fetching exchange rate from AKShare: {str(e)}")

    def get_stock_prices(
        self,
        symbols: List[str],
        market: str = "SH"
    ) -> Dict[str, Any]:
        try:
            prices = {}
            #stock_data = ak.stock_zh_a_spot_em()
            #stock_hk = ak.stock_hk_spot_em()
            for symbol in symbols:
                symbol, symbol_f, market = normalize_symbol(symbol)
                data = get_stock_spot(symbol)
                prices[symbol] = data['current_price']
                
            return prices
        except Exception as e:
            raise DataSourceError(f"Error fetching stock prices from AKShare: {str(e)}")