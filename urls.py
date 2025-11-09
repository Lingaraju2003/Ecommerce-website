from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
    path('register/', views.register_view, name='register'),
  
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/products/', views.admin_products, name='admin_products'),
    path('dashboard/orders/', views.admin_orders, name='admin_orders'),


    path('admin/orders/<int:order_id>/update/', views.update_order_status, name='update_order_status'),
]
