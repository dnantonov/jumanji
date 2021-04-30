from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView

from jumanji.settings import LOGIN_REDIRECT_URL

from .forms import CreateUserForm



class LoginView(LoginView):
    template_name = 'accounts/login.html'


class LogoutView(View):
    pass


class RegisterView(CreateView):
    form_class = CreateUserForm
    template_name = 'accounts/register.html'

    def post(self, request):
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()

                return HttpResponseRedirect(LOGIN_REDIRECT_URL)

        context = {'form': form}
        return render(request, template_name, context)

