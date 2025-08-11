from django.urls import path
from invest.views import StockPageView

urlpatterns = [
    path("api/stocks/<str:ticker>", StockPageView.as_view(), name="stock_page_data"),
]