from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings

from stock.models.stock import Stock
from stock.models.userstock import UserStock
from shared.helpers.logging_helper import logger
from stock.accessors.stock_accessor import StockPriceAccessor

class StockService:
    CACHE_TIMEOUT= 900 ## in seconds; 15 min
    @staticmethod
    def initialize_stocks():
        """Initialize predefined stocks if not already in DB"""
        for stock_data in settings.AVAILABLE_STOCKS:
            Stock.objects.get_or_create(
                symbol= stock_data['symbol'],
                defaults= {'name':stock_data['name']}
            )
        logger.info("Initialized available stocks")

    @staticmethod
    def set_cache():
        """get all stock"""
        StockService.initialize_stocks()
        stocks= Stock.objects.all()
        for stock in stocks:
            cache_key=f"stock_price_symbol_{stock.symbol}"
            price= StockPriceAccessor.fetch_stock_price(symbol=stock.symbol)
            if price!=None:
                cache.set(cache_key, price, StockService.CACHE_TIMEOUT)     


    @staticmethod
    def get_all_stock_with_prices():
        """get all the stock"""
        stocks= Stock.objects.all()
        stock_list=[]
        for stock in stocks:
            stock_list.append({
                "id":stock.id,
                "symbol":stock.symbol,
                "name":stock.name,
                "created_at":stock.created_at,
                "current_price":StockService.get_or_fetch_stock_price(stock.symbol)
            })
        return stock_list
   
    @staticmethod
    def get_or_fetch_stock_price(symbol):
        """Get price from cache or API"""
        cache_key= f"stock_price_{symbol}"
        cached_price= cache.get(cache_key)
        if cached_price:
            return cached_price
        price= StockPriceAccessor.fetch_stock_price(symbol=symbol)
        if price!=None:
            cache.set(cache_key, price, StockService.CACHE_TIMEOUT)
        return price
    

    @staticmethod 
    def update_stock_prices():
        """Update prices for all stocks"""
        stocks= Stock.objects.all()
        for stock in stocks:
            price= StockService.get_or_fetch_stock_price(stock.symbol)
            if price:
                stock.save_price(price)

    @staticmethod
    def check_and_notify():
        """check limits and notify users"""
        user_stocks= UserStock.objects.select_related('user','stock').all()
        for user_stock in user_stocks:
            price= StockService.get_or_fetch_stock_price(user_stock.stock.symbol)
            if price:
                trigger= user_stock.check_limits(price)
                if trigger:
                    StockService.notify_user(user_stock.stock, user_stock.user, price, trigger)
    
    @staticmethod
    def notify_user(stock, user, price, trigger):
        """Send email notification"""
        subject= f"Stock Price Alert: {stock.symbol}"
        message= f"Your stock {stock.symbol} ({stock.name}) has {trigger}. Current Price: ${price}"

        try:
            send_mail(
                subject,
                message,
                '',
                [user.email],
                fail_silently=False,
            )
            logger.info(f"Notification sent to {user.email} for {stock.symbol}")
        except Exception as e:
            logger.error(f"Failed to send notification to {user.email}: {str(e)}")
    
