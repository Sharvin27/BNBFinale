# urls.py
from django.urls import path
from .views import post_product,product_list,traders,bids_page


urlpatterns = [
    path('post/', post_product, name='post_product'),
    path('products/', product_list, name='product_list'),
    path('traders/', traders, name='traders'),
    path('bids_page/', bids_page, name='bids_page'),

]
