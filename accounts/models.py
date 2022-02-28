from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class User_meta_data(models.Model):
    first_name = models.CharField(max_length=200,null=True,blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User,related_name='usermeta',on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
