from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import *
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product_category=models.CharField(max_length=256, choices=[('electronic', 'electronic'), ('propertie','propertie'), ('art', 'art')],default="electronic")
    base_price=models.IntegerField(default="")
    raising_price=models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    sell_price=models.IntegerField(default=0,blank=True, null=True)
    status=models.CharField(max_length=50,default="bidding",choices=[('bidding', 'bidding'),('unsold', 'unsold'), ('sold','sold')])
    sell_customer_name= models.CharField(max_length=50,default="",blank=True)
    date = models.DateField(default=datetime.now)
    hour= models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(23)])
    minite=models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(59)])
    second=models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(59)])
    image = models.ImageField(default='default.jpg', upload_to='product_pics')
    payment_status=models.CharField(max_length=50,default="incomplete",choices=[('incomplete', 'incomplete'),('complete', 'complete')])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    
    

