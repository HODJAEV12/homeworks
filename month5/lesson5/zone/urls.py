from django.urls import path, include
from .views import ZoneViewSets, VisitorsViewSets
from rest_framework.routers import DefaultRouter

zone_router = DefaultRouter()
zone_router.register(r'zone', ZoneViewSets, basename='zone')

visitors_router = DefaultRouter()
visitors_router.register(r'visitors/', VisitorsViewSets, basename='visitors')

urlpatterns = [
    path('zone/', include(zone_router.urls)),
    path('visitors/', include(visitors_router.urls))
]