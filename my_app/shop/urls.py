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
    path('user/', views.user_info, name='user'),
    #  path('update_user_info/', views.update_user_info, name='update_user_info'),  # Thêm đường dẫn mới
    

    path('logout/', views.logoutUser, name = "logout"),
    path('create-items/', views.createItems, name="create-items"),
    path('items/<int:pk>/update/', views.update_item, name="update-item"),
    path('items/<int:pk>/delete/', views.delete_item, name="delete-item"),
    path('items/<int:pk>/view/', views.view_item, name="view-item"),

    path('delete-message/<str:pk>/', views.deleteMessage, name = "delete-message"),
    
    path('item/<str:pk>/', views.item_details, name = "item"),
    path('index/', views.indexPage, name = "index"),
    path('shop/', views.shopPage, name = "shop"),
    path('why/', views.whyPage, name = "why"),
    path('testimonial/', views.testimonialPage, name = "testimonial"),
    path('contact/', views.contactPage, name = "contact"),

    path('shop/', views.shopPage, name = "shop"),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:pk>/', views.update_cart_item, name='cart_updateItem'),
    path('checkout/', views.checkoutPage, name='checkoutpage'),

    path('cart/delete-item/', views.cart_deleteItem, name='cart_deleteItem'),

    path('related_pro/', views.related_pro, name = "related_pro"),


    
    
    # path('checkout/', views.checkout, name='checkout'),
    # path('checkout/success/', views.checkout_success, name='checkout_success'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)