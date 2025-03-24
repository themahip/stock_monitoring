from django.conf import settings
from django.db import models

from shared.helpers.logging_helper import logger
from stock.models.base import BaseStockModel

class Stock(BaseStockModel):
    symbol= models.CharField(max_length=10, unique=True)
    name= models.CharField(max_length=100)

    def __str__(self):
        return self.symbol
    
    def save_price(self, price):
        """sace current price to StockPrice"""
        StockPrice.objects.create(Stock=self, price= price)
        logger.info(f"Price ${price} saved for stock {self.symbol}")

class StockPrice(models.Model):
    stock= models.ForeignKey(Stock, on_delete=models.CASCADE)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    timestamp= models.DateTimeField(auto_now_add=True)

