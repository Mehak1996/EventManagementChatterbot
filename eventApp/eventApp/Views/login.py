from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
import re

class Login:
    def login_request(self,request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('listAll')
            else:
                messages.error(request,'Invalid username or password.')
                return redirect('login')

    def register(self,request):
        return render(request, 'register.html')
        
    def registerUser(self,request):
        if request.method == 'POST':
            uname=request.POST.get('username')
            fname=request.POST.get('firstname')
            lname=request.POST.get('lastname')
            emailAddress=request.POST.get('email')
            passwords=request.POST.get('password')
            cpasswords=request.POST.get('confirmPassword')
            if uname == "" or fname == "" or lname == "" or emailAddress == "" or passwords == "" or cpasswords == "" :
                messages.error(request,'Please fill in all the fields to register.')
                return redirect('register')
            elif  passwords != cpasswords :
                messages.error(request,'Password and Confirm password do not match.')
                return redirect('register')
            elif re.search('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$',emailAddress) == None:
                messages.error(request,'Please enter a valid email address.')
                return redirect('register')
            else :
                u = User.objects.create_user(username=uname,first_name=fname,last_name=lname,email=emailAddress,password=passwords)
                u.save();
                user = authenticate(username=uname, password=passwords)
                if user is not None:
                    login(request, user)
                    return redirect('listAll')

    def logout_request(self,request):
        logout(request)
        return redirect('login')

