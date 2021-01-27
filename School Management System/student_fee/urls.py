from django.urls import path
from . import views

urlpatterns = [
    path('fee-data', views.fee_list, name="fee_list"),
    path('new-fee-data/', views.new_fee_data, name='save_fee_data'),
    path('fee-update/<id>/', views.update_fee_data, name="update_fee"),
    path('fee-delete/<id>/', views.delete_fee_data, name='delete_fee'),
]

