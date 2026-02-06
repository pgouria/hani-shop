from django.urls import path

from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('products', views.products, name='products'),
    path('variants', views.variants, name='variants'),
    path('products/delete/<int:id>', views.delete_product, name='delete_product'),
    path('variants/delete/<int:id>', views.delete_variant, name='delete_variant'),
    path('products/edit/<int:id>', views.edit_product, name='edit_product'),
    path('variants/edit/<int:id>', views.edit_variant, name='edit_variant'),
    path('orders', views.orders, name='orders'),
    path('orders/detail/<int:id>', views.order_detail, name='order_detail'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-variant/', views.add_variant, name='add_variant'),
    path('add-category/', views.add_category, name='add_category'),
]
