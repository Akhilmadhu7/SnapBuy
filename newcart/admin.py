
from django.contrib import admin
from . models import  Cart, CartItem, Coupon, Order, OrderProduct, UsedCoupon, UserProfile,AddAddress


# Register your models here.


admin.site.register(Cart)


admin.site.register(CartItem)

admin.site.register(Order)

admin.site.register(OrderProduct)

admin.site.register(UserProfile)

admin.site.register(AddAddress)

admin.site.register(Coupon)

admin.site.register(UsedCoupon)

