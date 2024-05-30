from django.db import models


# Create your models here.

class Schema(models.Model):
    id = models.IntegerField(primary_key=True)
    schema = models.TextField()


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    schemas = models.ForeignKey(Schema, on_delete=models.CASCADE)
