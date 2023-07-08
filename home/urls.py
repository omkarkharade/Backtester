from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('' , views.next, name='home'),
    path('nextpage/', views.next , name ='next'),
    path('result/', views.result , name ='next'),
    path('candlestick/', views.candlestick)
    
]
 