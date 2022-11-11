

import re

from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
# from userhome.models import Customuser
from . models import Category,Product,Banner, ProductOffer
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# Create your views here.

login_required(login_url='adminlog')
def banner_view(request):
    try:
        banner = Banner.objects.all()
    except:
        pass    
    context = {
        'banner':banner
    }
    return render(request,'cat_adminside/banner.html',context)


login_required(login_url='adminlog')
def add_banner(request):

    banner = Banner()
    if request.method == 'POST':

        banner.title = request.POST.get('title')
        banner.description = request.POST.get('description')

        if banner.title == '' :
            messages.error(request,'Title should not be empty')
            return redirect(add_banner)

        if len(request.FILES)!= 0:
            banner.bannerimage = request.FILES['image'] 
        else:
            messages.error(request,'All fields required')
            return redirect(add_banner)

        banner.save()
        messages.success(request,'Banner added succesfully')    
        return redirect(banner_view) 

    return render(request,'cat_adminside/addbanner.html')


login_required(login_url='adminlog')
def edit_banner(request,id):

    try:
        banner = Banner.objects.get(id = id)
    except:
        pass    

    if request.method == 'POST':
       banner.title = request.POST.get('title') 
       banner.description = request.POST.get('description')

       if banner.title == '':
        messages.error(request,'Title should not be empty')
        return redirect(edit_banner)

       if len(request.FILES)!= 0:
          banner.bannerimage = request.FILES['image']

       banner.save()
       return redirect(banner_view)

    context = {
        'banner':banner
    }   

    return render(request,'cat_adminside/addbanner.html',context)



def delete_banner(request,id):

    banner = Banner.objects.get(id=id)
    banner.delete()
    messages.success(request,'Banner deleted succesfully')
    return redirect(banner_view)



def search_product_view(request):
    return render(request)



login_required(login_url='adminlog')
def category_view(request):

    categories = Category.objects.all()

    return render(request,'cat_adminside/ad_categories.html',{'categories':categories})

    
login_required(login_url='adminlog')
def addcategory_view(request):

    category = Category()
    if request.method == 'POST':

        category.title = request.POST.get('title')
        category.details = request.POST.get('details')

        if len(request.FILES)!=0:
            category.cat_image = request.FILES['image']
        else:
            messages.error(request,'All fields are required')  
            return redirect(addcategory_view)

        if category.title == '':
            messages.error(request,'Title should not be empty')
            return redirect(addcategory_view)
            
        if Category.objects.filter(title = category.title).exists():
            messages.error(request,'Category already exists')    
            return redirect(addcategory_view)

          
        
        category.save()
        messages.success(request,'Category added succesfully')
        return redirect(category_view)

    return render(request,'cat_adminside/addcategory.html')



login_required(login_url='adminlog')
def editcategory_view(request,id):

    category = Category.objects.get(id = id)
    if request.method == 'POST':
        category.title = request.POST.get('title')
        category.details = request.POST.get('details')

        if category.title == '':
            messages.error(request,'Title should not be empty')
            return redirect(editcategory_view)

        if len(request.FILES)!= 0:
            category.cat_image = request.FILES['image']
        
        category.save()
        messages.success(request,'Category edited succesfully')
        return redirect(category_view)

    context = {
        'category':category
    }    
    return render(request,'cat_adminside/addcategory.html',context)    



def category_delete_view(request,id):

    categories = Category.objects.get(id=id)
    categories.delete()

    messages.success(request,'Category deleted succesfully')

    return redirect(category_view) 


login_required(login_url='adminlog')
def productlist_view(request,id):

    try:
         products = Product.objects.filter(category_name = id)
    except:
        pass     
    print(products)
    context = {
        'products':products
    }
    return render(request,'cat_adminside/product_list.html',context)



login_required(login_url='adminlog')
def productdetails_view(request,id,offer=None):

    prod_details = Product.objects.get(id = id)
    try:
        offer = ProductOffer.objects.get(product = prod_details)
    except:
        pass        
    context = {
        'prod_details':prod_details,
        'offer':offer
    }
    return render(request,'cat_adminside/product-details.html',context)  



login_required(login_url='adminlog')
def addproduct_view(request):

    categorys = Category.objects.all()
  
    context = {
        'categoryname' : categorys, 
         
    }

    if request.method == 'POST':
          
        description  = request.POST.get('description')
        specifications  = request.POST.get('shortdescription')
        ram  = request.POST.get('ram')
        color  = request.POST.get('color')
        storage  = request.POST.get('storage')
        brand_name  = request.POST.get('brand')
        price  = request.POST.get('price')
        stock = request.POST.get('stock')
        product_name = request.POST.get('productname')
        discount = request.POST.get('discount')

        if len(request.FILES)!=0:
            productimage  = request.FILES['image']
            image1 = request.FILES['image1']
            image2 = request.FILES['image2']
        else:
            messages.error(request,'Image field should not be empty')  
            return redirect(addproduct_view)  

        

        if discount =='':
            discount = None

        categorys  = request.POST.get('category')
        cat = Category.objects.get(id=categorys)
        prod_lap = Product.objects.create(

                            description=description, specifications=specifications,ram=ram,
                            color=color,storage=storage,price=price,productimage=productimage,
                            product_name=product_name,brand_name=brand_name,category_name= cat,stock=stock,discount_price=discount,
                            image1 = image1,image2 = image2

                            )            
        prod_lap.save()                    

        messages.success(request,'Product added succesfully')
        return redirect('productlist',id=categorys)

   
        
    return render(request,'cat_adminside/product_add.html',context)  

    

login_required(login_url='adminlog')
def editproduct_view(request,id):

    categorys = Category.objects.all()
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        try:
            product.description  = request.POST.get('description')
            product.specifications  = request.POST.get('shortdescription')
            product.ram  = request.POST.get('ram')
            product.color  = request.POST.get('color')
            product.storage  = request.POST.get('storage')
            product.brand_name  = request.POST.get('brand')
            product.price  = request.POST.get('price')
            product.product_name = request.POST.get('productname')
            product.discount_price = request.POST.get('discount')
            product.stock = request.POST.get('stock')
            print(product.discount_price)
            if product.discount_price == '' or None:
                product.discount_price = 0
  

            if len(request.FILES)!=0:
                try:
                    productimage = request.FILES['image']
                    if len(productimage) > 0:
                        
                        product.productimage = request.FILES['image']    
                except: 
                    pass

            if len(request.FILES)!=0:
                try:
                    image1 = request.FILES['image1']
                    if len(image1) > 0:
                        
                        product.image1 = request.FILES['image1']
                except: 
                    pass  

            if len(request.FILES)!=0:
                try:
                    image2 = request.FILES['image2']
                    if len(image2) > 0:
                       
                        product.image2 = request.FILES['image2']    
                except: 
                    pass       
           

            categorys  = request.POST.get('category')
            product.cat = Category.objects.get(id=categorys)

            product.save() 

            messages.success(request,'Product Edited succesfully')
            return redirect('productlist',id=categorys)
        except ObjectDoesNotExist:
            return redirect(category_view)  

    context = {
        'categorys':categorys,
        'product':product
    }
    return render(request,'cat_adminside/product_edit.html',context)
    


def deleteproduct_view(request,id):

    product = Product.objects.get(id=id)
    cat_id = product.category_name.id
    product.delete()
    messages.success(request,'Product deleted successfully')
    return redirect('productlist',id = cat_id)









