from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User,Task,UserProfile,WorkRequest

# admin.site.register(User)
admin.site.register(Task)
admin.site.register(UserProfile)
admin.site.register(WorkRequest)