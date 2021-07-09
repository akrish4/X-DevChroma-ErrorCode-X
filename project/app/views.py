from django.http.response import HttpResponse
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages 
# Create your views here.

def home(request):
    return  render(request,"index.html")

def contact(request):
    return  render(request,"contact.html")

def handleblog(request):
    return render(request,"blog.html")


def about(request):
    return render(request,"about.html")    


def services(request):
    return render(request,"services.html")      

def handleLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        myuser = authenticate(username=username,password=pass1)
        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Successful")
            return redirect('/')
        else:
            messages.error(request,"Invalid Credientials")    


    return render(request,"login.html")   

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        firstname = request.POST.get('fname') 
        lastname =  request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
         
        if pass1!= pass2:
            messages.warning(request,"Passwords do not match!")
            return redirect('/signup')
        try:
            if User.objects.get(username = username):
                messages.warning(request,"Username is already taken!")
                return redirect('/signup')
        except Exception as identifier:
            pass   

        try:
            if User.objects.get(email = email):
                messages.warning(request,"Email is already taken!")
                return redirect('/signup')
        except Exception as identifier:
            pass   

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name=firstname
        myuser.last_name=lastname
        myuser.save()
        messages.success(request,"Please Login to continue")
        return redirect('/login')        
    return render(request,"signup.html")   

def dev(request):
    return render(request,"dev.html")