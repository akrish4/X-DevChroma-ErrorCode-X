from decimal import Context
from django.conf import settings
from django.core.mail import message
from django.http.response import HttpResponse
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages 
from app.models import Contact
import requests
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.urls import NoReverseMatch , reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes , force_text , DjangoUnicodeDecodeError 
from .utils import TokenGenerator , generate_token
from django.views.generic import View
# from django.contrib.auth.decorators import login_required

#emails
from django.core.mail import send_mail , EmailMultiAlternatives
from django.core.mail import BadHeaderError , send_mail
from django.core.mail.message import EmailMessage
from django.core.mail import EmailMessage
from django.core import mail
from django.conf import settings

# threading
import threading

# Reset Password Generator 
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .forms import  UserUpdateForm, ProfileUpdateForm

class EmailThread(threading.Thread):
    def __init__(self , email_message):
        self.email_message  = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()







class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user,token):
            user.is_active = True
            user.save()
            messages.success(request,"Account activated Successfully!")
            return redirect('/login')
        return render(request,'activatefail.html')    




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


# def handleblog(request):
   # return render(request,"blog.html")


def about(request):
    return render(request,"about.html")    


def services(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please login and try again!")
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

        user = User.objects.create_user(username,email,pass1)
        user.first_name=firstname
        user.last_name=lastname
        user.is_active=False
        user.save()
        current_site= get_current_site(requests)
        email_subject = "Activate your DevChroma Account"
        message = render_to_string('activate.html',
        {
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })
        email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
        EmailThread(email_message).start()
        messages.info(request,"We have sent you activation link to you mail!")
        return redirect('/login')   

    return render(request,'signup.html')   

def dev(request):
    return render(request,"dev.html")

def handleLogout(request):
    logout(request)
    messages.success(request,"Logout Success")
    return redirect('/login')


def quiz(request):
    return render(request,"quiz.html") 


API_KEY = 'acb74d6f02ea4fa99ea0d52025ab8e8a'

def news(request):
    country = request.GET.get('country')
    category = request.GET.get('category')
    if country:
        url = f'https://newsapi.org/v2/top-headlines?country={country}&apiKey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        articles = data['articles']
    else:
        url = f'https://newsapi.org/v2/top-headlines?category={category}&apiKey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        articles = data['articles']

    context = {
        'articles':articles
    }

    return render(request,"news.html", context)    

class RequestResetEmailView(View):
    def get(self,request):
        return render(request,'request-reset-email.html')

    def post(self,request):
        email = request.POST['email']
        user = User.objects.filter(email = email)
        if user.exists():
            current_site = get_current_site(request)
            email_subject = '[Reset Your DevChroma Password]'
            message = render_to_string('reset-user-password.html',
            {
                'domain' : '127.0.0.1:8000',
                'uid' : urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token' : PasswordResetTokenGenerator().make_token(user[0])
            })
            email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
            EmailThread(email_message).start()
            messages.success(request,"We have sent you an email with a link to reset your password")
            return render(request,'request-reset-email.html')
        else:
            messages.error(request,"There is NO account with this email id!")
            return render(request,'request-reset-email.html')


class SetNewPasaswordView(View):
    def get(self,request,uidb64,token):
        context = {
            'uidb64':uidb64,	
            'token':token
        }
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.error(request,"Password Reset Link is Invalid")
                return render(request,'request-reset-email.html')
        except DjangoUnicodeDecodeError as identifier:
            pass
        return render(request,'set-new-password.html',context)
        
    def post(self,request,uidb64,token):
        context = {
            'uidb64':uidb64,	
            'token':token
        }
        password = request.POST['pass1']
        confrim_passowrd = request.POST['pass2']
        if password != confrim_passowrd:
            messages.warning(request,"Passwords do not match")
            return render(request,'set-new-password.html',context)
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,"Password Reset Successful ,  Please Login!")
            return redirect('/login')
  
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"Something went wrong")
            return render(request,'set-new-password.html',context)

        return render(request,'set-new-password.html',context)   


def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request,'profile.html' , context)