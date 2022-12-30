

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ObjectDoesNotExist
import re
from django.contrib import messages


from . models import AddAddress, CartItem,Cart, Coupon, Order, OrderProduct,UserProfile,UsedCoupon
from category_adminside.models import Product
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control





def _cart_id_(request):                 ####CREATE CARTID FOR GUEST USERS
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart   
    

def couponprice(request,total):         #CALCULATE TOTAL PRICE AFTER APPLYING COUPON

    if 'coupon' in request.session:
        coupon = request.session['coupon']
        coupons = Coupon.objects.get(coupon_code = coupon)
        couponoffer = coupons.discount_percentage
        print(total)
        total = int(total - (total * (couponoffer/100)))
        print(total)

    else:
        total = total    
    return total    


def checkoffer(cart_item):
    
    if cart_item.product.discount_price:
        discount = cart_item.product.discount_price
    else:
        discount = cart_item.product.price

    return discount


def addcartview(request,pro_id):        #ADD TO CART FUNCTION

    product_obj = Product.objects.get(id = pro_id)
    cat_id = product_obj.category_name.id
    

    if request.user.is_authenticated:
        try:
            cart_items = CartItem.objects.get(
                product=product_obj, user = request.user
            )
            # if cart_items:
            #     cart_items.delete()
            cart_items.quantity += 1
            cart_items.save()

        except:
            cart_items = CartItem.objects.create(
                product=product_obj, user = request.user, quantity =1
            )  
            cart_items.save()  
    else:
        try:
            cart = Cart.objects.get(cartid = _cart_id_(request))
            
            
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cartid = _cart_id_(request))
            
            cart.save()   

        try:
           cart_items = CartItem.objects.get(
            cart = cart,  product = product_obj
            )
        #    if cart_items:
        #       cart_items.delete()
           cart_items.quantity += 1
           cart_items.save()

        except CartItem.DoesNotExist:
           cart_items = CartItem.objects.create(
             cart = cart,
             product=product_obj,
             quantity = 1
            )
           cart_items.save()

     
    return redirect(cart_view)
    # return redirect('products_list',id=cat_id)
    

    
def inc_cartq(request,id):          #TO INCREASE THE CART PRODUCT QUANTITY
    
    product_obj = Product.objects.get(id=id)
   

    if request.user.is_authenticated:
        try:
            cart_items = CartItem.objects.get(user = request.user,product=product_obj)
            cart_items.quantity += 1
            cart_items.save()
        except:
            cart_items = CartItem.objects.create(
                product=product_obj, user = request.user, quantity =1
            )  
            cart_items.save() 
    
    else:
        try:
            cart = Cart.objects.get(cartid = _cart_id_(request))
            cart_items = CartItem.objects.get(cart = cart, product = product_obj)
            cart_items.quantity += 1
            cart_items.save()
        except:
            cart = Cart.objects.create(cartid = _cart_id_(request))
            cart_items = CartItem.objects.create(
                product=product_obj, cart = cart, quantity =1
            )  
            cart_items.save()  
                     

    return redirect(cart_view)



def cart_view(request,total=0,quantity=0,cart_items=0):   #CART VIEW FUNCTION
    try:

        if request.user.is_authenticated:
           
           cart_items = CartItem.objects.filter(user = request.user,is_active=True)
           
        else:

            cart = Cart.objects.get(cartid = _cart_id_(request))   
            cart_items = CartItem.objects.filter(cart=cart, is_active = True)

        for cart_item in cart_items:
            

            total += checkoffer(cart_item) * cart_item.quantity
            quantity += cart_item.quantity

        # address1 = AddAddress.objects.filter(user = request.user)    

        
        
    except ObjectDoesNotExist:
        pass
      

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        # 'address1':address1
        
    }
    
    return render(request,'cartapps/cart.html',context)





def remove_cart_view(request,id):       #TO REMOVE THE QUANTITY OF CART PRODUCTS

    product_obj = Product.objects.get(id=id)
    # product_obj = get_object_or_404(id=id)

    if request.user.is_authenticated:

        cart_items = CartItem.objects.get(user=request.user, product = product_obj)

        if cart_items.quantity > 1:
        
            cart_items.quantity -= 1
            cart_items.save()

        else:

            cart_items.delete()  
            # return redirect(cart_view) 
          
    else:

        cart = Cart.objects.get(cartid = _cart_id_(request))
        cart_items = CartItem.objects.get(cart = cart, product = product_obj)
        
        if cart_items.quantity>1:
            cart_items.quantity -= 1
            cart_items.save() 

        else:

            
            cart_items.delete()   

    # return render(request,'cartapps/cart.hmtl')
    return redirect(cart_view)
    



