from django.db import models
from datetime import *
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image


# Create your models here.
class player(models.Model):
    player_id=models.AutoField
    player_name=models.CharField( max_length=50)
    player_country=models.CharField(max_length=50,choices=[('India', 'India'), ('England', 'England'),('Australia', 'Australia'),('Newzealand', 'Newzealand')],default="")
    player_role=models.CharField(max_length=50,choices=[('Batsman', 'Batsman'), ('Bowler', 'Bowler'),('AllRounder','AllRounder')],default="")
    base_price=models.IntegerField(default="")
    raising_price=models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    sell_price=models.IntegerField(default=0,blank=True, null=True)
    status=models.CharField(max_length=50,default="",choices=[('bidding', 'bidding'),('unsold', 'unsold'), ('sold','sold')])
    sell_teamName= models.CharField(max_length=50,default="",blank=True)
    date = models.DateField(default=datetime.now)
    hour= models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(23)])
    minite=models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(59)])
    second=models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(59)])
    image = models.ImageField(default='default.jpg', upload_to='player_pics')

    
    def __str__(self):
        return (self.player_name)

    #def save(self):
    #    super().save()

    #    img = Image.open(self.image.path)

     #   if img.height > 300 or img.width > 300:
      #      output_size = (300, 300)
       #     img.thumbnail(output_size)
        #    img.save(self.image.path)