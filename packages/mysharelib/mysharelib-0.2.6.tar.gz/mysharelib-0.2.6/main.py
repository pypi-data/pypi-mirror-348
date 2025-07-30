import logging
import streamlit as st
from mysharelib import MyShareData
from mysharelib.utils import setup_logger
from mysharelib.ak_data import get_stock_spot

# Initialize logger
setup_logger()
logger = logging.getLogger(__name__)

# Example usage
logger.info("myshare_lib testing...")

def main():
    st.title("Stock Data Viewer")
    
    # Move text input to top
    symbol = st.text_input("Enter Stock Symbol:", key="symbol")
    
    if symbol:  # Only run if symbol is provided
        try:
            current_data = get_stock_spot(symbol)
            st.write("Current Stock Data:")
            st.write(current_data)
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
    
    # Show historical prices table
    symbols = ['0144.HK', '0386.HK', '0939.HK', '0998.HK', '1288.HK', 
               '1339.HK', '1398.HK', '2800.HK', '2880.HK', '3988.HK', '6823.HK']
    ak_data = MyShareData.from_source('akshare')
    prices = ak_data.get_stock_prices(symbols)
    st.write("Historical Prices:")
    st.table(prices)


if __name__ == "__main__":
    main()
