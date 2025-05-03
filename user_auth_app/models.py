from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    
    @property
    def fullname(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def __str__(self):
        return self.user.username