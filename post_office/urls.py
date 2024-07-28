from django.urls import path
from post_office.views import PostOfficeDetailView, HomePageView,AddEquipment

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path("<uuid:pk>", PostOfficeDetailView.as_view(), name='post_office'),
    path('add/equipment', AddEquipment.as_view(), name='add_equipment'),
]
