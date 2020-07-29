from django.contrib import admin
from django.urls import path,include
from carts_app.views import user_creation
from carts_app.views import *

urlpatterns = [
    path('api/create_user',user_creation,name="add_user"),
    path('api/login',login,name="login"),
    path('api/add_items_to_carts',add_items_to_carts,name="add_items_to_cartslogin"),
    path('api/date_wise_cart_items',date_wise_cart_items,name="date_wise_cart_items"),
    path('api/user_role_mapping',user_role_mapping,name="user_role_mapping"),
    path('api/user_list',user_list,name="user_list")
]   