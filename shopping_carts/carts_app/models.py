from django.db import models
import datetime
# Create your models here.
class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name=models.CharField(max_length=500)
class User(models.Model):
    user_id=models.AutoField(primary_key=True)
    full_name= models.CharField(max_length=100)
    user_name= models.CharField(max_length=100)
    password= models.CharField(max_length=100)
    session_token= models.CharField(max_length=1000,default=0)
    exp_date=models.DateTimeField(default=datetime.date.today)

class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name=models.CharField(max_length=500)

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    item_id=models.ForeignKey(Item, on_delete=models.CASCADE)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE)
    cart_date=models.DateTimeField()


class RoleMapping(models.Model):
    role_mapping_id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE)
    role_id=models.ForeignKey(Role, on_delete=models.CASCADE)
