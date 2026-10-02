from django.urls import path
from .views import ProductsApi

urlpatterns = [
    path('products/', ProductsApi.as_view(), name='products_api')
]