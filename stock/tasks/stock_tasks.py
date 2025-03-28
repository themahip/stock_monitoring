from celery import shared_task
from shared.helpers.logging_helper import logger
from stock.services.stock_service import StockService  # Make sure StockService is correctly imported

@shared_task(name="execute_stock_task")
def update_stock_price():
    """Periodic task to update stock prices and notify users"""
    try:
        StockService.update_stock_prices()
        StockService.check_and_notify()
    except Exception as e:
        logger.info(f"Error executing task: {str(e)}")

@shared_task(name="execute_stock_task")
def execute_stock_task():
    """task to save stock periodically in cache"""
    try:
        stocks= StockService.set_cache()
    except Exception as e:
        print(f"Error executing task: {str(e)}")