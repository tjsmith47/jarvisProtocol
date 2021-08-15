from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('create', views.register),
    path('auth', views.authenticate),
    path('user/dashboard', views.dashboard),
    path('user/update', views.update),
    path('user/logout', views.logout),
]