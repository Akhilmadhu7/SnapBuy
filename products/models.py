from django.db import models
from userhome.models import Customuser
from category_adminside.models import Product


#wishlist for guest user .
#suppose guest user wants to add products to wishlist,then we want some unique key.
#so we create a sessoin and save it into this model whenever a guest user add a product into wihslist item
#and if the user add another product, then we check if the wishlist has the same session,if yes we add the product into this guest user wihslistitem model.
#if it does not contain the same session, then it create another wishlist model and add product into whislistitem model with the wishlist object.

#note: if any doubt , watch any tutorial explaining about cart and wishlist models.
class Wishlist(models.Model):
    wishlistid = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Wishlist: ' + str(self.id)

#to save the wishlist product.
class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(Customuser,  on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return str(self.product)
