from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from .models import User, Schema
from django.http import HttpRequest
from .backends import UserAuth
from .utils import generate_key, password_hasher
from .consumers import VerificationConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import UserSerializer, SchemaSerializer

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

        """

        Retrieving the schemas for the user

        """
        user_schemas = Schema.objects.filter(user=user)
        user_serializer = UserSerializer(user)
        schema_serializer = SchemaSerializer(user_schemas, many=True)
        if user != None:
            """
            Here we use the session to store the data related to the 
            logged in user. Sessions are used to store information about
            multiple requests for the same user.
            Sessions have several benefits like user isolation, persistence,
            scalability, security
            """
            request.session['user_id'] = user.user_id
            request.session['user_schemas'] = schema_serializer.data
            relevent_user_data = {
                "user": user_serializer.data,
                "user_schemas": schema_serializer.data
            }

            """
            Websocket communication is asynchronous, but normal views are
            synchronous, hence you cant simply use the websocket in views to
            send the data. WHat we did was create a group and converted the sync
            views to async. This allows us to send the data 
            """
            print("Sent user data to WebSocket group:", relevent_user_data)
            return render(request, "editor/index.html", context={"user" : user, "user_schemas" : user_schemas})
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
    
def delete_schema(request: HttpRequest):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        if user_id != None:
            user = User.objects.get(user_id = user_id)
            print(f"Current User: {UserSerializer(user).data} ")
            print(request.POST.get("selected_schema"))
            schema_name = request.POST.get('selected_schema')
            print(f"Schema to be deleted: {schema_name}")
            deleted_schema = Schema.objects.filter(user=user, schema_name = schema_name)
            deleted_schema.delete()
            user_schemas = Schema.objects.filter(user=user)
            # updating values in the sessioon storage
            request.session["user_schemas"] = SchemaSerializer(user_schemas, many=True).data
        return render(request, 'editor/index.html', context={"user" : user, "user_schemas" : Schema.objects.filter(user = user)})


def profile(request: HttpRequest):
    user_id = request.session.get("user_id")
    if request.method == "POST":
        username = request.POST.get('username')
        print(f"Username to be updated to: {username}")
        email = request.POST.get('email')
        print(f"Email to be updated to: {email}")
        profile_picture = request.FILES.get('profile_picture')
        print(f"Profile Picture to be updated to: {profile_picture}")
        user = User.objects.get(user_id = user_id)
        user.username = username
        user.user_email = email
        user.profile_picture = profile_picture
        user.save(update_fields=["username", "user_email", "profile_picture"])
        return redirect('login')
    else:
        if user_id != None:
            user = User.objects.get(user_id = user_id)
            return render(request, "editor/profile.html", context={"user" : user})
        
def forgot_password(request: HttpRequest):
    user_id = request.session.get("user_id")
    if request.method == "POST":
        pass
    else:
        return render(request, "editor/forgot_password.html")