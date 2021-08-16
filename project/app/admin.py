from django.contrib import admin
from app.models import Contact
from .models import Profile

# Register your models here.


admin.site.register(Contact)

admin.site.register(Profile)