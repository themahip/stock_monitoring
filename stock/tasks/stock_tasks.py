from celery import shared_task
from stock.services.stock_service import StockService  # Make sure StockService is correctly imported

@shared_task(name="execute_stock_task")
def execute_stock_task():
    """Periodic task to update stock prices and notify users"""
    print("Executing task...")
    try:
        StockService.update_stock_prices()
        StockService.check_and_notify()
        print("Stock prices updated and notifications sent.")
    except Exception as e:
        print(f"Error executing task: {str(e)}")