def remove_cartproduct_view(request,id):    #TO DELETE CART PRODUCT

    product_obj = Product.objects.get(id = id)

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(product = product_obj)
        cart_items.delete()

    else:
        cart_items = CartItem.objects.filter(product=product_obj)
        cart_items.delete()    

    return redirect(cart_view)    



@login_required(login_url='userlog')
def checkout_view(request,total=0,quantity=0,cart_items=0):

    totaltax = 0
    

    try:

        if request.user.is_authenticated:
           
           cart_items = CartItem.objects.filter(user = request.user,is_active=True)

        else:

            cart = Cart.objects.get(cartid = _cart_id_(request))   
            cart_items = CartItem.objects.filter(cart=cart, is_active = True)

        for cart_item in cart_items:


            total += checkoffer(cart_item) * cart_item.quantity
            quantity += cart_item.quantity

            totaltax = int(totaltax+( (checkoffer(cart_item) * cart_item.quantity) / 1200))
             
            
               
        shipping = 100 
        total = couponprice(request, total) 
        

        grandtotal = total + totaltax + shipping    
        
    except ObjectDoesNotExist:
        pass
    

    userprofile = UserProfile.objects.filter(user = request.user).first()

    address = AddAddress.objects.filter(user = request.user)
    context = {

        'totaltax':totaltax,
        'shipping':shipping,
        'grandtotal':grandtotal,
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'userprofile': userprofile,
        'address':address,
        
    }
    return render(request,'cartapps/checkout.html',context)



@login_required(login_url='userlog')
def makepayment(request,total=0,quantity=0,cart_items=0):


    totaltax = 0
    

    try:

        if request.user.is_authenticated:
           
           cart_items = CartItem.objects.filter(user = request.user,is_active=True)

        else:

            cart = Cart.objects.get(cartid = _cart_id_(request))   
            cart_items = CartItem.objects.filter(cart=cart, is_active = True)

        for cart_item in cart_items:


            total += checkoffer(cart_item) * cart_item.quantity
            quantity += cart_item.quantity

            totaltax = int(totaltax+( (checkoffer(cart_item) * cart_item.quantity) / 1200))
        # try:    
        #     if total > 75000:
        #         coupon = Coupon.objects.all().first
        #     else:
        #         coupon = None    
        # except:
        #     pass        
            
               
        shipping = 100 
        total = couponprice(request, total) 
        # if couponoffer != 0:
        #     total = int(total - (total * (couponoffer/100)))

        grandtotal = total + totaltax + shipping    
        
    except ObjectDoesNotExist:
        pass
    # if total > 75000:
    #         coupon = Coupon.objects.all().first 

    userprofile = UserProfile.objects.filter(user = request.user).first()

    # address = AddAddress.objects.filter(user = request.user)
    if request.method == 'POST':
        
        addid = request.POST.get('addid')

    try:    
        address = AddAddress.objects.get(id = addid)
    except:
        messages.error(request,'Choose an Address to make payment')  
        return redirect(checkout_view) 

    context = {

        'totaltax':totaltax,
        'shipping':shipping,
        'grandtotal':grandtotal,
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'userprofile': userprofile,
        'address':address,
        # 'coupon':coupon
    }

    return render(request,'cartapps/placeorder.html',context)


@login_required(login_url='userlog')
def checkout_addaddress(request):


    if request.method == 'POST':

        user = request.user
        name = request.POST.get('name')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phone_number')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        country = request.POST.get('country')
        newaddress = request.POST.get('address')

        username_pattern = "^[A-Za-z\s]{3,}$"       #username verify pattern
        username_verify = re.match(username_pattern,name)


        if username_verify is None:  #
            messages.error(request,'Name should contian only characters')
            return redirect(makepayment)


        email_pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"       #email verify pattern
        email_verify = re.match(email_pattern,email)


        if email_verify is None:
            messages.error(request,'Invalid Email')
            return redirect(makepayment)


        addadress = AddAddress.objects.create(

                user = user, name = name, email = email, newaddress = newaddress, city = city,
                phonenumber = phonenumber, pincode = pincode, state = state, country = country

        )

        addadress.save()
        messages.success(request,'Address added succesfully')

    return redirect(makepayment)



