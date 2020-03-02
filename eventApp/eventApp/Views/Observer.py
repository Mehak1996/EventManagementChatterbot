
from abc import ABC, abstractmethod
#from eventApp.Views.eventsClass import EventOperations
from django.shortcuts import render, render_to_response, redirect
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
    def observers(self):
        return self._observers    

    @subject_state.setter
    def subject_state(self, arg):
        self._subject_state = arg
        self.notify()

    def __init__(self):
        self._observers = []
        self._subject_state = None
        
    def attach(self, observer):
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer):
        print("Subject: Detached an observer.")
        self._observers.remove(observer)

    def notify(self):
        print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject: Subject):
        pass

"""
Concrete Observers react to the updates issued by the Subject they had been attached to.
"""
class ConcreteObserver(Observer):
    def update(self, subject: Subject):
        print("ConcreteObserver: Reacted to the event")
        return redirect('listAll')