
from . models import Cart,CartItem
from . views import _cart_id_
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from category_adminside.models import Category



def cart_count(request):
    count = 0
    
    
    cat_list = Category.objects.all()
    if request.user.is_authenticated:  
        try :
            cart_product = CartItem.objects.filter(user = request.user).order_by('-id')[:2]
            count = CartItem.objects.filter(user = request.user).aggregate(Count('quantity')).get('quantity__count')
            print(cart_product)
        except :
            pass
    else:
        try:
            cart = Cart.objects.filter(cartid = _cart_id_(request))

            cart_product = CartItem.objects.filter(cart__in = cart[:2]).order_by('-id')
            count = CartItem.objects.filter(cart__in = cart).aggregate(Count('quantity')).get('quantity__count')  
        except :
            pass  

        
    
 
    context = {
        'cat_list':cat_list,
        'cart_product':cart_product,
        'count':count,
       
    }    

    return dict(context)    