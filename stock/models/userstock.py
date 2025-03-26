from django.db import models

from user.models.user import User
from .base import BaseStockModel
from .stock import Stock

class UserStock(BaseStockModel):
    user= models.ForeignKey(User ,on_delete=models.CASCADE)
    stock= models.ForeignKey(Stock, on_delete=models.CASCADE)
    upper_limit= models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lower_limit= models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together=('user', 'stock')
    
    def check_limits(self, current_price):
        print("reached")
        """Check if price hits limits"""
        if self.upper_limit and current_price >= self.upper_limit:
            return f"reached upper limit of ${self.upper_limit}"
        if self.lower_limit and current_price<= self.lower_limit:
            return f"reached lower limit of ${self.lower_limit}"
        return None