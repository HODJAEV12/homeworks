from django.urls import path

from .views import (
    RegisterView, LoginView, LogOutView, ProfileView,
    TokenView, TokenLogOutView, JWTView, JWTLogOutView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),

    path('login/token', TokenView.as_view(), name='token'),
    path('logout/token', TokenLogOutView.as_view(), name='token-out'),

    path('login/jwt', JWTView.as_view(), name='jwt'),
    path('logout/jwt', JWTLogOutView.as_view(), name='jwt-out'),

    path('profile/', ProfileView.as_view(), name='profile'),
]
