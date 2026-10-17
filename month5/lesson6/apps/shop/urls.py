from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ShopViewSets

router = DefaultRouter()
router.register(r'shop', ShopViewSets, basename='shop')

urlpatterns = [
    path('', include(router.urls))
]