import logging
from mysharelib import MyShareData
from mysharelib.utils import setup_logger

# Initialize logger
setup_logger()
logger = logging.getLogger(__name__)

# Example usage
logger.info("myshare_lib testing...")

def main():
    yf = MyShareData.from_source('yahoo')
    ak_data = MyShareData.from_source('akshare')
    #result = ak_data.get_stock_history('0205', '20250421', '20250425')
    #print(result)
    #rate = ak_data.get_exchange_rate('USD/CNY')
    #print(rate)
    symbols = ['300507', '600325']
    #prices = ak_data.get_stock_prices(symbols)
    #symbols = ['0144.HK', '0386.HK', '0939.HK', '0998.HK', '1288.HK', '1339.HK', '1398.HK', '2800.HK', '2880.HK', '3988.HK', '6823.HK']
    prices = ak_data.get_stock_prices(symbols)

    print(prices)


if __name__ == "__main__":
    main()
