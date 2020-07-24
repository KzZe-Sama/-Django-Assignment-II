from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user=models.CharField(max_length=255)
    image=models.ImageField(default='default.png',upload_to='profile_pics',null=True,blank=True)
    def __str__(self):
        return f'{self.user} Profile'

