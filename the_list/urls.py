from django.urls import path
from .views import (index, product_change, product_remove, product_add,
                    product_change_status, clean_user_products_full)

app_name = "the_list"


urlpatterns = [
    path('', index, name='list_products'),
    path('history/clean_history/', clean_user_products_full, name='product_history_clean'),
    path('search/', index, name='search'),

    path('product-add/', product_add, name='product_add'),
    path('product_change/<slug:product_slug>/', product_change, name='product_change'),
    path('product_change_status/<slug:product_slug>/', product_change_status, name='product_change_status'),
    path('product_delete/<slug:product_slug>/', product_remove, name='product_remove'),
]
