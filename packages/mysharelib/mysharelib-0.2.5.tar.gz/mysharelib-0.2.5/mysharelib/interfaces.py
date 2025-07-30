from abc import ABC, abstractmethod
from typing import Dict, Any, List

class InvalidSymbolError(Exception):
    """Raised when a symbol format is invalid."""
    pass

class DataSourceError(Exception):
    """Raised when there's an error with the data source."""
    pass

class MyShareData(ABC):
    """Abstract base class for financial data sources."""

    @classmethod
    def from_source(cls, source: str, **kwargs) -> "MyShareData":
        """Factory method to create a data source instance."""
        from .akshare_data import AKShareData
        from .yahoo_data import YahooData
        
        source = source.lower().strip()
        if source == "yahoo":
            return YahooData()
        elif source == "akshare":
            return AKShareData()
        else:
            raise ValueError(f"Unsupported data source: {source}")

    @abstractmethod
    def get_stock_prices(
        self,
        symbols: List[str],
        market: str = "SH"
    ) -> Dict[str, Any]:
        """
        Get stock prices for given symbols.
        
        Args:
            symbols: List of stock symbols to query
            market: Market identifier (SH, SZ, etc.)
            
        Returns:
            Dictionary mapping each symbol to its current price data,
            including:
            - symbol (str): Stock symbol
            - price (float): Current trading price
            
        Raises:
            InvalidSymbolError: If any symbol format is invalid
            DataSourceError: If there's an error retrieving data
        """
        pass

    @abstractmethod
    def get_stock_history(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        period: str = "daily",
        adjust: str = "",
        market: str = "SH"
    ) -> List[Dict[str, Any]]:
        """
        Get historical stock data.
        
        Args:
            symbol: Stock symbol
            start_date: Start date in YYYYMMDD format
            end_date: End date in YYYYMMDD format
            period: Data frequency (daily, weekly, monthly)
            adjust: Price adjustment type
            market: Market identifier (SH, SZ, etc.)
            
        Returns:
            List of dictionaries containing historical data
        """
        pass

    @abstractmethod
    def get_exchange_rate(self, symbol: str) -> float:
        """
        Get current exchange rate for a currency pair.
        
        Args:
            symbol: Currency pair (e.g., 'SGD/CNY', 'USD/CNY', 'AUD/CNY', 'HKGD/CNY')
            
        Returns:
            Current exchange rate
        """
        pass

    @abstractmethod
    def validate_symbol(self, symbol: str) -> bool:
        """
        Validate a stock or currency symbol format.
        
        Args:
            symbol: Symbol to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
