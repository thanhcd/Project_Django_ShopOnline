from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('api/register/', views.api_register, name='api_register'),
    path('api/login/', views.api_login, name='api_login'),

    path('logout/', views.logoutUser, name = "logout"),
    path('create-items/', views.createItems, name="create-items"),
    path('items/<int:pk>/update/', views.update_item, name="update-item"),
    path('items/<int:pk>/delete/', views.delete_item, name="delete-item"),
    path('items/<int:pk>/view/', views.view_item, name="view-item"),

    path('delete-message/<str:pk>/', views.deleteMessage, name = "delete-message"),
    
    path('item/<str:pk>/', views.item, name = "item"),
    path('index/', views.indexPage, name = "index"),
    path('shop/', views.shopPage, name = "shop"),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)