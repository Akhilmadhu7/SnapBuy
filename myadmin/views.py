
import re
from django.shortcuts import render,redirect

from userhome.models import Customuser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.cache import cache_control
from newcart.models import Cart, CartItem, Order, OrderProduct,Coupon,UsedCoupon
from category_adminside.models import Product,ProductOffer,CategoryOffer,Category
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,Count
from django.utils import timezone
import datetime 
import pytz


tz_india = pytz.timezone("Asia/Kolkata")


#admin log function.
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def adminlog_view(request):
    #if user is admin,redirect to admin home page.
    if request.user.is_superuser:
        return redirect(adminhome_view)    

    if request.method == 'POST':

        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        user = authenticate(phone_number=phone_number, password = password)
        #if the user is admin,then save no: to session and redirect to admin home.
        if user is not None and user.is_superuser:
            request.session['phone_number']= phone_number
            login(request,user)
            return redirect(adminhome_view)
        else:
            #if the entered data is not admin, then show error message.
            messages.error(request,'Invalid Details')   
            return redirect(adminlog_view) 

    return render(request,'adminside/adminlogin.html')



#admin home page view.
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def adminhome_view(request):

    if request.user.is_superuser :
        
        orders = Order.objects.all()
        try:
            #total amount users paid through cod.
            codtotal = Order.objects.filter(paymentmode = 'COD').aggregate(Sum('grandtotal')).get('grandtotal__sum')
            #totoal count of users paid through cod
            cod = Order.objects.filter(paymentmode = 'COD').aggregate(Count('id')).get('id__count')
            #total amount users paid through razorpay.
            raztotal = Order.objects.filter(paymentmode = 'paid by razorpay').aggregate(Sum('grandtotal')).get('grandtotal__sum')
            #totoal count of users paid through razorpay
            raz = Order.objects.filter(paymentmode = 'paid by razorpay').aggregate(Count('id')).get('id__count')
            #total amount users paid through paypal.
            paytotal = Order.objects.filter(paymentmode = 'paid by paypal').aggregate(Sum('grandtotal')).get('grandtotal__sum')
            #totoal count of users paid through paypal
            pay = Order.objects.filter(paymentmode = 'paid by paypal').aggregate(Count('id')).get('id__count')
        except:
            pass   

        try:
            lapsale = OrderProduct.objects.filter(product__category_name = 1).aggregate(Sum('price')).get('price__sum') #totla amount earned after sold laptop
            mobsale = OrderProduct.objects.filter(product__category_name = 2).aggregate(Sum('price')).get('price__sum') #totla amount earned after sold mobile
            ipadsale = OrderProduct.objects.filter(product__category_name = 3).aggregate(Sum('price')).get('price__sum') #totla amount earned after sold ipad

            lap = OrderProduct.objects.filter(product__category_name = 1).count() #total count of laptop sold
            mob = OrderProduct.objects.filter(product__category_name = 2).count() #total count of mobile sold
            pad = OrderProduct.objects.filter(product__category_name = 3).count() #total count of ipad sold
        except:
            pass 
        #grandtotal of all products
        ordertotal = Order.objects.all().aggregate(Sum('grandtotal')).get('grandtotal__sum')
        context = {
            'orders':orders,
            'codtotal':int(codtotal),
            'paytotal':paytotal,
            'raztotal':raztotal,
            'total':int(ordertotal),
            'pay':pay,
            'raz':raz,
            'cod':cod,
            'lap':lap,
            'mob':mob,
            'pad':pad,
            'lapsale':lapsale,
            'mobsale':mobsale,
            'ipadsale':ipadsale
        }
        return render(request,'adminside/adminhome.html',context) 
    return redirect(adminlog_view)
    
       
#admin logout 
def adminlogout_view(request):

    if request.user.is_superuser:
        request.session.flush()
        logout(request)
    return redirect(adminlog_view)   
    
