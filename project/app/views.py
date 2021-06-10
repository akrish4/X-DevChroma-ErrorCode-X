from django.http.response import HttpResponse
from django.shortcuts import render,HttpResponse


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
    return render(request,"login.html")   

def signup(request):
    return render(request,"signup.html")   