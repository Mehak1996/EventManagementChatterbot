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

admin.autodiscover()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', views.home),
    path('get-response/', views.get_response),
    path("", views.homee, name="login"),
    path("register/",views.register),
    #path("listAllEvents/", views.list_all_events),
    path("eventDetail/", views.event_detail),
    path("listAllEvents", views.login_request),
    path("logout_request", views.logout_request)
]

if settings.DEBUG == True:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)