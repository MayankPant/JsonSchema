from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('login/', views.login, name="login"),
    path('signup/', views.sign_up, name='signup'),
    path('delete/', views.delete_schema, name="delete"),
    path('profile/', views.profile, name="profile"),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('generate_otp/', views.generate_otp, name="generate_otp"),
    path('export_schemas/', views.export_schemas, name="export_schemas"),
]