@login_required(login_url='userlog')
def placeorder_view(request,total=0,quantity=0,order=0):

    
    cart_items = CartItem.objects.filter(user = request.user)
    
    totaltax = 0
    
    for cart_item in cart_items:

        total += checkoffer(cart_item)* cart_item.quantity
        quantity += cart_item.quantity
        totaltax = int(totaltax+( (checkoffer(cart_item) * cart_item.quantity) / 1200))
    
    shipping = 100
    total = couponprice(request,total)
    grandtotal = totaltax +total +shipping 

    if 'coupon' in request.session:
            # coupons = request.session['coupon']
            coupons = Coupon.objects.get(coupon_code = request.session['coupon'])
            print(coupons)
            try:
                print('sjdhfjkshakdjhfsadfkl')
                UsedCoupon.objects.create(coupon = coupons,user = request.user)
                print('sdfsdfsadgasdg',UsedCoupon.coupon)
                UsedCoupon.save()
                del request.session['coupon']
                
            except:
                pass   

    if 'coupon' in request.session:
        del request.session['coupon']   

    if request.method == 'POST':

        if not AddAddress.objects.filter(user =request.user):  # if the logged in user have no address then it will create one.
            
                    user = request.user
                    name = request.POST.get('name')
                    email = request.POST.get('email')
                    phonenumber = request.POST.get('phone')
                    city = request.POST.get('city')
                    pincode = request.POST.get('pincode')
                    state = request.POST.get('state')
                    country = request.POST.get('country')
                    newaddress = request.POST.get('address')

                    addadress = AddAddress.objects.create(

                            user = user, name = name, email = email, newaddress = newaddress, city = city,
                            phonenumber = phonenumber, pincode = pincode, state = state, country = country

                    )

                    addadress.save()
        if not UserProfile.objects.filter(user = request.user):
            userp = UserProfile()
            userp.user = request.user
            userp.save()
        
        user = request.user
        customername = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')

        paymentmode = request.POST.get('paymentmode')
        payment_id = request.POST.get('payment_id')

        print(customername)
        username_pattern = "^[A-Za-z\s]{3,}$"       
        username_verify = re.match(username_pattern,customername)


        if username_verify is None:  
            messages.error(request,'Name should contian only characters')
            return redirect(checkout_view)


        email_pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"       
        email_verify = re.match(email_pattern,email)


        if email_verify is None:
            messages.error(request,'Invalid Email')
            return redirect(checkout_view)    
       

        neworder = Order.objects.create(

            user = user, customername = customername, phone=phone, email=email, address=address,
            pincode = pincode, city = city, state = state, country = country, tax = totaltax, 
            paymentmode = paymentmode, shippping = shipping, grandtotal = grandtotal, 
            total_price = total, payment_id=payment_id
        )
        
        neworder.save()  

        orderitem = CartItem.objects.filter(user=request.user)
        for item in orderitem:

            # CREATING ORDER PRODUCTS
            order =OrderProduct(
                    order = neworder,
                    price = checkoffer(item),
                    product = item.product,
                    quantity = item.quantity,
            )
            order.save()
            
           

            # TO DECREASE THE STOCK OF THE PRODUCT

            orderproduct = Product.objects.filter(id=item.product.id).first()
            orderproduct.stock = orderproduct.stock - item.quantity
            orderproduct.save()
             
        # DELETE THE CARTITEMS FROM FROM CART

        CartItem.objects.filter(user = request.user).delete()

        paymode = request.POST.get('paymentmode')

        
        if ( paymode == "paid by razorpay" or paymode == "paid by paypal"):
            
            return JsonResponse({
                'status': 'Your order has been placed succesfully'
            })
        
        # return render(request,'cartapps/invoice.html',context)
        return redirect(invoice_view)
        

    else:
        
        return render(request,'cartapps/checkout.html')
        



