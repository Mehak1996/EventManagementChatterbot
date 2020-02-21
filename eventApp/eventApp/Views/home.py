from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

def home(request, template_name="home.html"):
    context = {'title': 'Chatbot Version 1.0'}
    return render_to_response(template_name, context)

def homePage(request):
    return render(request,'login.html')

def floating_button(request):
    return render(request, 'floatingButton.html')