from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Exams Administration"
admin.site.site_title = "Online Examination Sytem Administration Portal"
admin.site.index_title = "Welcome to Online Exams Admin Portal"

urlpatterns = [
    path('', include('participants.urls')),
    path('exams/', include('exams.urls')),
    path('admin/', admin.site.urls),
]