def razorpay_view(request,total=0,quantity=0):          #razorpay function

    cart_items = CartItem.objects.filter(user = request.user)
    
    totaltax = 0
    
    for cart_item in cart_items:

        
        total += checkoffer(cart_item) * cart_item.quantity
        quantity += cart_item.quantity
        totaltax = int(totaltax+( (checkoffer(cart_item) * cart_item.quantity) / 1200))

    shipping = 100
    grandtotal = totaltax+total+shipping 
   

    return JsonResponse({
        'grandtotal':grandtotal
    })
    



def invoice_view(request,a=0,b=0,coupon=0):

    try: 
        orders = Order.objects.last()
        order = OrderProduct.objects.filter(order = orders)
        
        for o in order:
            a += o.product.price * o.quantity
          
            if o.product.discount_price:
                b += o.product.discount_price * o.quantity
            else:
                b += o.product.price * o.quantity
                
        discount = a-b
        print('discount',discount)
        coupon = b - int(orders.total_price)

    except:
        pass    
   
    context = {
        'orders':orders,
        'order':order,
        'discount':discount,
        'coupon':coupon

    }
        
    return render(request,'cartapps/invoice.html',context)


#show my total orders list.
def myorder_view(request):
    if request.user.is_authenticated:
        try:
            order = Order.objects.filter(user = request.user).order_by('-created_at')
            
            # orderproduct = OrderProduct.objects.filter(order__in = order)
        except Order.DoesNotExist:
            messages.error(request,'Something went wrong')
            return redirect('userindex')
    else:
        return render(request,'cartapps/view_order.html')      

    context = {
        'order':order,
        # 'orderproduct':orderproduct,
        # 'cartitem':cartitem
    }

    return render(request,'cartapps/view_order.html',context)




def orderinfo_view(request, id,a=0,b=0):        # a & b are variables to calculate the discount amount 
    
    try:
        orders = Order.objects.get(id = id)
        orderproduct = OrderProduct.objects.filter(order = orders)

        for o in orderproduct:
            a += o.product.price * o.quantity
            if o.product.discount_price:
                b += o.product.discount_price  * o.quantity
            else:
                b = b + o.product.price * o.quantity   
                print(b)
        print(b)
        discount = a-b
        print(discount,'ddddd')
        coupon = b  - int(orders.total_price) 
        print(coupon)
    except:
        messages.error(request,'Order does not exist')   
        return redirect(myorder_view) 
      
    
    context = {
        'orders':orders,
        'orderproduct': orderproduct,
        'discount':discount,
        'coupon':coupon
    }
    return render(request,'cartapps/neworderinfo.html',context)    




def remove_order_view(request,id):

    orders = Order.objects.get(id = id)
    orders.status ="Cancelled" 
    orders.save()

    # To increase the stock of the cancelled product
    orderproduct = OrderProduct.objects.filter(order = orders)
    for order in orderproduct:

        product = Product.objects.get(id = order.product.id)
        product.stock = product.stock + order.quantity
        product.save()
      
    return redirect(myorder_view)


def return_order(request,id):

    orders = Order.objects.get(id = id)
    orders.status ="Returned" 
    orders.save()

    # To increase the stock of the cancelled product
    orderproduct = OrderProduct.objects.filter(order = orders)
    for order in orderproduct:

        product = Product.objects.get(id = order.product.id)
        product.stock = product.stock + order.quantity
        product.save()
      
    return redirect(myorder_view)


   


def apply_coupon(request):

    if request.method =="POST":
        coupon =request.POST['coupon'] 
        print('sdafsa',coupon)
        try:
            if Coupon.objects.get(coupon_code = coupon):
                coupon_exists = Coupon.objects.get(coupon_code = coupon)

                try:
                    if UsedCoupon.objects.get(user = request.user, coupon = coupon_exists):
                        messages.error(request,'Coupon already used')
                        return redirect(checkout_view)
                        
                except:
                    request.session['coupon'] = coupon
                    print('aaaaaaaaa',coupon)
                    return redirect(checkout_view)
            else:
                messages.error(request,'Coupon does not exists')          
                return redirect(checkout_view)   

        except:
            messages.error(request,'coupon does not exist')  
            return redirect(checkout_view)         

    return redirect(checkout_view)    

    




