from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
import json
import datetime 
from django.contrib import messages
from eventApp.Models.models import Event,UserEventRegisteration
from eventApp.Views import Observer
from eventApp.Views.Factory import *
from django.core.files.storage import FileSystemStorage

class EventOperations():

    def list_all_events(self,request):

        obj = Event.objects.all()
        registeredObj = UserEventRegisteration.objects.all().filter(userId_id=request.user.id)
        registeredByUser= []
        for each in registeredObj:
                registeredByUser.append(each.eventID_id)
        context = {"totalEvents": obj,"registered":registeredByUser}
        return render(request, 'listAllEvents.html',context)

    def event_detail(self,request,eventId):
        obj = Event.objects.get(id=eventId)
        registeredObj = UserEventRegisteration.objects.all().filter(userId_id=request.user.id,eventID_id= eventId)
        if registeredObj:
            setTo = True
        else:
            setTo = False
        context = {"event": obj,"registered":setTo}
        return render(request, 'eventDetail.html',context)

    def edit_event(self,request,eventId):
        obj = Event.objects.get(id=eventId)
        formattedDate = obj.date.strftime("%m/%d/%Y")
        #formattedTime = obj.time.hour+":"+obj.time.hour
        context = {"event": obj, "date": formattedDate}
        return render(request, 'addEvent.html',context)

    def formatTime(self,time):
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

    def saveEvent(self,request,eventId,name,address, date, description,city,time,eventType):
        # for add 
        if eventId == '0':
            if request.method == 'POST':
                if request.POST.get('name') == " " or request.POST.get('address') == " " or request.POST.get('date') == " " or request.POST.get('city') == " " or request.POST.get('time') == " ":
                    messages.error(request,'Please fill in all the fields to add new event.')
                    return redirect('addEvent')
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
            messages.success(request, "Successfully added")
                
        # for edit
        elif eventId:
            obj = Event.objects.get(id=eventId)
            obj.name = request.POST.get('name')
            obj.address = request.POST.get('address')
            obj.city = request.POST.get('city')
            time = request.POST.get('time')
            #formatting time
            obj.time = self.formatTime(time)
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
            messages.success(request, "Successfully saved")
        return redirect('listAll')


    def deleteEvent(self,request,eventId):
        Event.objects.get(id=eventId).delete()
        messages.success(request, "Successfully deleted")
        return redirect('listAll')

    def add_Event(self,request):
        context = {"event": {"id":0,"name":" ","date":" ","description":" ","address":" ","time":" ","city": " ","eventType":" "}, "date": " "}
        return render(request, 'addEvent.html',context)

class EventRegistrations:

    def registerEvent(self,request,eventId):
        e = UserEventRegisteration(userId_id=request.user.id,eventID_id=eventId)
        res = e.save();
        #adding observer pattern
        subject = Observer.ConcreteSubject()
        observer_a = Observer.ConcreteObserver()
        subject.attach(observer_a)
        subject.subject_state = "registered"
        subject.detach(observer_a)

        #adding factory pattern
        messageFactory = MessageFactory().get_message("Success")
        print(messageFactory.get_messageText())
        messages.success(request, "Successfully registered")
        return redirect('listAll')

    def listAllRegisteredEvents(self,request):
        obj = UserEventRegisteration.objects.all().filter(userId_id=request.user.id)
        eventObj=[]
        for eachEvent in obj:
            eventObj.append(Event.objects.get(id=eachEvent.eventID_id))
        context = {"totalEvents": eventObj, "registeredList":True}
        return render(request, 'listAllEvents.html',context)


