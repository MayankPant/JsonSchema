from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from django.http import HttpRequest
from .backends import UserAuth
from .utils import generate_key, password_hasher



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
            return render(request, "editor/index.html", context={"user" : user})
        else:
            return render(request, "editor/login.html")
    else:
        return render(request, "editor/login.html")
    
def sign_up(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        print(password)
        confirm_password = request.POST.get('confirm_password')
        print(confirm_password)
        profile_picture = request.FILES.get('profile_picture')
        print(profile_picture)
        user = User(user_id=generate_key(), username=username, user_email=email,password_hash=password_hasher(password), profile_picture=profile_picture)
        user.save()
        return redirect('login')
    else:
        return render(request, "editor/signup.html")
