from django.db import models

# Create your models here.

class category(models.Model):
    category_name = models.CharField(max_length=100,null=False,unique=True)
    source_type = models.CharField(max_length=100, null=False)
    user_id = models.IntegerField(null=True,unique=False)
    category_icon_name = models.CharField(max_length=100,null=False)
