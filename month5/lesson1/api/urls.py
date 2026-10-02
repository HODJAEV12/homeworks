from django.urls import path
from .views import HelloView, hello_view, People, people_func

urlpatterns = [
    path('hi_class/', HelloView.as_view(), name='hello-class'),
    path('hi_func/', hello_view, name='hello-func'),
    path('people_class/', People.as_view(), name='people-class'),
    path('people_func/', people_func, name='people-func')
]