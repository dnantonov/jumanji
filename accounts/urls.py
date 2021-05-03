from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import MyLoginView, MyRegisterView


urlpatterns = [
    path('login/', MyLoginView.as_view(), name="login"),
    path('register/', MyRegisterView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
]
