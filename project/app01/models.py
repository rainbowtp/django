from django.db import models

# Create your models here.
class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    date = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=32)

    # email=models.EmailField(required=False)
    # tel=models.CharField(required=False)

class DateInfo(models.Model):
    id = models.AutoField(primary_key=True)
    site = models.URLField(max_length=32)
    account =  models.CharField(max_length=32)
    password = models.BinaryField(max_length=128)
    date = models.DateTimeField(auto_now_add=True)
    userinfo = models.ForeignKey(to="UserInfo", to_field = 'id', on_delete=models.CASCADE)

