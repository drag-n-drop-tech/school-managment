from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name = 'index'),
    path('aboutus', views.aboutus, name = 'aboutus'),
    path('contactus', views.contactUs, name = 'contactus'),
    path('facilities', views.facilities, name = 'facilities'),
    path('gallery', views.gallery, name = 'gallery'),
    path('pre-primary', views.pre_primary, name = 'pre_primary'),
    path('primary', views.primmary, name = 'primmary'),
    path('high-school', views.high_school, name = 'high_school'),

]
