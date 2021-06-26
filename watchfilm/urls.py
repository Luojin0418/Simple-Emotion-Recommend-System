from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('random', views.random_get),
    path('search', views.search, name='search'),
    path('success', views.success, name='success'),
    path('recommend', views.recommend, name='recommend'),
    #path('detail',views.detail,name='detail'),
    path('detail/<name>',views.detail,name='detail'),
    path('questionnaire',views.questionnaire,name='questionnaire'),
    path('home',views.home,name='home'),
    #path('register/',views.register,name='register')
]