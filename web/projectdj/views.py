from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView

from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from projectdj.forms import MyUserCreationForm


class Home(TemplateView):
    template_name = 'home.html'


class NotFound(TemplateView):
    template_name = '404.html'


class UserCreationView(CreateView):
    form_class = MyUserCreationForm
    template_name = 'registration/user_create.html'
    success_url = reverse_lazy('homepage')


class UserLoginView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/user_create.html'
    success_url = reverse_lazy('homepage')


class MyLogoutView(LogoutView):
    template_name = "home.html"
    success_url = reverse_lazy('homepage')

