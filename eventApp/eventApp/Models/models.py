" models file "
from django.db import models
from datetime import date, datetime


class Event(models.Model):
    " test model"
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, default=None)
    image = models.ImageField(upload_to='eventImages/', height_field=None, width_field=None, max_length=100, default = '/static/img/abcimage.jpg')
    date = models.DateField(auto_now_add = False, auto_now = False, blank = True)
    description = models.CharField(max_length=500, default=None)

    def __str__(self):
        return self.name


