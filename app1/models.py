from django.db import models

# Create your models here.

class ContactForm(models.Model):
    name = models.CharField(max_length=30, default='')
    email = models.EmailField(default='')
    message = models.CharField(max_length=1000, default='')
    
    def __str__(self):
        return self.name
    
    
class signUp(models.Model):
    name = models.CharField(max_length=30, default='')
    email = models.EmailField(default='')
    address = models.CharField(max_length=100, default='')
    number = models.PositiveIntegerField(default='')
    password = models.CharField(default='', max_length=15)

    def __str__(self):
        return self.name
    
