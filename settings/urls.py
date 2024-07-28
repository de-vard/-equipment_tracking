"""
URL configuration for settings project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.post_office, name='post_office')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='post_office')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from allauth.account import views as allauth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # django-allauth
    path('accounts/login/', allauth_views.login, name='account_login'),
    path('accounts/logout/', allauth_views.logout, name='account_logout'),
    path("accounts/signup/", allauth_views.signup, name='account_signup'),



    # Local apps
    path('', include('post_office.urls')),
    path('equipment/', include('equipment.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
