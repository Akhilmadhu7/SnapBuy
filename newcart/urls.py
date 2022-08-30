
from django.urls import path
from . import views



urlpatterns=[

    path('addcart/<int:pro_id>/',views.addcartview,name='addtocart'),

    path('cart-inc/<int:id>/',views.inc_cartq,name='increase-cartq'),

    path('',views.cart_view,name='cart_view'),

    path('removecart/<int:id>/',views.remove_cart_view,name='cart_remove'),

    path('remove/<int:id>/',views.remove_cartproduct_view, name='cartproduct_remove'),

    path('checkout',views.checkout_view, name='itemcheckout'),

    path('check-address',views.checkout_addaddress,name='checkout_address'),

    path('make-payment',views.makepayment,name='make_payment'),

    path('place-order',views.placeorder_view,name='placeorder'),

    path('vieworder',views.myorder_view,name='myorder'),

    path('orderinfo/<int:id>/',views.orderinfo_view,name='myorderinfo'),

    path('returnorder/<int:id>/',views.return_order,name='return_order'),

    path('removeorder/<int:id>/',views.remove_order_view,name='order_remove'),

    path('proceed-to-pay',views.razorpay_view,name='razorpay'),

    path('invoice',views.invoice_view,name='invoice'),

    path('coupon',views.apply_coupon,name='applycoupon')


]

htmx_urlpatterns = [
    # path('removecart/<int:id>/',views.remove_cart_view,name='cart_remove'),   
]

urlpatterns += htmx_urlpatterns