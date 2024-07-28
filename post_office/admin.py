
from django.contrib import admin
from .models import PostOffice


class PostOfficeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'index',
    )


admin.site.register(PostOffice, PostOfficeAdmin)

