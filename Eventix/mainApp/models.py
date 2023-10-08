from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#class Name(models.Model):
    #campos

class Space(models.Model):
    title = models.CharField(max_length=100)
    capacity = models.IntegerField();
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField(blank = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self): #es para que en admin aparezca el nombre del objeto y no "obecjt(x)"
        return self.title
    
