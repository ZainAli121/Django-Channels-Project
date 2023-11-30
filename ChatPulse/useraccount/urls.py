from .forms import *
from django.urls import path
from django.contrib.auth.views import LoginView

app_name = 'useraccount'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='useraccount/login.html', form_class=LoginForm), name='login')
]