
from django.urls import path, include
from . import views

urlpatterns = [
    path('add_assignment',views.add_assignment,name="add_assignment")
]