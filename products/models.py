from django.db import models
from userhome.models import Customuser
from category_adminside.models import Product

# Create your models here.

class Wishlist(models.Model):
    wishlistid = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return 'Wishlist: ' + str(self.id)



class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(Customuser,  on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    




    def __str__(self):
    
        return str(self.product)
