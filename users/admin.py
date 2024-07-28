from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from users.forms import CustomUserCreationForm, CustomUserChangeForm

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = (
        ('Должность/одел ', {'fields': ('department', 'job_title')}), *UserAdmin.fieldsets
    )
    list_display = ('username', 'department', 'job_title')


admin.site.register(CustomUser, CustomUserAdmin)
