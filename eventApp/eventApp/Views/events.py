from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
import json
import datetime 
from django.contrib import messages
from eventApp.Models.models import Event,UserEventRegisteration
from django.core.files.storage import FileSystemStorage

def list_all_events(request):
    obj = Event.objects.all()
    registeredObj = UserEventRegisteration.objects.all().filter(userId_id=request.user.id)
    registeredByUser= []
    for each in registeredObj:
            registeredByUser.append(each.eventID_id)
    context = {"totalEvents": obj,"registered":registeredByUser}
    return render(request, 'listAllEvents.html',context)

def event_detail(request,eventId):
    obj = Event.objects.get(id=eventId)
    registeredObj = UserEventRegisteration.objects.all().filter(userId_id=request.user.id,eventID_id= eventId)
    if registeredObj:
        setTo = True
    else:
        setTo = False
    context = {"event": obj,"registered":setTo}
    return render(request, 'eventDetail.html',context)

def edit_event(request,eventId):
    obj = Event.objects.get(id=eventId)
    formattedDate = obj.date.strftime("%m/%d/%Y")
    #formattedTime = obj.time.hour+":"+obj.time.hour
    context = {"event": obj, "date": formattedDate}
    return render(request, 'addEvent.html',context)

def saveEvent(request,eventId,name,address, date, description,city,time,eventType):
    # for add 
    if eventId == '0':
        unformattedDate = request.POST.get('date')
        format_str = '%m/%d/%Y' # The format
        datetime_obj = datetime.datetime.strptime(unformattedDate, format_str)
        e = Event(name=request.POST.get('name'),address=request.POST.get('address'),date=datetime_obj,description=request.POST.get('description'),city=request.POST.get('city'),time=request.POST.get('time'),eventType=request.POST.get('eventType'))
        if request.FILES.get('image', False) == False:
            e.save()
        else : 
            files = request.FILES["image"]
            fs = FileSystemStorage()
            fs.save(files.name,files)
            e.image.name = files.name
            e.save()
            
    # for edit
    elif eventId:
        obj = Event.objects.get(id=eventId)
        obj.name = request.POST.get('name')
        obj.address = request.POST.get('address')
        obj.city = request.POST.get('city')
        obj.time = request.POST.get('time')
        obj.eventType = request.POST.get('eventType')
        date = request.POST.get('date')
        format_str = '%m/%d/%Y' # The format
        datetime_obj = datetime.datetime.strptime(date, format_str)
        obj.date = datetime_obj
        obj.description = request.POST.get('description')
        #still to be fixed
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
        if request.FILES.get('image', False) == False:
            obj.save()
        else : 
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
    context = {"event": {"id":0,"name":" ","date":" ","description":" ","address":" ","time":" ","city": " ","eventType":" "}, "date": " "}
    return render(request, 'addEvent.html',context)

def registerEvent(request,eventId):
    e = UserEventRegisteration(userId_id=request.user.id,eventID_id=eventId)
    e.save();
    return redirect('listAll')

def listAllRegisteredEvents(request):
    obj = UserEventRegisteration.objects.all().filter(userId_id=request.user.id)
    eventObj=[]
    for eachEvent in obj:
        eventObj.append(Event.objects.get(id=eachEvent.eventID_id))
    context = {"totalEvents": eventObj, "registeredList":True}
    return render(request, 'listAllEvents.html',context)
