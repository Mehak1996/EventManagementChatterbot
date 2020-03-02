"""eventApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from eventApp import views
from django.conf.urls.static import static
from django.conf import settings
from .Views import chatterbotUtility
#from .Views import login
#from .Views import events
#from .Views import home
from .Views.eventsClass import EventOperations,EventRegistrations
from .Views.login import Login
from .Views.home import Home

home = Home()
login = Login()
event = EventOperations()
eventRegister = EventRegistrations()

admin.autodiscover()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('floatingbutton/', home.floating_button),
    path('chatbot/', home.home, name='chatbot'),
    path('get-response/', chatterbotUtility.get_response),
    path("", home.homePage, name="login"),
    path("register/",login.register, name="register"),
    path("register/registerUser",login.registerUser, name="registerUser"),
    path("listAll", event.list_all_events,  name="listAll"),
    path("listAllRegisteredEvents", eventRegister.listAllRegisteredEvents,  name="listAllRegisteredEvents"),
    path(r'^eventDetail/(?P<eventId>\d+)/$', event.event_detail, name='eventDetail'),
    path(r'^editEvent/(?P<eventId>\d+)/$', event.edit_event, name='editEvent'),
    path(r'^editEvent/(?P<eventId>\d+)/deleteEvent/$', event.deleteEvent, name='deleteEvent'),
    path(r'^editEvent/(?P<eventId>\d+)/registerEvent/$', eventRegister.registerEvent, name='registerEvent'),
    path("listAllEvents", login.login_request),
    path("logout_request", login.logout_request),
    path("addEvent/", event.add_Event, name='addEvent'),
    path(r'^eventDetail/(?P<eventId>\d+)/(?P<name>\w+)/(?P<address>\w+)/(?P<date>\w+)/(?P<description>\w+)/(?P<city>\w+)/(?P<time>\w+)/(?P<eventType>\w+)/saveEvent/$', event.saveEvent, name="saveEvent")
]

if settings.DEBUG == True:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)