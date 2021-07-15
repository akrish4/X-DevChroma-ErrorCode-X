from django.core.mail.message import EmailMessage
from django.core.mail import EmailMessage
from django.core import mail
from django.conf import settings
from django.http.response import HttpResponse
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages 
from app.models import Contact
# Create your views here.

def home(request):
    return  render(request,"index.html")

def contact(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('num')
        description = request.POST.get('description')
        contact_query = Contact(
            name=fullname, email=email, number=phone, description=description)
        contact_query.save()
        from_email = settings.EMAIL_HOST_USER
        # email starts here
        # your mail starts here
        connection = mail.get_connection()
        connection.open()
        email_mesge = mail.EmailMessage(f'DevChroma Contact Email from {fullname}', f'Email from : {email}\nUser Query :{description}\nPhone No : {phone}', from_email, [
                                        'ananthakrishnannairrs@gmail.com'], connection=connection)
        email_user = mail.EmailMessage('DevChroma Customer Support', f'Hello {fullname}\nI hope you are doing well..\nThanks for Contacting Us, Our team is working on it & will resolve your query as soon as possible.\n\n\n\nThanks & Regards \nAnanthakrishnan \nDevChroma', from_email, [email], connection=connection)
        connection.send_messages([email_mesge, email_user])
        connection.close()
        messages.info(request, "Thanks for Contacting Us , Will get back to you soon..")
        return redirect('/contact')
    return render(request, 'contact.html')


def handleblog(request):
    return render(request,"blog.html")


def about(request):
    return render(request,"about.html")    


def services(request):
    if not request.user.is_authenticated:
        messages.error(request, "please login and try again")
        return redirect('/login')
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

def news(request):
    return render(request,"news.html")    

def handleLogout(request):
    logout(request)
    messages.success(request,"Logout Success")
    return redirect('/login')