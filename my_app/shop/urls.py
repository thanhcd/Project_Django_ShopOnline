from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('room/', views.room, name="room"),
    path('login/', views.loginPage, name = "login"),
    path('register/', views.registerPage, name = "register"),
    path('logout/', views.logoutUser, name = "logout"),

    path('index/', views.indexPage, name = "index"),
    path('shop/', views.shopPage, name = "shop"),
    



]