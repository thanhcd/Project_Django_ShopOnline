from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('items/', views.createItems, name="create-items"),
    path('login/', views.loginPage, name = "login"),
    path('register/', views.registerPage, name = "register"),
    path('logout/', views.logoutUser, name = "logout"),

    path('index/', views.indexPage, name = "index"),
    path('shop/', views.shopPage, name = "shop"),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)