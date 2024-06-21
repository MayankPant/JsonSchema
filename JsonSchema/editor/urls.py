from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('login/', views.login, name="login"),
    path('signup/', views.sign_up, name='signup'),
    path('delete/', views.delete_schema, name="delete"),
    path('profile/', views.profile, name="profile"),
]