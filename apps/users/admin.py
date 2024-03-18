from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
# # Register your models here.
from apps.users.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username','mobile','password','is_superuser']
    search_fields = ['username']
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", 'mobile'),
            },
        ),
    )
