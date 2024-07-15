from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path

from . import views

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', views.registrationView, name='register'),
    path('logout/', views.logoutView, name='logout'),
]

