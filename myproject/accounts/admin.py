#accounts admin.py
from django.contrib import admin
from .models import LogEntry, LoginEntry

admin.site.register(LogEntry)
admin.site.register(LoginEntry)