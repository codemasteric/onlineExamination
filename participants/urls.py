from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('change_password', views.change_password, name='change_password'),
    path('logout', views.logout, name='logout'),

]
