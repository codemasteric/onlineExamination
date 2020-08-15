from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('change_password', views.change_password, name='change_password'),
    path('logout', views.logout, name='logout'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

]
