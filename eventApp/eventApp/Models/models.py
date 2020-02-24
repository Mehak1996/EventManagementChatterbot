" models file "
from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime


class Event(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, default=None)
    image = models.ImageField(upload_to='eventImages/', height_field=None, width_field=None, max_length=100, default = '/static/img/abcimage.jpg')
    date = models.DateField(auto_now_add = False, auto_now = False, blank = True)
    description = models.CharField(max_length=500, default=None)
    city = models.CharField(max_length=255, default=" ")
    time = models.TimeField(auto_now=False, auto_now_add=False, blank =True,default='20:00')
    eventType = models.CharField(max_length=255, default="Others")
    

    def __str__(self):
        return self.name

class UserEventRegisteration(models.Model):
    userId = models.ForeignKey(User,on_delete=models.CASCADE,);
    eventID = models.ForeignKey(Event,on_delete=models.CASCADE,);


