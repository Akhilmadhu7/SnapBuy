
from . models import Cart,CartItem
from . views import _cart_id_
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from category_adminside.models import Category


#fucntion to get the count of cartitems to show in navbar.
def cart_count(request):
    count = 0
    cat_list = Category.objects.all()
    #if user
    if request.user.is_authenticated:  
        try :
            cart_product = CartItem.objects.filter(user = request.user).order_by('-id')[:2] #getting last two cart item products.
            #getting all the cartitem products count.
            count = CartItem.objects.filter(user = request.user).aggregate(Count('quantity')).get('quantity__count') 
            print(cart_product)
        except :
            pass
    else:   #if guest user(not logged in)
        try:
            cart = Cart.objects.filter(cartid = _cart_id_(request)) #getting the cart using session id
            cart_product = CartItem.objects.filter(cart__in = cart).order_by('id')[:2] #getting the guest user cartitem
            print('cartpproduct is ',cart_product)
            count = CartItem.objects.filter(cart__in = cart).aggregate(Count('quantity')).get('quantity__count')  #getting the count of cartiem products.
        except :
            pass  
    context = {
        'cat_list':cat_list,
        'cart_product':cart_product,
        'count':count,
    }    
    return dict(context)    