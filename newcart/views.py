

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ObjectDoesNotExist
import re
from django.contrib import messages


from . models import AddAddress, CartItem,Cart, Coupon, Order, OrderProduct,UserProfile,UsedCoupon
from category_adminside.models import Product
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control




#create cart id for guest users to store the cart products.
def _cart_id_(request):                 
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart   
    
#calculate total price after applying coupon.
def couponprice(request,total):         

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

#fucntion to check offer
def checkoffer(cart_item):
    
    if cart_item.product.discount_price:
        discount = cart_item.product.discount_price
    else:
        discount = cart_item.product.price

    return discount

#add to cart function.
def addcartview(request,pro_id):        

    product_obj = Product.objects.get(id = pro_id) #product which is to be added on cart.
    cat_id = product_obj.category_name.id

    if request.user.is_authenticated: #if user logged in.
        try: #if the product is already in cartitem , then increase the quantity of product in cart.
            cart_items = CartItem.objects.get(
                product=product_obj, user = request.user
            )
            # if cart_items:
            #     cart_items.delete()
            cart_items.quantity += 1
            cart_items.save()

        except: #if no cartiem, then create.
            cart_items = CartItem.objects.create(
                product=product_obj, user = request.user, quantity =1
            )  
            cart_items.save()  
    else:   #if guest user(not logged in)
        try:
            cart = Cart.objects.get(cartid = _cart_id_(request)) #getting cart using session.
            
        except Cart.DoesNotExist: #if no cart, then create a new cart using session.
            cart = Cart.objects.create(cartid = _cart_id_(request))
            cart.save()   

        try: #increase the quantity of the product,if guest user cart contains the product.
           cart_items = CartItem.objects.get(
            cart = cart,  product = product_obj
            )
        #    if cart_items:
        #       cart_items.delete()
           cart_items.quantity += 1
           cart_items.save()
        #if not product in the guest user cart, then create new cartitem with the product.
        except CartItem.DoesNotExist:
           cart_items = CartItem.objects.create(
             cart = cart,
             product=product_obj,
             quantity = 1
            )
           cart_items.save()
    return redirect(cart_view)
    # return redirect('products_list',id=cat_id)


#cart veiw to all the products in cart.
def cart_view(request,total=0,quantity=0,cart_items=0): 
    try:

        if request.user.is_authenticated: #if user.
           cart_items = CartItem.objects.filter(user = request.user,is_active=True)#getting all the products in cart of the user.
        else:   #if not logged in (guest user)
            cart = Cart.objects.get(cartid = _cart_id_(request))   #getting the cart by using the session.
            cart_items = CartItem.objects.filter(cart=cart, is_active = True)#getting all the products in cart using session of the guest user.

        for cart_item in cart_items:
            total += checkoffer(cart_item) * cart_item.quantity #products total price 
            quantity += cart_item.quantity  #quantity of cart items
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


#increase the cart product quantity. 
def inc_cartq(request,id):         
    
    product_obj = Product.objects.get(id=id) #getting the product.
    if request.user.is_authenticated:
        try:
            cart_items = CartItem.objects.get(user = request.user,product=product_obj)#getting cartproduct of the user.
            cart_items.quantity += 1 #if quantity is greater than 1, then increase 1 quantity.
            cart_items.save()
        except: #if no product,then add product in cartitem.
            cart_items = CartItem.objects.create(
                product=product_obj, user = request.user, quantity =1
            )  
            cart_items.save() 
    else: #if not authenticated(guest user).
        try:
            cart = Cart.objects.get(cartid = _cart_id_(request)) #getting the cart using session.
            cart_items = CartItem.objects.get(cart = cart, product = product_obj) #if quantity is greater than 1, then decrease 1 quantity.
            cart_items.quantity += 1
            cart_items.save()
        except: #if not authenticated(guest user).
            cart = Cart.objects.create(cartid = _cart_id_(request)) #getting the cart using session.
            #if no products in cart, then add.
            cart_items = CartItem.objects.create(
                product=product_obj, cart = cart, quantity =1
            )  
            cart_items.save()           
    return redirect(cart_view)


#remove the quantity of cart products.
def remove_cart_view(request,id):

    product_obj = Product.objects.get(id=id) #getting that particular product which is to be decreased from cart.
    # product_obj = get_object_or_404(id=id)

    if request.user.is_authenticated:
        cart_items = CartItem.objects.get(user=request.user, product = product_obj)#getting cartproduct of the user.

        if cart_items.quantity > 1: #if quantity is greater than 1, then decrease 1 quantity.
            cart_items.quantity -= 1
            cart_items.save()
        else:   #if quantity is 1, then delete the remaining one quantity.
            cart_items.delete()  
            # return redirect(cart_view)  
    else: #if not authenticated(guest user).
        cart = Cart.objects.get(cartid = _cart_id_(request)) #getting the cart using session.
        cart_items = CartItem.objects.get(cart = cart, product = product_obj) #getting cartproduct of the guest user.
        
        if cart_items.quantity>1: #if quantity is greater than 1, then decrease 1 quantity.
            cart_items.quantity -= 1
            cart_items.save() 
        else:   #if quantity is 1, then delete the remaining one quantity.
            cart_items.delete()   
    # return render(request,'cartapps/cart.hmtl')
    return redirect(cart_view)
    

