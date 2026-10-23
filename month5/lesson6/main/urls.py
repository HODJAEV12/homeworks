from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('swagger/', SpectacularSwaggerView.as_view(), name='swagger'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('redoc/', SpectacularRedocView.as_view(), name='redoc'),

    path('api/', include("apps.api.urls")), 
    path('task/', include("apps.task.urls")),
    path('books/', include("apps.books.urls")),
    path('shop/', include("apps.shop.urls")),
    path('users/', include("apps.users.urls"))
]
