from .models import Shop
from .serializer import ShopSer
from .pagination import ShopPagination
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly

from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework import viewsets, permissions, status

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class ShopViewSets(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSer
    pagination_class = ShopPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'color']
    search_fields = ['name', 'color']
    ordering_fields = ['name', 'id']
    ordering = ['id']

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

    # Кэш, с использованием встроенного декоратора
    @method_decorator(cache_page(60 * 5, key_prefix='shop_list_cache'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)