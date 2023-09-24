from django.db import models

from django.db import models

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=200) 
    lastName = models.CharField(max_length=200)  
    tachado = models.BooleanField(default=False)


    