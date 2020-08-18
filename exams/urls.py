from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.instruction, name='instruction'),
    path('question/', views.question, name='question'),
    # path('result/', views.result, name='result'),

]
