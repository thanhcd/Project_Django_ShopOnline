from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('room/', views.room, name="room"),
    path('login/', views.loginPage, name = "login"),
    path('index/', views.indexPage, name = "index"),


]