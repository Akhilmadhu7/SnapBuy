from django.db import models

from userhome.models import Customuser
from category_adminside.models import Product

class Cart(models.Model):
    cartid = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return 'Cart: ' + str(self.id)



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(Customuser,  on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    

    def subtotal(self):  
        
        if self.product.discount_price:
            return (self.product.price - (self.product.price - self.product.discount_price)) * self.quantity
        else:     
            return self.product.price*self.quantity


    def __str__(self):
    
        return str(self.product)



class Order(models.Model):

    user = models.ForeignKey(Customuser, on_delete=models.CASCADE)
    customername = models.CharField( max_length=50, null=False)
    phone = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=120, null=True)
    address = models.TextField(max_length=600, null=False)
    city = models.CharField(max_length=200, null=False)
    pincode = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=120, null=False)
    country = models.CharField(max_length=120, null=False)
    total_price = models.CharField(max_length=100, null=False)
    tax = models.CharField(max_length=120, null=False)
    shippping = models.CharField(max_length=100, null=False)
    grandtotal = models.CharField(max_length=120, null=False)
    paymentmode = models.CharField(max_length=120, null=False)
    payment_id = models.CharField(max_length=120, null=True)

    orderstatus = (

        ('pending','pending'),
        ('Out for shipping','Out for shipping'),
        ('Returned','Returned'),
        ('cancelled','cancelled'),
        ('Delivered','Delivered')

    )

    status = models.CharField(max_length=120, choices=orderstatus, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.customername


class OrderProduct(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()
    
    

    def __str__(self):
        return self.product.product_name



class UserProfile(models.Model):

    user = models.OneToOneField(Customuser, on_delete=models.CASCADE)
    gender_choice = (

        ('MALE','MALE'),
        ('FEMALE','FEMALE')
    )
    gender = models.CharField(max_length=120, choices=gender_choice, default='Male', null=True)
    address = models.TextField()
    city = models.CharField(max_length=200)
    pincode = models.CharField(max_length=100)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username

class AddAddress(models.Model):
    user = models.ForeignKey(Customuser, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=120)
    phonenumber = models.CharField(max_length=120, null=True)
    email = models.CharField(max_length=120, null=True)
    newaddress = models.TextField()
    city = models.CharField(max_length=120)
    pincode = models.CharField(max_length=100)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=100, unique=True)
    discount_percentage = models.IntegerField(null= True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.coupon_code


class UsedCoupon(models.Model):
    user = models.ForeignKey(Customuser, on_delete = models.CASCADE,null=True)
    coupon = models.ForeignKey(Coupon, on_delete = models.CASCADE, null=True)


    def __str__(self):
        return self.user.username
    
    




    