#list all customers, excluding admin
login_required(login_url='adminlog')
def admincustomers_view(request):
    if request.user.is_superuser:
        user_phone = Customuser.objects.get(username = request.user)
        customers = Customuser.objects.exclude(phone_number=user_phone.phone_number)
    else:
        return redirect(adminlog_view)    

    return render(request,'adminside/ad_customers.html',{'userlist':customers})     


#block and unblocl customers.
def blockuser(request,id):

    try:
        user = Customuser.objects.get(id=id)    #getting the user 
    except: #if no user with the above id, thens show error message.
        messages.error(request,'No user')    
        return redirect(admincustomers_view)
    #if user is active, then change to false(means the user has been blocked)
    if user.is_active:
        user.is_active = False
        messages.warning(request,'Account is BLOCKED')
        user.save()
        return redirect(admincustomers_view)
    #if user is not active, then change to true    
    else:
        user.is_active = True 
        messages.success(request,'Account is unblocked') 
    user.save()
    
    return redirect(admincustomers_view)      


#list category offers
login_required(login_url='adminlog')
def category_offer(request):

    cat_offer = CategoryOffer.objects.all()
    context = {
        'c_offer':cat_offer
    }
    return render(request,'cat_adminside/categoryoffer.html',context)

#add category offer
login_required(login_url='adminlog')
def add_catoffer(request):          

    category = Category.objects.all()
    c = datetime.datetime.now(tz_india).strftime("%d/%m/%Y, %H:%M")   #GETTING CURRENT TIME
    print(' current date ===================   ',c)

    if request.method == 'POST':

        categorys = request.POST.get('category') #category name 
        offer = request.POST.get('offer') #offer value(in between 1 & 100)

        valid_f = request.POST.get('from') #offer valid from date
        valid_t = request.POST.get('to') #offer ending date

        # validf = valid_f.strftime("%d/%m/%Y, %H:%M")
        # validt = valid_t.strftime("%d/%m/%Y, %H:%M")

        print('validf  ========',valid_f,'     validto =====   ',valid_t,'     offer========  ',offer)

        cat = Category.objects.get(id=categorys)
        try:
            if CategoryOffer.objects.get(category = cat): #if the category offer already exists, then show error message
                messages.error(request,'Offer already exists')
                return redirect(add_catoffer)
        except:
            pass
        
        #offer values must be in between 1 and 100, if it's not satisfy condition, then show error message.
        if int(offer) > 100 or int(offer) < 0: 
            messages.error(request,'Offer should between 1 and 100')
            return redirect(add_catoffer)

        # if valid_f > c:
        #     messages.error(request,'Date should be current date or above')
        #     return redirect(add_catoffer)

        #if starting date is greater than ending date , then show error message
        if valid_f > valid_t:
            messages.error(request,'From date should be less than To date')
            return redirect(add_catoffer)   
        #if all validations are ok, then create offer.
        else:
            catoffer = CategoryOffer(
                        category = cat, offer = offer, valid_from = valid_f, 
                        valid_to = valid_t
            )    
            catoffer.save()
            messages.success(request,'Category offer added succesfully')
            return redirect(category_offer)
    context = {
        'category':category,
    }
    return render(request,'cat_adminside/addoffer.html',context)

