from django.db import models

# Create your models here.
# myapp/models.py
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Admin autorisation
    is_approved = models.BooleanField(default=False)
    
    # Additional access control
    role = models.CharField(max_length=100, choices=[('admin', 'Admin'), ('editor', 'Editor'), ('viewer', 'Viewer')], default='viewer')
    access_level = models.IntegerField(default=3)
    special_permission = models.BooleanField(default=False)  # field for any specific permission

    def __str__(self):
        return self.user.username

