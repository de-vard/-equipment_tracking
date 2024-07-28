from django.urls import path
from .views import *

urlpatterns = [
    path('', EquipmentListView.as_view(), name='equipment_list'),
    path('<uuid:pk>', EquipmentDetailView.as_view(), name='equipment_detail'),
    path('search/', EquipmentResultsView.as_view(), name='search_results'),
]
