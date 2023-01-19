


from django.shortcuts import redirect, render
from category_adminside.models import Category,Product
from category_adminside.models import ProductOffer, CategoryOffer

from newcart.models import CartItem,Cart
from newcart.views import _cart_id_
from . models import Wishlist,WishlistItem
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils import timezone
import datetime 
import pytz

#getting indian standart time.
tz_india = pytz.timezone("Asia/Kolkata")


#function to list products.
def productlist_view(request,id,cf= 0,of=None):
    
    products = Product.objects.filter(category_name=id) #getting the products of which category which is to be displayed
    category = Category.objects.all()
    recent_p = Product.objects.exclude(category_name = id)[:3] #recent products.

    #getting current time.
    c = datetime.datetime.now(tz_india).strftime("%d/%m/%Y, %H:%M:%S") 
    #looping all the products.
    for p in products:
        try:
            ct = CategoryOffer.objects.get(category = id)   #getting the category offer object
            
            a = ct.valid_to.strftime("%d/%m/%Y, %H:%M:%S") # getting category offer starting time.
            print('aaaaa',a)
            print('ccccc',c)
            #if cat offer starting time is greater than currentitme or not.
            if ct.valid_to.strftime("%d/%m/%Y, %H:%M:%S") > c:
                cf = int(p.price - (p.price * (ct.offer/100)))  #converting real price into discount price.
            #if cat offer starting time is less than current time.
            if a < c:   #then assign cat offer = 0(bcoz the offer has come to end)
                print('iiiiiiiiiiiiiiiii',a)
                print('hhhhhhhhhhhhhhhh',c)
                # ct.delete()
                cf = 0    
                print('rrrrrrrrrrrr',cf)
        except:
            pass
        try:
            #getting the productoffers, if the products of the category have any product offer.
            #of is productoffer
            of = ProductOffer.objects.get(product__id = p.id)
            print('===========================================',(of,of.product.product_name),of.product.price,of.product.id)
        except:
            print('ababababababababab',p.id,of)
            pass   
        
        try:        
            print('==================',of.product.id ,  p.id,'============')
            #if productoffer product and category prodcut is same(then the product has product offer).
            if of.product.id == p.id:
                of.valid_to = of.valid_to.strftime("%d/%m/%Y, %H:%M:%S") #product offer ending date.
                if of.valid_to > c: #if product offer ending date is greater than current time, then offer is still valid.
                    print('aaaaaaaaaaaaaaaaa',of.valid_to)
                    #op is product offer discount price.
                    op = int(p.price - (p.price * (of.offer/100))) #converting real price into discount price.
                    #if product offer is less than cat offer or cat offer is 0,
                    #then assing discount price as product offer(bcoz minimum price should be displayed).
                    if op <= cf or cf == 0: 
                        p.discount_price = op
                        print(p.discount_price,cf,op)
                        print('productoffer',of.offer)
                        p.save()
                    #if prod offer is greater then assign cat offer to discount price.
                    else:
                        p.discount_price = cf
                        print('dddddddddddd',p.discount_price)
                        print('catoffer',ct.offer)
                        p.save()
                #if current time is greater(offer ends)        
                if of.valid_to < c:
                    print(of.valid_to,'pppppppppppp',c)
                    if cf != 0: #if cat offer exists, assign cat offer to discount price.
                        p.discount_price = cf
                        print('catoffer')
                    #if cat offer does not exist, then assign discount price = 0.    
                    else:
                        p.discount_price = 0     #None
                    of.delete() #then delete product offer.
                    p.save()
            #if productoffer product and category product are not same        
            else: #if cat offer exists, assing cat offer to discount price.
                if cf != 0:
                    p.discount_price = cf
                    print('yyyyyyyyyyyyyyyyyyyyy',p.discount_price)
                    p.save()
                else:    #if cat offer does not exist, then assign 0 to discount price.
                    p.discount_price = 0        #None
                    print('noooooooooooo',p.discount_price)
                    p.save()
        except: #if no product offer exists
            if cf != 0: #if cat offer exists, assign cat offer to discount price.
                    p.discount_price = cf
                    print('yesssssssssssssss',p.discount_price)
                    print('catoffer')
                    p.save()
            else:    #if cat offer does not exist, then assign discount price = 0
                    p.discount_price =0             # None
                    print('noooooooooooo',p.discount_price)
                    p.save()    
    context = {
        'products':products,
        'category':category,
        'recent_p':recent_p 
    }
    return render(request,'categories/productslist.html',context)


