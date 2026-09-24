from django.contrib import admin
from .models import (
    Settings, 
    Banner, 
    Advantages, 
    About_hotel,
    Rooms,
)

admin.site.register(Settings)
admin.site.register(Banner)
admin.site.register(Advantages)
admin.site.register(About_hotel)
admin.site.register(Rooms)