#remove product from cart.
def remove_cartproduct_view(request,id):    #TO DELETE CART PRODUCT

    product_obj = Product.objects.get(id = id) #getting that particular product.
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(product = product_obj) #collecting the cart products.
        cart_items.delete()
    else:
        cart_items = CartItem.objects.filter(product=product_obj) #collecting the cart products.
        cart_items.delete()    
    return redirect(cart_view)    


#checkout view to show order details.
@login_required(login_url='userlog')
def checkout_view(request,total=0,quantity=0,cart_items=0):

    totaltax = 0
    try:
        if request.user.is_authenticated:
           cart_items = CartItem.objects.filter(user = request.user,is_active=True)#getting all cartiems of the user.
        else:
            cart = Cart.objects.get(cartid = _cart_id_(request))     #if guest user,getting session id 
            cart_items = CartItem.objects.filter(cart=cart, is_active = True)#getting all cartitems using session id of guest user.

        for cart_item in cart_items:
            total += checkoffer(cart_item) * cart_item.quantity #products total price
            quantity += cart_item.quantity #quantity of cart items

            totaltax = int(totaltax+( (checkoffer(cart_item) * cart_item.quantity) / 1200)) #tax
               
        shipping = 100 
        total = couponprice(request, total)   #calculating total,if there is any coupon used by the user.
        grandtotal = total + totaltax + shipping    
        
    except ObjectDoesNotExist:
        pass
    userprofile = UserProfile.objects.filter(user = request.user).first() #userprofile.

    address = AddAddress.objects.filter(user = request.user)    #user address.
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

#makepayment function.
@login_required(login_url='userlog')
def makepayment(request,total=0,quantity=0,cart_items=0):

    totaltax = 0
    try:
        if request.user.is_authenticated:
           cart_items = CartItem.objects.filter(user = request.user,is_active=True)#getting all cartiems of the user.
        else:
            cart = Cart.objects.get(cartid = _cart_id_(request))   #if guest user,getting session id
            cart_items = CartItem.objects.filter(cart=cart, is_active = True)#getting all cartitems using session id of guest user.

        for cart_item in cart_items:
            total += checkoffer(cart_item) * cart_item.quantity #products total price
            quantity += cart_item.quantity #quantity of cart items

            totaltax = int(totaltax+( (checkoffer(cart_item) * cart_item.quantity) / 1200)) #tax
        # try:    
        #     if total > 75000:
        #         coupon = Coupon.objects.all().first
        #     else:
        #         coupon = None    
        # except:
        #     pass           
        shipping = 100 
        total = couponprice(request, total)  #calculating total,if there is any coupon used by the user.
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
        addid = request.POST.get('addid') #getting selected address.

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

#add new address in checkout page.
@login_required(login_url='userlog')
def checkout_addaddress(request):

    if request.method == 'POST':
        #getting all the details.
        user = request.user
        name = request.POST.get('name')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phone')
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
    return redirect(checkout_view)  


#function to placeorder.
@login_required(login_url='userlog')
def placeorder_view(request,total=0,quantity=0,order=0):

    #getting all the cartitems of the user
    cart_items = CartItem.objects.filter(user = request.user)
    totaltax = 0
    
    for cart_item in cart_items:
        total += checkoffer(cart_item)* cart_item.quantity #products total price
        quantity += cart_item.quantity #quantity of cart items
        totaltax = int(totaltax+( (checkoffer(cart_item) * cart_item.quantity) / 1200)) #tax
    
    shipping = 100 #shipping
    total = couponprice(request,total) #calculating total,if there is any coupon used by the user.
    grandtotal = totaltax +total +shipping  #grandtotal

    #if coupon user, we want to add the coupon into used coupon,bcos no one wants to use that coupon again.
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
    #if coupon used, then we want to delete the coupon from session.
    if 'coupon' in request.session:
        del request.session['coupon']   

    if request.method == 'POST':
        # if not AddAddress.objects.filter(user =request.user):  # if the logged in user have no address then it will create one.
            
        #             user = request.user
        #             name = request.POST.get('name')
        #             email = request.POST.get('email')
        #             phonenumber = request.POST.get('phone')
        #             city = request.POST.get('city')
        #             pincode = request.POST.get('pincode')
        #             state = request.POST.get('state')
        #             country = request.POST.get('country')
        #             newaddress = request.POST.get('address')

        #             addadress = AddAddress.objects.create(

        #                     user = user, name = name, email = email, newaddress = newaddress, city = city,
        #                     phonenumber = phonenumber, pincode = pincode, state = state, country = country

        #             )

        #             addadress.save()
        # if not UserProfile.objects.filter(user = request.user):
        #     userp = UserProfile()
        #     userp.user = request.user
        #     userp.save()

        #taking all the details 
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
       
        #creating the order with the details.
        neworder = Order.objects.create(

            user = user, customername = customername, phone=phone, email=email, address=address,
            pincode = pincode, city = city, state = state, country = country, tax = totaltax, 
            paymentmode = paymentmode, shippping = shipping, grandtotal = grandtotal, 
            total_price = total, payment_id=payment_id
        )
        neworder.save()  

        orderitem = CartItem.objects.filter(user=request.user)
        for item in orderitem:
            # creating order products for each product in the order.
            order =OrderProduct(
                    order = neworder,
                    price = checkoffer(item),
                    product = item.product,
                    quantity = item.quantity,
            )
            order.save()

            #to decrease the stock of the product after an item is ordered.
            orderproduct = Product.objects.filter(id=item.product.id).first()
            orderproduct.stock = orderproduct.stock - item.quantity
            orderproduct.save()
             
        #delete cartitems from the cart after item is ordered.
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
        