#product details
def productsdetails_view(request,id,wishitem=0,d=0,cartitem=None):
    
    products = Product.objects.get(id=id)
    #if the user is logged in, checking the product is in cart and wihslist
    if request.user.is_authenticated:
        try:
            cartitem = CartItem.objects.filter(user=request.user,product=products)
            wishitem = WishlistItem.objects.filter(user = request.user,product = products)
        except ObjectDoesNotExist:
            pass
    #if user is not logged in (guest user), then getting whislist and cartitem object,
    # check the product in guest user whislistiem and cartitem .  
    else:  
        try:  
            cart = Cart.objects.get(cartid = _cart_id_(request))
            cartitem = CartItem.objects.filter(cart=cart,product=products)
            wish = Wishlist.objects.get(wishlistid = _wishid_(request))
            wishitem = WishlistItem.objects.filter(wishlist=wish)
        except ObjectDoesNotExist:
            pass   
    #related products.     
    related_products = Product.objects.filter(category_name= products.category_name).exclude(id=id)[:3]
    context = {
        'products':products,
        'wishitem':wishitem,
        'cartitem':cartitem,
        'related_products':related_products,
        'd':d
    }
    return render(request,'categories/productsdetails.html',context)    

#search products.
def search_view(request):

    category = Category.objects.all()
    if request.method == "GET":
        searchvalue = request.GET.get('search') #product or category name
        products = Product.objects.filter(product_name__icontains = searchvalue) #getting the products according to the searchvalue.
        product = Product.objects.exclude(product_name__icontains = searchvalue)[:3]
    context = {
        'results':products,
        'category':category,
        'product':product
    }    
    return render(request,'categories/search.html',context)   


#create session for guest user.
def _wishid_(request):

    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist

#add product to wishlist.
def add_wishlist_view(request,id):

    product_obj = Product.objects.get(id = id) #getting the product ,which is to be added into wishlist.
    if request.user.is_authenticated:

        try:    #if the product is already in wishlist, then remove
            wishitem= WishlistItem.objects.get(product = product_obj)
            if wishitem:
                wishitem = WishlistItem.objects.get(
                product = product_obj,
                user = request.user
                )
                wishitem.delete()  
        except: #if product is not in wishlist, then create 
                wishitem = WishlistItem.objects.create(
                    product = product_obj,
                    user = request.user
                )
                wishitem.save()
    #if guest user(not logged in)   
    else:
        try:  #collect wishlist using session 
            wishlist = Wishlist.objects.get(wishlistid = _wishid_(request))  
            print('here not try')
        except Wishlist.DoesNotExist:
            wishlist = Wishlist.objects.create(wishlistid = _wishid_(request))   
            print('here not except ') 

        try: #if wishlist and the product is already in wishlist, then remove 
            wishitem= WishlistItem.objects.get(product = product_obj)
            if wishitem:
                wishitem = WishlistItem.objects.get(
                    product = product_obj,
                    wishlist = wishlist
                )  
                wishitem.delete()  
        except:  #if product is not in wishlist, then create
             wishitem = WishlistItem.objects.create(
                product = product_obj,
                wishlist = wishlist
            )  
             wishitem.save()     
    return redirect(wishlist_view) 



#list wihslist products.
def wishlist_view(request,wishitem = 0):

    try:    #if user loggedin collect all user wishlist products
        if request.user.is_authenticated:
            wishitem = WishlistItem.objects.filter(user = request.user)
        else:   #if guest user, collect all the wishlist products using session
            wishlist = Wishlist.objects.get(wishlistid = _wishid_(request)) 
            wishitem =  WishlistItem.objects.filter(wishlist = wishlist)
    except ObjectDoesNotExist:
        pass
    context = {
        'wishitem':wishitem
    }
    print(wishitem)
    return render(request,'cartapps/wishlist.html',context)    

#remove wish item 
def remove_wish_view(request,id):
    
    product_obj = Product.objects.get(id = id)
    if request.user.is_authenticated:
        wishitem = WishlistItem.objects.get(Q(product = product_obj) & Q(user=request.user))
        wishitem.delete()
    else:
        wishlist = Wishlist.objects.get(wishlistid = _wishid_(request)) 
        wishitem = WishlistItem.objects.get(Q(product=product_obj) & Q(wishlist=wishlist))
        wishitem.delete()

            

    return redirect(wishlist_view) 