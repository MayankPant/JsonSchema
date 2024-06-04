from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Create your views here.



def index(request):
    return render(request, "editor/index.html")

def login(request):
    return render(request, 'editor/login.html')

def authenticate(request, form):
    pass
