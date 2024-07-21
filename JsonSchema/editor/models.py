from django.db import models
from datetime import datetime
from .utils import generate_key

# Create your models here.

"""
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Schemas (
    schema_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    schema_name VARCHAR(255) NOT NULL,
    schema_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Validations (
    validation_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    schema_id INT NOT NULL,
    json_string TEXT NOT NULL,
    is_valid BOOLEAN,
    validation_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (schema_id) REFERENCES Schemas(schema_id)
);





"""


class User(models.Model):
    user_id = models.CharField(primary_key=True, default=generate_key)
    username = models.CharField(max_length=200, unique=True)
    password_hash = models.CharField(default='1234')
    profile_picture = models.CharField(max_length=200)
    user_email = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(default=datetime.now) # automatically set to now time

    def __str__(self) -> str:
        return self.user_id + " " + self.username



class Schema(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schema_name = models.CharField(max_length=255)
    schema_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.user_id + " " + self.schema_name
"""
The auto_now_add and datetime.now are both the same thing which compute the current timings

"""
class Validation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    json_string = models.TextField()
    is_valid = models.BooleanField()
    validation_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Validation for {self.schema.schema_name} by {self.user.username}"
