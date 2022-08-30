from django.urls import path
from . import views

urlpatterns = [

   path('',views.adminlog_view,name='adminlog'),

    path('adhome',views.adminhome_view,name='adminhome'),

    path('adlogout',views.adminlogout_view,name='adminlogout'),

    path('adcustomers',views.admincustomers_view,name='admincustomers'),

    path('block/<int:id>/', views.blockuser, name='blockuser'),

    path('orders',views.order_admin_view,name='cart_admin'),

    path('vieworder_details/<int:id>/',views.orderdetails_view,name='vieworderdetail'),

    path('changestatus/<int:id>/',views.orderstatus_view, name='orderstatus'),

    path('sales',views.sales_view,name='viewsales'),

    path('sale-date',views.date_range_view,name='date_range'),

    path('category-offer',views.category_offer,name='c_offer'),

    path('add-category-offer',views.add_catoffer,name='add_cat_offer'),

    path('edit-category-offer/<int:id>/',views.edit_catoffer,name='edit_cat_offer'),

    path('delete-cat-offer/<int:id>/',views.delete_cat_offer,name='catoffer_delete'),

    path('product-offer',views.product_offer,name='p_offer'),

    path('add-product-offer',views.add_prodoffer,name='add_prod_offer'),

    path('edit-product-offer/<int:id>/',views.edit_prodoffer,name='edit_prod_offer'),

    path('delete-prd-offer/<int:id>/',views.delete_prod_offer,name='prodoffer_delete'),

    path('coupon',views.coupon_view,name='coupon_view'),

    path('add-coupopn',views.add_coupon,name='coupon_add'),

    path('block-coupon/<int:id>/',views.block_coupon,name='block_coupon'),

    path('delete-coupon/<int:id>/',views.coupon_delete,name='coupondelete'),

    path('coupon-used',views.used_coupon,name='usedcoupon'),

    path('delete-usedcoupon/<int:id>/',views.delete_usedcoupon,name='delete_used_coupon'),

    path('monthlyreport/<int:date>/',views.monthly_sales_view,name='monthly'),
    
    path('yearlyreport/<int:date>/',views.yearly_report,name='yearly')
]



    


