from django.urls import path, include
from app import views
from django.contrib import admin

urlpatterns = [
    path('',views.home,name="home"),
    path('contact',views.contact,name="contact"),
    path('about',views.about,name="about"),
    path('services',views.services,name="services"),
    path('login',views.handleLogin,name="handleLogin"),
    path('signup',views.signup,name="signup"),
    path('logout',views.handleLogout,name="handleLogout"),
    path('news',views.news,name="news"),
    path('dev',views.dev,name="dev"),
    path('quiz',views.quiz,name="quiz"),
    path('accounts/', include('allauth.urls')),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    path('request-reset-email/',views.RequestResetEmailView.as_view(),name='request-reset-email'),
    path('set-new-password/<uidb64>/<token>',views.SetNewPasaswordView.as_view(),name='set-new-password'),
    path('profile',views.profile,name="profile"),
]