#razorpay function.
def razorpay_view(request,total=0,quantity=0):    

    #taking cartiems
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
    
#invoice after an item is ordered.
def invoice_view(request,actual_price=0,discounted_price=0,coupon=0):

    try: 
        orders = Order.objects.last()   #taking the last order.
        order = OrderProduct.objects.filter(order = orders) #taking all the products in the last order.
        
        for o in order:
            actual_price += o.product.price * o.quantity   #total price of all the ordered products without offer and coupon to calculate for the discount.
            if o.product.discount_price:    #if any product has discount price.
                discounted_price += o.product.discount_price * o.quantity #calculating the order products price with discount.
            else:
                discounted_price += o.product.price * o.quantity   #if ordered prodcuts does not have discount price
        #actual_price=total price of all ordered products
        #b=total price of all ordered products included with discount.      
        discount = actual_price-discounted_price  
        print('discount',discount)
        #calculating coupon price ,if coupon applied in this order products.
        coupon = discounted_price - int(orders.total_price)

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
            #collecting all the orders 
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

#information of particular order,
def orderinfo_view(request, id,actual_price=0,discounted_price=0):         
    
    try:
        orders = Order.objects.get(id = id)
        orderproduct = OrderProduct.objects.filter(order = orders)

        for o in orderproduct:
            actual_price += o.product.price * o.quantity   #total price of all the ordered products without offer and coupon to calculate for the discount.
            if o.product.discount_price:    #if any product has discount price.
                discounted_price += o.product.discount_price  * o.quantity #calculating the order products price with discount.
            else:
                discounted_price = discounted_price + o.product.price * o.quantity   #if ordered prodcuts does not have discount price  
                print(discounted_price)
        print(discounted_price)
        #actual_price=total price of all ordered products
        #b=total price of all ordered products included with discount. 
        discount = actual_price-discounted_price
        print(discount,'ddddd')
        coupon = discounted_price  - int(orders.total_price) 
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

#Cancel order
def remove_order_view(request,id):

    orders = Order.objects.get(id = id)
    orders.status ="Cancelled"  #changing status of order to 'Cancelled'.
    orders.save()

    #increase the stock of the cancelled product
    orderproduct = OrderProduct.objects.filter(order = orders)
    for order in orderproduct:
        product = Product.objects.get(id = order.product.id)
        product.stock = product.stock + order.quantity
        product.save()
    return redirect(myorder_view)


#return delivered order.
def return_order(request,id):

    orders = Order.objects.get(id = id)
    orders.status ="Returned"  #changing status of order to 'Returned'.
    orders.save()

    # To increase the stock of the returned product
    orderproduct = OrderProduct.objects.filter(order = orders)
    for order in orderproduct:
        product = Product.objects.get(id = order.product.id)
        product.stock = product.stock + order.quantity
        product.save()
    return redirect(myorder_view)


#applying coupon 
def apply_coupon(request):
    if request.method =="POST":
        coupon =request.POST['coupon'] 
        print('sdafsa',coupon)
        try:
            if Coupon.objects.get(coupon_code = coupon):    #if coupon exists.
                coupon_exists = Coupon.objects.get(coupon_code = coupon)    #getting the coupon.

                try:
                    if UsedCoupon.objects.get(user = request.user, coupon = coupon_exists): #if coupon is used.
                        messages.error(request,'Coupon already used')
                        return redirect(checkout_view)
                        
                except:     #if coupon is not used.
                    request.session['coupon'] = coupon  #adding into session.
                    print('aaaaaaaaa',coupon)
                    return redirect(checkout_view)
            else:   #if coupon does not exist.
                messages.error(request,'Coupon does not exists')          
                return redirect(checkout_view)   

        except:
            messages.error(request,'coupon does not exist')  
            return redirect(checkout_view)         

    return redirect(checkout_view)    

    




