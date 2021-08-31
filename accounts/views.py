from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

from .forms import CreateUserForm


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'accounts/login.html'


class MyRegisterView(CreateView):
    form_class = CreateUserForm
    success_url = '/accounts/login/'
    template_name = 'accounts/register.html'
