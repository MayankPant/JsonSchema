from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from django.http import HttpRequest
from .backends import UserAuth



# Create your views here.



def index(request: HttpRequest):
    return render(request, "editor/index.html")



def login(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        print(password)
        user = UserAuth.authenticate(request=request, username=username, password=password)

        if user != None:
            return render(request, "editor/index.html")
        else:
            return render(request, "editor/login.html")
    else:
        return render(request, "editor/login.html")
    
def sign_up(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        print(password)
        user = UserAuth.authenticate(request=request, username=username, password=password)
        
        if user != None:
            return render(request, "editor/index.html")
        else:
            return render(request, "editor/login.html")
    else:
        return render(request, "editor/signup.html")
