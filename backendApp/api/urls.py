# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('get-stocks/', views.get_stocks, name='get-stocks'),
    path('get-stocks/<int:stock_id>/', views.get_stocks_by_id, name='get-stocks-id'),
    path('create-stock/', views.create_stock, name='create-stock'),
    path('update-stock/<int:stock_id>/', views.update_stock, name='update-stock'),
    path('update-stock-data/<int:pageNumber>/', views.update_stock_data, name='Update Stock Data'),
]