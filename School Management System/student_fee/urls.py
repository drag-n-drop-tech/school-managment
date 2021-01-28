from django.urls import path, include
from . import views
from .api import fees_collection_view, feesDataView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('collectionFees', fees_collection_view, 'collectionFees')
router.register('feesType', feesDataView, 'feesDataView')

urlpatterns = [
    path('', include(router.urls)),
    path('fee-data', views.fee_list, name="fee_list"),
    path('new-fee-data/', views.new_fee_data, name='save_fee_data'),
    path('fee-update/<id>/', views.update_fee_data, name="update_fee"),
    path('fee-delete/<id>/', views.delete_fee_data, name='delete_fee'),
    path('fees-collection/', views.fees_collection_list, name='fees_collection_list')
]