#edit category offer
login_required(login_url='adminlog')
def edit_catoffer(request,id):              

    try:
         catoffer = CategoryOffer.objects.get(id = id)  #getting the category ,which is to be edited.
    except:
        pass
    category = Category.objects.all()

    a = catoffer.valid_from.strftime("%d/%m/%Y, %H:%M") 
    
    if request.method == 'POST':
        try:
            categorys = request.POST.get('category')
            catoffer.offer = request.POST.get('offer')
            catoffer.valid_from = request.POST.get('from')
            catoffer.valid_to = request.POST.get('to')

            # valid_f = request.POST.get('from')
            # valid_t = request.POST.get('to')
            
            # catoffer.valid_from = valid_f.strftime("%d/%m/%Y, %H:%M")
            # catoffer.valid_to = valid_t.strftime("%d/%m/%Y, %H:%M")

            catoffer.category = Category.objects.get(id=categorys)
            print('catoffer.category',catoffer.category)
            if int(catoffer.offer) > 100 or int(catoffer.offer) < 0:
                messages.error(request,'Offer should between 1 and 100')
                return redirect(edit_catoffer,id)

            if catoffer.valid_from > catoffer.valid_to:
                messages.error(request,'From date should be less than To date')
                return redirect(edit_catoffer,id)    
            
            # if catoffer.valid_from  <= a:
            #     print('valid from and previous date',catoffer.valid_from,'to',a)
            #     messages.error(request,'From date should not be less than previous date')
            #     return redirect(edit_catoffer,id)

            else:
                catoffer.save()
                messages.success(request,'Category offer edited succesfully')
                return redirect(category_offer)    

        except:
            messages.error(request,'Add valid from date')
            return redirect(edit_catoffer,id)
    context = {
        'category':category,
        'catoffer':catoffer,
    }    

    return render(request,'cat_adminside/addoffer.html',context)


#delete category offer
def delete_cat_offer(request,id):   

    cat_offer = CategoryOffer.objects.get(id = id)
    cat_offer.delete()
    messages.success(request,'Category offer deleted succesfully')

    return redirect(category_offer)

#list products offer
login_required(login_url='adminlog')
def product_offer(request):         

    p_offer = ProductOffer.objects.all()
    context = {
        'p_offer':p_offer
    }
    return render(request,'cat_adminside/productoffer.html',context)

#add product offer (fucntion same as add category offer)
login_required(login_url='adminlog')
def add_prodoffer(request):             

    product = Product.objects.all()

    c = datetime.datetime.now(tz_india).strftime("%d/%m/%Y, %H:%M:%S")   #GETTING CURRENT TIME
    print(' current date ===================   ',c)

    if request.method == 'POST':

        products = request.POST.get('product')
        offer = request.POST.get('offer')

        valid_f = request.POST.get('from')
        valid_t = request.POST.get('to')
        

        print('validf  ========',valid_f,'     validto =====   ',valid_t,'     offer========  ',offer)

        prod = Product.objects.get(id = products)
        try:
            if ProductOffer.objects.get(product = prod):
                messages.error(request,'Offer already exists')
                return redirect(add_prodoffer)
        except:
            pass

        if int(offer) > 100 or int(offer) < 0:
            messages.error(request,'Offer should between 1 and 100')
            return redirect(add_prodoffer)
        print(type(c),'qqqqqqqqqqqqq',type(valid_f))
        # if valid_f > c:
        #     print(valid_f,'========',c)
        #     messages.error(request,'Date should be current date or above')
        #     return redirect(add_prodoffer)

        if valid_f > valid_t:
            messages.error(request,'From date should be less than To date')
            return redirect(add_prodoffer)   
        else:
            prod_offer = ProductOffer(
                        product = prod, offer = offer, valid_from = valid_f, 
                        valid_to = valid_t
            )    
            prod_offer.save()
            messages.success(request,'Product offer added succesfully')
            return redirect(product_offer)
    context = {
        'product':product
    }

    return render(request,'cat_adminside/addprod_offer.html',context)


