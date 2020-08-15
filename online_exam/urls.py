from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('participants.urls')),
    path('exams/', include('exams.urls')),
    path('admin/', admin.site.urls),
]
