from django.urls import path
from .views import LoginView, RegisterView

urlpatterns = [
    path('login/', 
        LoginView.as_view(), name="login"),
    path('logout/', 
        RegisterView.as_view(), name="logout"),
    path('register/', 
        RegisterView.as_view(), name="register"),   
]