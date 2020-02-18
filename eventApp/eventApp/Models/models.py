" models file "
from django.db import models

class Testt(models.Model):
    " test model"
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=10)

    def __str__(self):
        return self.username
