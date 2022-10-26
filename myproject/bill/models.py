from django.db import models

# Create your models here.
#
class Bill(models.Model):
    user_id = models.IntegerField(null=False, unique=False)
    source_type = models.CharField(max_length=255, null=False)
    bill_amount = models.IntegerField(null=False)
    category_name = models.CharField(max_length=255,null=False)
    category_id = models.IntegerField(null=False)
    bill_remark = models.CharField(max_length=255, null=True)
    bill_date = models.CharField(max_length=255,null=False)
    category_icon_name = models.CharField(max_length=255,null=True)

