from celery import shared_task

from stock.services.stock_service import StockService

@shared_task 
def update_stock_prices_task():
    """periodic task to update stock prices and notify"""
    StockService.update_stock_prices()
    StockService.check_and_notify()