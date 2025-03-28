from django.urls import path
from .views.stock import StockListView, UserStockListView, StockDetail

app_name='stocks'

urlpatterns=[
    path('api/stocks/', StockListView.as_view(), name= 'stock_list'),
    path('api/my-stocks/', UserStockListView.as_view(), name='user_stock_list'),
    path('api/stock/<str:symbol>', StockDetail.as_view(), name="stock detail")
]