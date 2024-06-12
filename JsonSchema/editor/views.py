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
            # send the data to the frontend for manuipulation

            """
            Websocket communication is asynchronous, but normal views are
            synchronous, hence you cant simply use the websocket in views to
            send the data. WHat we did was create a group and converted the sync
            views to async. This allows us to send the data 
            """
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "user_info", #group name
                { # data
                    # type of message so that this is the type consumer reacts to
                    "type": "send_user_data_event",
                    "data": relevent_user_data
                }
            )
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