#edit product offer(same as edit category offer)
login_required(login_url='adminlog')
def edit_prodoffer(request,id):

    try:
        p_offer = ProductOffer.objects.get(id = id)
    except:
        pass
    product = Product.objects.all()
    a = p_offer.valid_from.strftime("%d/%m/%Y, %H:%M")   #to get the previous offer started date

    if request.method == 'POST':
        try:
            products = request.POST.get('product')
            p_offer.offer = request.POST.get('offer')

            p_offer.valid_from = request.POST.get('from')
            p_offer.valid_to = request.POST.get('to')
            
            p_offer.product = Product.objects.get(id=products)

            if int(p_offer.offer) > 100 or int(p_offer.offer) < 0:
                messages.error(request,'Offer should between 1 and 100')
                return redirect(edit_prodoffer,id)

            if p_offer.valid_from > p_offer.valid_to:
                messages.error(request,'From date should be less than To date')
                return redirect(edit_prodoffer,id)    

            # if p_offer.valid_from >= a:
            #     print(p_offer.valid_from,'============',a)
            #     messages.error(request,'From date should not be less than previous date')
            #     return redirect(edit_prodoffer,id)

            else:
                
                p_offer.save()

                messages.success(request,'Product offer edited succesfully')
                return redirect(product_offer) 
        except:
            messages.error(request,'Add valid from date')
            return redirect(edit_prodoffer,id)

    context = {
        'p_offer':p_offer,
        'product':product
    }
    return render(request,'cat_adminside/addprod_offer.html',context)

#delete product offer
def delete_prod_offer(request,id):            

    p_offer = ProductOffer.objects.get(id = id)
    p_offer.delete()
    return redirect(product_offer)
    
#list all coupon(not used)
login_required(login_url='adminlog')
def coupon_view(request):

    coupon = Coupon.objects.all()
    context = {
        'coupon':coupon
    }
    return render(request,'cat_adminside/coupon.html',context) 

#add coupon
login_required(login_url='adminlog')
def add_coupon(request):

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon') #coupon code
        discount = request.POST.get('discount') #coupon discount value (in % )
        try:
            #if discount value is in between 0 and 100, then create coupon.
            if int(discount) > 0 : 
                if int(discount) < 100:
                    coupon = Coupon(
                    coupon_code = coupon_code, discount_percentage = discount
                    )    
                    coupon.save() 
                    messages.success(request,'Coupon added succesfully')
                    return redirect(coupon_view)
        #if discount values is not in between 1 and 100, then show error message.            
        except:
            messages.error(request,'Discount percentage must be < 0  and > 100')
            return redirect(add_coupon)
    return render(request,'cat_adminside/couponadd.html')

#block coupon
def block_coupon(request,id):

    coupon = Coupon.objects.get(id=id)
    if coupon.is_active:
        coupon.is_active =False
        messages.warning(request,'Coupon blocked')
    else:
        coupon.is_active = True
        messages.success(request,'Coupon unblocked')    
    coupon.save()
    return redirect(coupon_view)

#delete coupon
def coupon_delete(request,id):

    coupon = Coupon.objects.get(id = id)
    coupon.delete()
    messages.success(request,'Coupon deleted succesfully')
    return redirect(coupon_view)

#list all used coupons
login_required(login_url='adminlog')
def used_coupon(request):

    usedcoupon = UsedCoupon.objects.all()
    context = {
        'usedcoupon':usedcoupon
    }
    return render(request,'cat_adminside/usedcoupon.html',context)


#delete used coupon
def delete_usedcoupon(request,id):

    usedcoupon = UsedCoupon.objects.get(id = id)
    usedcoupon.delete()
    messages.success(request,'Used coupon deleted succesfully')
    return redirect(used_coupon)

#list all orders
login_required(login_url='adminlog')
def order_admin_view(request):
    # cartitems = CartItem.objects.all()
    # customer = Customuser.objects.all()
    try:
        orders = Order.objects.all().order_by('-created_at')
    except:
        pass    
    orderitems = OrderProduct.objects.all()
    context={
        # 'cartitems': cartitems,
        'orders':orders,
        'orderitems':orderitems, 
    }
    return render(request,'cat_adminside/order.html',context)

#fucntion to particular order details.
login_required(login_url='adminlog')
def orderdetails_view(request, id):
    
    # productobj = Product.objects.get(id = id)
    try:
        orders = Order.objects.get(id = id) #getting the order
        orderitems = OrderProduct.objects.filter(order = orders) #getting all the products from the particular order.
    except:
        pass
    context = {
        'orders': orders,
        'orderitems': orderitems,  
    }
    return render(request,'cat_adminside/vieworder_details.html',context)    

