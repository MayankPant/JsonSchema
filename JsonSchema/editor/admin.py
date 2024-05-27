from django.contrib import admin
from .models import Schema, User

# Register your models here.
admin.site.register(Schema)
admin.site.register(User)