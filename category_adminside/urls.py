from django.urls import path
from . import views


urlpatterns = [

    path('banner',views.banner_view,name ='banner-view'),

    path('add-banner',views.add_banner,name='banner-add'),

    path('editbanner/<int:id>/',views.edit_banner,name='banner-edit'),

    path('deletebaneer/<int:id>/',views.delete_banner,name='delete-banner'),

    path('ad_categorylist',views.category_view,name='list_category'),

     
    path('cattegory-delete/<int:id>/',views.category_delete_view,name='delete_category'),

    # path('adlaptops',views.cat_laptop_view,name='adminlaptops'),
    path('add-category',views.addcategory_view,name='category_add'),

    path('edit-category/<int:id>/',views.editcategory_view,name = 'category-edit'),

    path('products/<int:id>/',views.productlist_view,name='productlist'),

    path('details_products/<int:id>/',views.productdetails_view,name='product_details'),

    path('add_product',views.addproduct_view,name='productadd'),

    path('editproducts/<int:id>/',views.editproduct_view,name='productedit'),

    path('deleteproduct/<int:id>/',views.deleteproduct_view,name='productdelete'),




 
]



















