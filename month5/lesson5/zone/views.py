from django.shortcuts import render
from rest_framework import viewsets
from .models import Zone, Visitors
from .serializer import ZoneSerializer, VisitorsSerializer
from .pagination import ZonePagination, VisitorsPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class ZoneViewSets(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    pagination_class = ZonePagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['location']
    search_fields = ['name', 'description']
    ordering_fileds = ['name']

    ordering = ['id',]

class VisitorsViewSets(viewsets.ModelViewSet):
    queryset = Visitors.objects.all()
    serializer_class = VisitorsSerializer
    pagination_class = VisitorsPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['is_allowed', 'zone']
    search_fields = ['full_name']
    ordering_fileds = ['zone']

    ordering = ['id',]