#accounts models.py
from django.db import models
from django.contrib.auth.models import User

class LogEntry(models.Model):
    command = models.CharField(max_length=255)
    approved = models.BooleanField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.command} - {self.approved} at {self.timestamp}"

class LoginEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Null for failed logins without user
    success = models.BooleanField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'User ' + self.user.username if self.user else 'Unknown user'} - {'Success' if self.success else 'Failed'} at {self.timestamp}"