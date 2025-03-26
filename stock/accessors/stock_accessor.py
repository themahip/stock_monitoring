import requests
from decimal import Decimal
from django.conf import settings  


from shared.helpers.logging_helper import logger

class StockPriceAccessor:
    BASE_URL= "https://www.alphavantage.co/query"
    API_KEY = settings.ALPHA_VANTAGE_API_KEY

    @staticmethod 
    def fetch_stock_price(symbol):
        """fetch stock price from Alpha Ventage"""
        try:
            params={
                'function':'TIME_SERIES_INTRADAY',
                'symbol':symbol,
                'interval':'15min',
                'apikey': StockPriceAccessor.API_KEY
            }
            response= requests.get(StockPriceAccessor.BASE_URL, params=params)
            response.raise_for_status()
            data= response.json()

            time_series= data.get('Time Series (15min)', {})
            if not time_series:
                raise ValueError("No Price data returned")
            latest_time= sorted(time_series.keys())[0]
            price= Decimal(time_series[latest_time]['4. close'])
            logger.info(f"Fetched price ${price} for {symbol}")
            print(price)
            print(type(price))
            return price
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}:{str(e)}")
            return None
