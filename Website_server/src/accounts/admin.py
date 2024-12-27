from django.contrib import admin
from django import forms
from .models import UserProfile


# Register your models here.
# Admin panel layout:
#   Approve users
#   Set their accesslevel (see models.py for options)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_approved', 'role', 'access_level', 'special_permission')
    list_filter = ('is_approved', 'role', 'access_level', 'special_permission')
    # Actions to apply to the users
    actions = ['approve_users', 'update_access_level']

    # action to approve users
    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected users have been approved.")
    approve_users.short_description = "Approve selected users"
    
    def update_access_level(self, request, queryset):
        pass
        #self.message_user(request, f"Selected users have been updated with access level {new_access_level}.")
    update_access_level.short_description = "Update access level for selected users"

