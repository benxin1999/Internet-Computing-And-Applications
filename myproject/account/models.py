from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=100, unique=True,null=False)
    password = models.CharField(max_length=255, null=False)
    slogon = models.CharField(max_length= 128, null=True)
    avatar = models.CharField(max_length = 128, null=True)