
from abc import ABC, abstractmethod
#from eventApp.Views.eventsClass import EventOperations
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpRequest
from django.http import HttpResponse, HttpResponseRedirect
from eventApp.Models.models import Event,UserEventRegisteration

class Subject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """
    @abstractmethod
    def attach(self, observer):
        pass

    @abstractmethod
    def detach(self, observer):
        pass

    @abstractmethod
    def notify(self):
        pass


class ConcreteSubject(Subject):
    """
    The Subject owns some important state and notifies observers when the state
    changes.
    """
    
    @property
    def subject_state(self):
        return self._subject_state
    
    @property
    def request(self):
        return self._request
        
    @property
    def observers(self):
        return self._observers    

    @subject_state.setter
    def subject_state(self, arg):
        self._subject_state = arg
        self.notify()

    @request.setter
    def request(self, arg):
        self._request = arg

    def __init__(self):
        self._observers = []
        self._subject_state = None
        self._request = None
        
    def attach(self, observer):
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer):
        print("Subject: Detached an observer.")
        self._observers.remove(observer)

    def notify(self):
        print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self,self._request)

class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self,subject: Subject,request):
        pass

"""
Concrete Observers react to the updates issued by the Subject they had been attached to.
"""
class checkForRegisterObserver(Observer):
    def update(self,subject: Subject,request):
        print("ConcreteObserver: Reacted to the event")
        #Fetching list of events from the backnend
        obj = Event.objects.all()
        #Fetching list of redistered events from the backnend for the user who is logged in
        registeredObj = UserEventRegisteration.objects.all().filter(userId_id=request.user.id)
        registeredByUser= []
        #Reformuling data received from backend into an array 
        for each in registeredObj:
                registeredByUser.append(each.eventID_id)
        #Passing data of all the events and registered events into context variable 
        context = {"totalEvents": obj,"registered":registeredByUser}
        # Render the list again with the latest data
        return render(request, 'listAllEvents.html',context)
        #return redirect('listAll')
