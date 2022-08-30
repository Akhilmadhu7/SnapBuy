


from django.shortcuts import redirect, render
from category_adminside.models import Category,Product
from category_adminside.models import ProductOffer, CategoryOffer

from newcart.models import CartItem,Cart
from newcart.views import _cart_id_
from . models import Wishlist,WishlistItem
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import datetime 
import pytz


tz_india = pytz.timezone("Asia/Kolkata")



def productlist_view(request,id,cf= 0,of=None):
    
    products = Product.objects.filter(category_name=id)
    category = Category.objects.all()
    recent_p = Product.objects.exclude(category_name = id)[:3]

    c = datetime.datetime.now(tz_india).strftime("%d/%m/%Y, %H:%M:%S") 
    

    for p in products:
        
        try:
            ct = CategoryOffer.objects.get(category = id)
            
            a = ct.valid_to.strftime("%d/%m/%Y, %H:%M:%S")
            
            if ct.valid_to.strftime("%d/%m/%Y, %H:%M:%S") > c:
                
                cf = int(p.price - (p.price * (ct.offer/100)))
                
            if a < c:
           
                print('iiiiiiiiiiiiiiiii',a)
                print('hhhhhhhhhhhhhhhh',c)
                # ct.delete()
                cf = 0    
                print('rrrrrrrrrrrr',cf)
        except:
            pass
       
        try:
            of = ProductOffer.objects.get(product__id = p.id)
            print('===========================================',(of,of.product.product_name),of.product.price,of.product.id)
        except:
            print('ababababababababab',p.id,of)
            pass   
        
        try:        
            print('==================',of.product.id ,  p.id,'============')
            if of.product.id == p.id:
                of.valid_to = of.valid_to.strftime("%d/%m/%Y, %H:%M:%S")
                if of.valid_to > c:
                    print('aaaaaaaaaaaaaaaaa',of.valid_to)
                    op = int(p.price - (p.price * (of.offer/100)))
                    if op <= cf or cf == 0:
                        p.discount_price = op
                        print(p.discount_price,cf,op)
                        print('productoffer',of.offer)
                        p.save()
                    else:
                        p.discount_price = cf
                        print('dddddddddddd',p.discount_price)
                        print('catoffer',ct.offer)
                        p.save()
                if of.valid_to < c:
                    print(of.valid_to,'pppppppppppp',c)
                    print(';jsdhfjkashfkjashfks')
                    
                    if cf != 0:
                        p.discount_price = cf
                        print('catoffer')
                    else:
                            p.discount_price = 0     #None
                    of.delete()
                    p.save()
            else:
                if cf != 0:
                    p.discount_price = cf
                    print('yyyyyyyyyyyyyyyyyyyyy',p.discount_price)
                    print('catoffer')
                    p.save()
                else:    
                    p.discount_price = 0        #None
                    print('noooooooooooo',p.discount_price)
                    p.save()
        except:
            if cf != 0:
                    p.discount_price = cf
                    print('yesssssssssssssss',p.discount_price)
                    print('catoffer')
                    p.save()
            else:    
                    p.discount_price =0             # None
                    print('noooooooooooo',p.discount_price)
                    p.save()    

    
    

    context = {
        'products':products,
        'category':category,
        'recent_p':recent_p 
        
    }
    return render(request,'categories/productslist.html',context)


    

def productsdetails_view(request,id,wishitem=0,d=0,cartitem=None):
    
    products = Product.objects.get(id=id)
    
    

    if request.user.is_authenticated:
        try:
            cartitem = CartItem.objects.filter(user=request.user,product=products)
            wishitem = WishlistItem.objects.filter(user = request.user,product = products)
        except ObjectDoesNotExist:
            pass
    else:  
        try:  
            cart = Cart.objects.get(cartid = _cart_id_(request))
            cartitem = CartItem.objects.filter(cart=cart,product=products)
            wish = Wishlist.objects.get(wishlistid = _wishid_(request))
            wishitem = WishlistItem.objects.filter(wishlist=wish)
        except ObjectDoesNotExist:
            pass    


    related_products = Product.objects.filter(category_name= products.category_name).exclude(id=id)[:3]
   
    context = {
        'products':products,
        'wishitem':wishitem,
        'cartitem':cartitem,
        'related_products':related_products,
        'd':d
    }
    return render(request,'categories/productsdetails.html',context)    



def search_view(request):

    category = Category.objects.all()

    if request.method == "GET":
        searchvalue = request.GET.get('search')
        products = Product.objects.filter(product_name__icontains = searchvalue)

        product = Product.objects.exclude(product_name__icontains = searchvalue)[:3]

    context = {
        'results':products,
        'category':category,
        'product':product
    }    

    return render(request,'categories/search.html',context)   





def _wishid_(request):

    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()

    return wishlist


def add_wishlist_view(request,id):

    product_obj = Product.objects.get(id = id)
    
    if request.user.is_authenticated:

        try:
            wishitem= WishlistItem.objects.get(product = product_obj)
            if wishitem:
                wishitem = WishlistItem.objects.get(
                product = product_obj,
                user = request.user
                )
                wishitem.delete()
                
        except:
                wishitem = WishlistItem.objects.create(
                    product = product_obj,
                    user = request.user
                )
                wishitem.save()
            
    else:

        try:
            wishlist = Wishlist.objects.get(wishlistid = _wishid_(request))  

        except Wishlist.DoesNotExist:

            wishlist = Wishlist.objects.create(wishlistid = _wishid_(request))    

        try:

            wishitem= WishlistItem.objects.get(product = product_obj)

            if wishitem:
                wishitem = WishlistItem.objects.get(
                    product = product_obj,
                    wishlist = wishlist
                )  
                wishitem.delete()  

        except:
             wishitem = WishlistItem.objects.create(
                product = product_obj,
                wishlist = wishlist
            )  
             wishitem.save()     

    return redirect(wishlist_view) 




def wishlist_view(request,wishitem = 0):

    try:
        if request.user.is_authenticated:
            wishitem = WishlistItem.objects.filter(user = request.user)

        else:
            wishlist = Wishlist.objects.get(wishlistid = _wishid_(request)) 
            wishitem =  WishlistItem.objects.filter(wishlist = wishlist)

    except ObjectDoesNotExist:
        pass

    context = {
        'wishitem':wishitem
    }
    print(wishitem)
    return render(request,'cartapps/wishlist.html',context)    


def remove_wish_view(request,id):
    
    product_obj = Product.objects.get(id = id)
    wishitem = WishlistItem.objects.get(product = product_obj)
    wishitem.delete()

    return redirect(wishlist_view)