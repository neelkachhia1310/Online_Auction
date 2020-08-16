from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import *
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image

# Create your models here.
class order(models.Model):
    product_id = models.IntegerField(default=0) 
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length = 254)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode =  models.IntegerField()
    payment_status=models.CharField(max_length=50,default="incomplete",choices=[('incomplete', 'incomplete'),('complete', 'complete')])
