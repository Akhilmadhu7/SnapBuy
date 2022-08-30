from django.urls import path
from . import views


urlpatterns = [

    path('products/<int:id>/',views.productlist_view,name='products_list'),

    path('products-details/<int:id>/',views.productsdetails_view,name='product_detial'),


    path('searchproducts',views.search_view,name='searchproduct'),

    path('wish-list/<int:id>/',views.add_wishlist_view,name='wishlist'),

    path('wishlistview',views.wishlist_view,name='wish_list'),

    path('remove-wishlist/<int:id>/',views.remove_wish_view,name = 'wishlist_remove')
]
