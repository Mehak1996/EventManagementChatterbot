from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User

def login_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('listAll')
            #list_all_events(request);
            #return render(request, 'listAllEvents.html')
        else:
            messages.error(request,'Invalid username or password.')
            return redirect('login')

def register(request):
    return render(request, 'register.html')
    
def registerUser(request):
    u = User.objects.create_user(username=request.POST.get('username'),first_name=request.POST.get('firstname'),last_name=request.POST.get('lastname'),email=request.POST.get('email'),password=request.POST.get('password'))
    u.save();
    return redirect('login');

def logout_request(request):
    logout(request)
    return redirect('login')

