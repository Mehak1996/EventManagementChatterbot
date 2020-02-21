from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
import json
import datetime 
from django.contrib import messages
from eventApp.Models.models import Event
from django.core.files.storage import FileSystemStorage

def list_all_events(request):
    obj = Event.objects.all()
    context = {"totalEvents": obj}
    return render(request, 'listAllEvents.html',context)

def event_detail(request,eventId):
    obj = Event.objects.get(id=eventId)
    context = {"event": obj}
    return render(request, 'eventDetail.html',context)

def edit_event(request,eventId):
    obj = Event.objects.get(id=eventId)
    formattedDate = obj.date.strftime("%m/%d/%Y")
    context = {"event": obj, "date": formattedDate}
    return render(request, 'addEvent.html',context)

def saveEvent(request,eventId,name,location, date, description):
    # for add 
    if eventId == '0':
        unformattedDate = request.POST.get('date')
        format_str = '%m/%d/%Y' # The format
        datetime_obj = datetime.datetime.strptime(unformattedDate, format_str)
        e = Event(name=request.POST.get('name'),location=request.POST.get('location'),date=datetime_obj,description=request.POST.get('description'))
        files = request.FILES["image"]
        fs = FileSystemStorage()
        fs.save(files.name,files)
        e.image.name = files.name
        e.save();
        
    # for edit
    elif eventId:
        obj = Event.objects.get(id=eventId)
        obj.name = request.POST.get('name')
        obj.location = request.POST.get('location')
        date = request.POST.get('date')
        format_str = '%m/%d/%Y' # The format
        datetime_obj = datetime.datetime.strptime(date, format_str)
        obj.date = datetime_obj
        obj.description = request.POST.get('description')
        # still to be fixed
        #if request.method == "GET" or request.method == "POST" :
        #    files = request.FILES["image"]
        #    fs = FileSystemStorage()
        #    fs.save(files.name,files)
        #    obj.image.name = files.name
        #else :
        #    files = request.FILES["image"]
        #    fs = FileSystemStorage()
        #    fs.save(files.name,files)
        #    obj.image.name = files.name
        files = request.FILES["image"]
        fs = FileSystemStorage()
        fs.save(files.name,files)
        obj.image.name = files.name
        obj.save()
    
    return redirect('listAll')


def deleteEvent(request,eventId):
    Event.objects.get(id=eventId).delete()
    return redirect('listAll')

def add_Event(request):
    context = {"event": {"id":0,"name":" ","date":" ","description":" ","location":" "}, "date": " "}
    return render(request, 'addEvent.html',context)
