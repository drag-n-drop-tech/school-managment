
from django.urls import path, include
from . import views

urlpatterns = [
    path('add_assignment',views.add_assignment,name="add_assignment"),
    path('edit_assignment/<id>/',views.edit_assignment,name="edit_assignment"),
    path('delete_assignment/<id>/',views.delete_assignment,name="delete_assignment"),
    path('add_assignment_files/<id>/',views.add_assignment_files,name="add_assignment_files"),
    path('delete_assignment_files/<id>/',views.delete_assignment_files,name="delete_assignment_files"),
]



