# myshare-lib

## **Requirements for `myshare` Library**

#### **1. Core Structure**

- **Abstract Base Class `MyShareData`**
  
  - Defines a standardized interface for fetching financial data (stocks, currencies, etc.).
  
  - Requires subclasses to implement the following abstract methods:
    
    1. `get_stock_history(symbol: str, start_date: str, end_date: str, period: str = "daily", market: str = "SH")`
       - Fetches historical stock price data (open, high, low, close, volume).
       - The return value is an array of dictionary which can be converted to JSON data structure in Restful API design. The dictionary includes (symbol, market, date, open, close, high, low, volume, source). The source indicates akshare, yahoo or cache.
    2. `get_exchange_rate(symbol: str) -> int`
       - Fetches the current exchange rate data for a current pair. The symbol is a pair of exchange rate such as USDCNY.
    3. `validate_symbol(symbol: str) -> bool`
       - Validates the format of a stock/currency symbol.
  
  - `MyShareData` implement a method from_source to create a subclass.
    
    ```python
    class MyShareData():
    @classmethod
    def from_source(cls, source: str, **kwargs) -> "MyShareData":
        """Factory method to create a data source instance."""
        source = source.lower().strip()
        if source == "yahoo":
            return YahooData(**kwargs)
        elif source == "akshare":
            return AKShareData(**kwargs)
        else:
            raise ValueError(f"Unsupported data source: {source}")
    @abstractmethod
    def get_stock_data(symbol: str,
        start_date: str,
        end_date: str,
        period: str = "daily",
        adjust: str = "",
        market: str = "SH"):
        pass
    @abstractmethod
    def get_exchange_rate(self, symbol: str) -> int:
        pass
    @abstractmethod
    def validate_symbol(self, symbol: str) -> bool:
        pass
    ```

- **Subclass `AKShareData`**
  
  - Implements `MyShareData` using the **AKShare** library.
  - Handles AKShare-specific parameters, errors (e.g., network failures), and data formatting.
  - Example override: Map AKShare’s output to a standardized DataFrame structure.

- **Subclass `YahooData`**
  
  - Implements `MyShareData` using **yfinance** (Yahoo Finance).
  - Converts Yahoo’s response (timezone-aware timestamps, column names) to match the base class’s format.

---

#### **2. Key Enhancements**

- **Consistent Output Format**  
  All methods return pandas DataFrames with standardized columns (e.g., `datetime`, `open`, `high`, `low`, `close`, `volume` for stocks; `datetime`, `rate` for currencies).

- **Error Handling**
  
  - Subclasses raise custom exceptions (e.g., `InvalidSymbolError`, `DataSourceError`) for uniformity.
  - Handle API rate limits, timeouts, and data parsing failures gracefully.

- **Extensibility**

- - New data sources (e.g., Alpha Vantage, Quandl) can be added by subclassing `MyShareData`.

## Symbols

Please refer to `docs/symbol.md` for more details.

To create a list of SH, SZ and HK symbols in SQLite database, please run the following command:

```python
(myshare-lib) C:\myshare-lib>python mysharelib\ak_symbols.py
```



## TODO:

- Support SH, SZ and HK in MyShareData