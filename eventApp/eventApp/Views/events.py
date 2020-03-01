from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
import json
import datetime 
from django.contrib import messages
from eventApp.Models.models import Event,UserEventRegisteration
from django.core.files.storage import FileSystemStorage
from eventApp.Views import chatterbotUtility

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

def formatTime(time):
    t= time.split(" ")[0]
    if 'p.m.' in time :
        if ':' in time.split(" ")[0] :
            timepart1 = int(t.split(":")[0])+12
            if timepart1 == 24:
                formattedtime =  "00:"+(t.split(":")[1])
            else: 
                formattedtime = str(timepart1)+ ":"+(t.split(":")[1])
        else:
            formattedtime = str(int(time.split(" ")[0])+12)+":00"
    elif 'a.m.' in time:
        if ':' in time.split(" ")[0] :
             formattedtime = str(int(t.split(":")[0]))+":"+(t.split(":")[1])
        else:
            formattedtime = str(int(time.split(" ")[0]))+":00"
    else:
        formattedtime = time
    return formattedtime

def formatDate(date):
    format_str = '%m/%d/%Y' # The format
    datetime_obj = datetime.datetime.strptime(date, format_str)
    return datetime_obj


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
            chatterbotUtility.formulate_conversations(e)
    
    # for edit
    elif eventId:
        obj = Event.objects.get(id=eventId)
        objStatus = {'name' : 'unMod', 'address' : 'unMod', 'eventDate' : 'unMod', 'desc' : 'unMod' , 'city' : 'unMod' , 'eventTime' : 'unMod', 'eventType' : 'unMod'}
        
        currentName = request.POST.get('name')
        currentAddress = request.POST.get('address')
        currentCity = request.POST.get('city')
        currentTime = request.POST.get('time')
        formattedCurrentTime = formatTime (currentTime)
        currentEventType = request.POST.get('eventType')
        currentDate = request.POST.get('date')
        currentFormattedDate = formatDate (currentDate)
        currentDesc = request.POST.get('description')

        if (obj.name != currentName):
            obj.name = currentName
            objStatus['name'] = 'Mod'
        
        if (obj.address != currentAddress):
            obj.address = currentAddress
            objStatus['address'] = 'Mod'

        if (obj.city != currentCity):
            obj.city = currentCity
            objStatus['city'] = 'Mod'

        if (obj.time != formattedCurrentTime):
            obj.time = formattedCurrentTime
            objStatus['eventTime'] = 'Mod'
        
        if (obj.eventType != currentEventType):
            obj.eventType = currentEventType
            objStatus['eventType'] = 'Mod'
        
        if (obj.date != currentFormattedDate):
            obj.date = currentFormattedDate
            objStatus['eventDate'] = 'Mod'
        
        if (obj.description != currentDesc):
            obj.description = currentDesc
            objStatus['desc'] = 'Mod'

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
        chatterbotUtility.edit_converstaions (obj, objStatus)

    return redirect('listAll')

def deleteEvent(request,eventId):
    Event.objects.get(id=eventId).delete()
    return redirect('listAll')

def add_Event(request):
    context = {"event": {"id":0,"name":" ","date":" ","description":" ","address":" ","time":" ","city": " ","eventType":" "}, "date": " "}
    return render(request, 'addEvent.html',context)

def registerEvent(request,eventId):
    e = UserEventRegisteration(userId_id=request.user.id,eventID_id=eventId)
    e.save()
    return redirect('listAll')

def listAllRegisteredEvents(request):
    obj = UserEventRegisteration.objects.all().filter(userId_id=request.user.id)
    eventObj=[]
    for eachEvent in obj:
        eventObj.append(Event.objects.get(id=eachEvent.eventID_id))
    context = {"totalEvents": eventObj, "registeredList":True}
    return render(request, 'listAllEvents.html',context)
