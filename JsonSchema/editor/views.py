from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from .models import User, Schema
from django.http import HttpRequest, HttpResponse, JsonResponse
from .backends import UserAuth
from .utils import generate_key, password_hasher, otp_generator, send_mail
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import UserSerializer, SchemaSerializer
from django.core.cache import cache
import json
from django.conf import settings
import logging
import time
import cloudinary
from django.conf import settings
from django.utils import timezone
from datetime import datetime


logger = logging.getLogger('editor')


# Create your views here.



def index(request: HttpRequest):
    return render(request, "editor/index.html")



def login(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST.get('username')
        logger.debug(username)
        password = request.POST.get('password')
        logger.debug(password)
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
            logger.debug(f"Type of schema:  {type(schema_serializer.data)}")
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
            logger.debug("Sent user data to WebSocket group:", relevent_user_data)
            return render(request, "editor/index.html", context={"user" : user, "user_schemas" : user_schemas})
        else:
            return render(request, "editor/login.html")
    else:
        return render(request, "editor/login.html")
    
def sign_up(request: HttpRequest):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            logger.debug(username)
            email = request.POST.get('email')
            logger.debug(email)
            password = request.POST.get('password')
            logger.debug(password)
            confirm_password = request.POST.get('confirm_password')
            logger.debug(confirm_password)
            profile_picture = request.FILES.get('profile_picture')
            logger.debug(f"Profile Picture to be updated to: {profile_picture}")
            public_id = request.POST.get('cloudinary_public_id')
            logger.debug(f"Image public id: {public_id}")
            user = User(user_id=generate_key(), username=username, user_email=email,password_hash=password_hasher(password), profile_picture=public_id, created_at=timezone.make_aware(datetime(2024, 7, 24, 8, 51, 9, 920129)))
            user.save()
            return redirect('login')
        except Exception as e:
            logger.debug(f"Error in signup view: {e}")
            return render(request, 'editor/signup.html')
    else:
        return render(request, "editor/signup.html")    

def get_signature(request: HttpRequest):

    """the signature has the current timestamp which the cloudinary will
    use to verify how long the signature should be valid for. The default
    value from cloudinary is 1 hour. We can subtract time from it if we want it
    to be a bit less"""
    if request.method == 'GET':
        try:
                params = {
                'timestamp' :int(time.time()),
                'folder' : 'jsonschema_profiles'
            }

                signature = cloudinary.utils.api_sign_request(params_to_sign=params, api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'])
                return JsonResponse({
                'status' : status.HTTP_201_CREATED,
                'signature': signature,
                'api_key' : settings.CLOUDINARY_STORAGE['API_KEY'],
                'timestamp' : params['timestamp'],
            })
        except Exception as e:
            logger.debug(f"Error at get_signature: {e}")
            return JsonResponse({
                'status' : status.HTTP_404_NOT_FOUND,
                "error" : "error occured"
            })

        
    
def delete_schema(request: HttpRequest):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        if user_id != None:
            user = User.objects.get(user_id = user_id)
            logger.debug(f"Current User: {UserSerializer(user).data} ")
            logger.debug(request.POST.get("selected_schema"))
            schema_name = request.POST.get('selected_schema')
            logger.debug(f"Schema to be deleted: {schema_name}")
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
        logger.debug(f"Username to be updated to: {username}")
        email = request.POST.get('email')
        logger.debug(f"Email to be updated to: {email}")
        profile_picture = request.FILES.get('profile_picture')
        logger.debug(f"Profile Picture to be updated to: {profile_picture}")
        public_id = request.POST.get('cloudinary_public_id')
        logger.debug(f"Image public id: {public_id}")
        user = User.objects.get(user_id = user_id)
        user.username = username
        user.user_email = email
        user.profile_picture = public_id
        user.save(update_fields=["username", "user_email", "profile_picture"])
        return redirect('login')
    else:
        if user_id != None:
            user = User.objects.get(user_id = user_id)
            return render(request, "editor/profile.html", context={"user" : user})
        
def forgot_password(request: HttpRequest):
    if request.method == "POST":
        logger.debug(f"Used user email:   {user_email}")
        user = User.objects.filter(user_email = user_email).first()
        logger.debug(f"Retrieved User:  {UserSerializer(user).data}")
        if user :
            user_otp = "".join([request.POST.get("code-"+str(i))for i in range(1, 7)])
            logger.debug(f"User Entered OTP:  {user_otp}")
            otp_generated = cache.get(user_email)
            logger.debug(f"Generated OTP: {otp_generated}")
            if otp_generated == user_otp:
                new_password = request.POST.get("password")
                logger.debug(f"Previous user password hash: {user.password_hash}")
                user.password_hash = password_hasher(new_password)
                user.save()
                logger.debug(f"New user password hash:  {user.password_hash}")
                logger.debug(f"New password:  {new_password}")
                logger.debug("Otp verified. Password changed")
                return render(request, "editor/login.html")
            else:
                logger.debug("otp not verified")
                return redirect('forgot_password')
        else:
            return redirect("forgot_password")
    else:
        return render(request, "editor/forgot_password.html")
def generate_otp(request: HttpRequest):
    if request.method == "POST":
        body = request.body
        data = json.loads(body)
        if data["event"] == "GENERATE_OTP":
            global user_email
            user_email = data["user_email"]
            user = User.objects.filter(user_email = user_email).first()
            if user:
                otp_generator(length=data["length"], user_email = data["user_email"])
                return HttpResponse(status.HTTP_200_OK, {"message" : "OTP generated successfully"})

            return HttpResponse(status.HTTP_400_BAD_REQUEST, {"message" : "OTP generated unsuccessfully"})
        else:
            return HttpResponse(status.HTTP_400_BAD_REQUEST, {"message" : "OTP generation unsuccessfully"})
        

def export_schemas(request: HttpRequest):
    try:
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({"message": "User not logged in"}, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.get(user_id=user_id)
        user_schemas = Schema.objects.filter(user=user)
        schema_serializer = SchemaSerializer(user_schemas, many=True)
        user_schemas_data = schema_serializer.data
        parsed_schemas = parse_data(user_schemas_data)

        # Use json.dumps with ensure_ascii=False
        json_data = json.dumps(parsed_schemas, ensure_ascii=False, indent=2)
        
        return HttpResponse(json_data, content_type='application/json')
        
    except User.DoesNotExist:
        return JsonResponse({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    

def parse_data(data: list):
    schema_list = []
    for schema in data:
        schema_list.append({
            "name" : schema["schema_name"],
            "text" : json.loads(schema["schema_text"])
        })

    return schema_list