#change order status of the order
def orderstatus_view(request, id):

    order = Order.objects.get(id = id)
    if request.method == 'POST':
        status  = request.POST.get('status') #getting the order status 
        order.status = status #changing the status.
        print(order.status)
        order.save()
    return redirect(order_admin_view)

#sales view
login_required(login_url='adminlog')
def sales_view(request):

    try:
        usercount = Order.objects.all().aggregate(Count('user')).get('user__count') #total users count
        ordertotal = Order.objects.all().aggregate(Sum('grandtotal')).get('grandtotal__sum') #total amount 
        totalorder = Order.objects.filter(status = 'Delivered').aggregate(Count('id')).get('id__count') #total count of delivered orders.

        prod_sold = OrderProduct.objects.all().aggregate(Count('quantity')).get('quantity__count') #total products sold count.
        sales_report = OrderProduct.objects.exclude(order__status='Cancelled') #total ordered products excluding cancelled products.
    except:
        pass    
    
    context = {
        'usercount':usercount,
        'ordertotal':ordertotal,
        'totalorder':totalorder,
        'prod_sold':prod_sold,
        'sales_report':sales_report
    }
    return render(request,'adminside/salesreport.html',context)
    
#search sales in between start and end date.
def date_range_view(request):

    if request.method == 'POST':
        from_date = request.POST.get('fromdate') #from date
        to_date = request.POST.get('todate') #end date

        #checking if date is valid or not.
        if len(from_date)>0 and len(to_date)>0:
            f_date = from_date.split("-")
            t_date = to_date.split("-")

            td = [int(x) for x in t_date]
            fd = [int(x) for x in f_date] 
            #getting the sales date with in the start and end date.  
            try:
                sales_report = OrderProduct.objects.exclude(order__status='Cancelled').filter(order__created_at__gte = datetime.date(fd[0],fd[1],fd[2]),
                                                        order__created_at__lte = datetime.date(td[0],td[1],td[2]))
            except:
                pass                                          
            context = {
                'sales_report':sales_report
            }
            return render(request,'adminside/salesreport.html',context)
        #if date is not valid, then show all sale report excluding status of order is 'cancelled'.
        else:
            try:
                 sales_report = OrderProduct.objects.exclude(order__status='Cancelled')
            except:
                pass

            context = {
                'sales_report':sales_report
            }
            return render(request,'adminside/salesreport.html',context)
    # return render(request,'adminside/salesreport.html',context)

#get sales report in a month
def monthly_sales_view(request,date):
    #funciton similar to above code(date_range_view)
    frmdate = date
    fm = [2022, frmdate, 1]
    todt = [2022,frmdate,28]

    sales_report = OrderProduct.objects.exclude(order__status='Cancelled').filter(order__created_at__gte = datetime.date(fm[0],fm[1],fm[2]),order__created_at__lte=datetime.date(todt[0],todt[1],todt[2])).order_by("-id")
    if len(sales_report)>0:
        print(sales_report)
        context = {
            'sales_report':sales_report,
        }
        return render(request,'adminside/salesreport.html',context)

    else:
        messages.error(request,"No Orders")
        return render(request,'adminside/salesreport.html')

    # return render(request,'adminside/salesreport.html')

#get sales report in a year
def yearly_report(request,date):
    #funciton similar to above code(date_range_view)
    frmdate = date
    fm = [frmdate, 1, 1]
    todt = [frmdate,12,31]

    try:
        sales_report = OrderProduct.objects.filter(order__created_at__gte = datetime.date(fm[0],fm[1],fm[2]),order__created_at__lte=datetime.date(todt[0],todt[1],todt[2])).order_by("-id")
    except:
        pass   

    if len(sales_report)>0:
        context = {
            'sales_report':sales_report,
        }
        return render(request,'adminside/salesreport.html',context)

    else:
        messages.error(request,"No Orders")
        return render(request,'adminside/salesreport.html')