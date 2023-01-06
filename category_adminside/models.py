from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.


class Category(models.Model):

    title =      models.CharField(max_length=200)
    details =     models.TextField()
    cat_image =   models.ImageField(upload_to='categoryimage')
    created_at =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Product(models.Model):

    product_name    = models.CharField(max_length=100)
    brand_name      = models.CharField(max_length=100)
    category_name   = models.ForeignKey(Category, on_delete=models.CASCADE)
    price           = models.PositiveIntegerField()
    ram             = models.CharField(max_length=100)
    color           = models.CharField(max_length=100)
    stock           = models.PositiveIntegerField(null=True)
    storage         = models.CharField(max_length=100)
    productimage    = models.ImageField(upload_to='product')  
    image1          = models.ImageField(null = True, upload_to = 'sideimage1')  
    image2          = models.ImageField(null = True, upload_to = 'sideimage2')
    specifications  = models.TextField()
    description     = models.TextField()
    discount_price  = models.PositiveIntegerField(null=True,blank=True)


    def __str__(self):
        return self.product_name  




class Banner(models.Model):
    bannerimage = models.ImageField(upload_to = 'banner') 
    title = models.CharField(max_length=100,null=True)  
    description = models.TextField()     
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


class ProductOffer(models.Model):

    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    offer = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(100)])
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()


    def __str__(self):
        return self.product.product_name


class CategoryOffer(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    offer = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    

    def __str__(self):
        return self.category.title
    
    