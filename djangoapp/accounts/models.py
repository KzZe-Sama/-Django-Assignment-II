from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user=models.CharField(max_length=100)
    image=models.ImageField(default='default.png',upload_to='profile_pics',null=True,blank=True)
    def __str__(self):
        return f'{self.user} Profile'

class verification_code(models.Model):
    user=models.EmailField()
    code=models.CharField(max_length=4)

    def __str__(self):
        return self.user
