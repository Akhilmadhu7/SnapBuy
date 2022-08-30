from django.contrib import admin

from . models import Banner, Category,Product, ProductOffer,CategoryOffer

# Register your models here.



class Productadmin(admin.ModelAdmin):
    list_display = [
        'product_name'
    ]
admin.site.register(Product,Productadmin)


class Categoryadmin(admin.ModelAdmin):
    list_display = [
        'title'
    ]
admin.site.register(Category,Categoryadmin)

class ProductOfferAdmin(admin.ModelAdmin):
  list_display = [
    'product',
    'valid_from',
    'valid_to'
  ]

admin.site.register(ProductOffer,ProductOfferAdmin)

class CategoryOfferAdmin(admin.ModelAdmin):
  list_display = [
    'category',
    'valid_from',
    'valid_to'
  ]

admin.site.register(CategoryOffer,CategoryOfferAdmin)

admin.site.register(Banner) 
