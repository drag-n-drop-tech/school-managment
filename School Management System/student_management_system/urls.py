from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from student_management_system import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('webapp.urls')),
    path('', include('student_management_app.urls')),
    path('fee/', include('student_fee.urls')),
    path('assignment/', include('student_assignment.urls')),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
