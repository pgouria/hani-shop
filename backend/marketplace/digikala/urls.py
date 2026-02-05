
from django.urls import path
from .views import *

urlpatterns = [ 
   
    path('orders/', display_orders, name='orders'),
    path('filter-orders/', filter_orders, name='filter_orders'),
    path('variants/', variant_list, name='variant_list'), 
    path('update_prices/', update_prices, name='update_prices'),

]
