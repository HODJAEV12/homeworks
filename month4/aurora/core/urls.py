from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from apps.aurora.views import index, contact, rooms

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index-page"),
    path('contact/', contact, name="contact-page"),
    path('rooms/', rooms, name="rooms-page")
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)