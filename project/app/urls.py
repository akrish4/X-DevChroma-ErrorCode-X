from django.urls import path, include
from app import views
from django.contrib import admin

urlpatterns = [
    path('',views.home,name="home"),
    path('blog',views.handleblog,name="handleblog"),
    path('contact',views.contact,name="contact"),
    path('about',views.about,name="about"),
    path('services',views.services,name="services"),
    path('login',views.handleLogin,name="handleLogin"),
    path('signup',views.signup,name="signup"),
    path('logout',views.handleLogout,name="handleLogout"),
    path('news',views.news,name="news"),
    path('dev',views.dev,name="dev"),
     path('accounts/', include('allauth.urls')),
]
