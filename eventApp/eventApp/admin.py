from django.contrib import admin
from .Models.models import Event,UserEventRegisteration

# Register your models here.
admin.site.register(Event)
admin.site.register(UserEventRegisteration)