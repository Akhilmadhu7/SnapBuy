

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.cache import cache_control
from twilio.rest import Client
from ebazaar import settings
import re


from newcart.models import AddAddress
from category_adminside.models import Category,Banner
from newcart.models import UserProfile,OrderProduct
from . models import Customuser
from category_adminside.models import Product,Category,ProductOffer

from newcart.models import Cart,CartItem
from newcart.views import _cart_id_
from products.models import Wishlist,WishlistItem
from products.views import _wishid_

# Create your views here.

@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def userlog_view(request):

    if request.method == 'POST':

        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        user = authenticate(phone_number=phone_number, password=password)

        active_user = Customuser.objects.get(phone_number=phone_number)

        if active_user.is_active==True:

            if user is not None:

                try:
                    cart = Cart.objects.get(cartid = _cart_id_(request))
                   
                    cart_items_eixsts = CartItem.objects.filter(cart = cart).exists()

                    if cart_items_eixsts:
                        
                        cart_items = CartItem.objects.filter(cart=cart)
                        user_carts = CartItem.objects.filter(user = user)
                        
                        
                        for cart_item in cart_items:
                          
                            item = 0
                            if user_carts:
                                for user_cart in user_carts:  #check each item in user item

                                    if cart_item.product == user_cart.product:  #check wheather the same product in user cart and session cart item product exists
                                        user_cart.quantity += cart_item.quantity  # then session cart item product save to user cart item product and increase the quantity of the product
                                        cart_item.delete()  # deleting the cart item created by the session
                                        user_cart.save()    # saving the product to the user cart 

                                        item = 1
                                        break
                                    if item == 0:
                                    
                                        cart_item.user = user # adding the cart item to the user cart
                                        cart_item.save()
                                        
                            else:
                                cart_item.user = user # if no carts in user , then it will add the cartitems to usercart.
                                cart_item.save()

                
                except:
                    pass  

                try: 
                    wishlist = Wishlist.objects.get(wishlistid = _wishid_(request)) 
                    wishitem = WishlistItem.objects.filter(wishlist = wishlist).exists()

                    if wishitem:

                        wishitem = WishlistItem.objects.filter(wishlist = wishlist)    #if wishlistitem exists of guest user
                        userwish = WishlistItem.objects.filter(user = user)             # if wishlistitem exists of user

                        for w_item in wishitem:

                            if userwish:  

                                for u_item in userwish:

                                    if w_item.product == u_item.product:    #checking wishlistitem product and userwishlist item product are same
                                       
                                        w_item.delete()     #then wishlistitem deletes  and saves the user wishlistitem product
                                        u_item.save()
                                        break
                                    else:
                                        w_item.user = user    # if the products are not same, then user will assign to the wishlist item and save the product
                                        w_item.save()
                            else:
                                w_item.user = user
                                w_item.save()         


                except:
                    pass 
            
                request.session['phone_number']=phone_number
                login(request,user)

                return redirect(index_view)
                # return redirect(otpverify)

            else:
                 messages.error(request,'Invalid Details')
                 return redirect(userlog_view)  

        else:
            messages.error(request,'Account is blocked')


    return render(request,'userside/userlogin.html')


def phonelogin(request):


    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        phone_no="+91" + phone_number

        if Customuser.objects.filter(phone_number=phone_number).exists():
            user = Customuser.objects.get(phone_number = phone_number)
            account_sid = settings.ACCOUNT_SID
            auth_token = settings.AUTH_TOKEN
            client = Client(account_sid, auth_token)
            verification = client.verify \
                .services(settings.SERVICES) \
                .verifications \
                .create(to=phone_no ,channel='sms')
            return render(request,'userside/otp.html',{'phone_number':phone_number})
            
            

        else:
            messages.info(request,'invalid Mobile number')
            return redirect(phonelogin)

    return render(request,'userside/phonelogin.html')


def otpverify(request,phone_number):

    print('aaaahdfvasvfvhjnsbdjhf ljsnd')
    if request.method == 'POST':
        if Customuser.objects.filter(phone_number=phone_number):
            user      = Customuser.objects.get(phone_number=phone_number)
            phone_no = "+91" + str(phone_number)

            otp_input   = request.POST.get('otp')
            print(otp_input)
            print('aaaahdfvasvfvhjnsbdjhf ljsnd')
            if len(otp_input)>0:
                account_sid = settings.ACCOUNT_SID
                auth_token = settings.AUTH_TOKEN
                client = Client(account_sid, auth_token)
            
                verification_check = client.verify \
                                    .services(settings.SERVICES) \
                                    .verification_checks \
                                    .create(to= phone_no, code= otp_input)

                if verification_check.status == "approved":
                    # auth.login(request,user)
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect(index_view)
                else:
                    messages.error(request,'Invalid OTP')
                    return render(request,'userside/otp.html',{'phone_number':phone_number})

                   
            else:
                messages.error(request,'Invalid OTP')
                return render(request,'userside/otp.html',{'phone_number':phone_number})

        else:

            messages.error(request,'Invalid Phone number')
            return redirect(otpverify)
    return render(request,'userside/otp.html')





# @cache_control(no_cache = True, must_revalidate = True, no_store = True)
def index_view(request):

    # if 'phone_number' in request.session:
    
    try:
            banner = Banner.objects.all()[:3]
            banners = Banner.objects.all()[:1]
            category = Category.objects.all()
            product_lap = Product.objects.filter(category_name = 1).order_by('-id')[:3]
            product_mob = Product.objects.filter(category_name = 2).order_by('-id')[:2]
            product_pad = Product.objects.filter(category_name = 3).order_by('-id')[:3]
            newproduct = Product.objects.filter(discount_price = 0).order_by('-id')[:8]
            bestsell = OrderProduct.objects.filter(product__gte =15).distinct()[1:16:2]
            offerproduct = Product.objects.exclude(discount_price = 0).order_by('discount_price')[:4]
           
                  
    except:
        pass
  

    context = {
        'banner':banner,
        'category':category,
        'product_lap':product_lap,
        'product_mob':product_mob,
        'product_pad':product_pad,
        'newproduct':newproduct,
        'bestsell':bestsell,
        'offerproduct':offerproduct,
        'banners':banners,
        
    }
    
    return render(request,'userside/index.html',context)
    # return redirect(userlog_view)        


def userlogout_view(request):

    if 'phone_number' in request.session:
        request.session.flush()
        logout(request)

    return redirect(userlog_view)

# def register_view(request):
#     return render(request,'userside/register.html')





 ############################## USEER REGISTRATION ###########################################
    



def userregister_view(request):

    if request.method == 'POST':

        phone_number =  request.POST.get('phone_number')

        email        =  request.POST.get('email')
        username     =  request.POST.get('username')
        password1    =  request.POST.get('password1')
        password2    =  request.POST.get('password2')


        username_pattern = "^[A-Za-z\s]{3,}$"       #USERNAME VERIFICATION
        username_verify = re.match(username_pattern,username)

        if username_verify is None:
            messages.error(request,'Name should contian only characters')
            return redirect(userregister_view)

        if Customuser.objects.filter(username=username):
            messages.error(request,'Username already exists') 
            return redirect(userregister_view)


        email_pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{2,3}$"     # EMAIL VERIFICATION 
        email_verify = re.match(email_pattern,email)


        if email_verify is None:
            messages.error(request,'Invalid Email')
            return redirect(userregister_view)

        if Customuser.objects.filter(email=email):
            messages.error(request,'Email already exists')
            return redirect(userregister_view)


        phone_pattern = '^\d{10}$'           # PHONE NUMBER VERIFICATION 
        phone_verify = re.match(phone_pattern, phone_number)  

        if phone_verify is None:
            messages.error(request,'Invalid phone number')
            return redirect(userregister_view)

        if Customuser.objects.filter(phone_number=phone_number):
            messages.error(request,'Phone number already exists') 
            return redirect(userregister_view)  


        if password1 == "" or len(password1)<4:         # PASSWORD VERIFICATION 
            messages.error(request,'Password should contains atleast 5 letters')
            return redirect(userregister_view)

        if password1 != password2:
            messages.error(request,'Password incorrect')
            return redirect(userregister_view)



        else:

            user = Customuser.objects.create_user(
                phone_number=phone_number, 
                email=email,
                username=username, 
                password=password1
                )

            user.save()

            userprofile = UserProfile.objects.create(
                user = user
            )
            userprofile.save()
            return redirect(userlog_view)

    return render(request,'userside/register.html')



def profile_view(request):

    # customuser = Customuser.objects.get(user = request.phone_number)

    profile = UserProfile.objects.get(user = request.user)
    addaddress = AddAddress.objects.filter(user= request.user)
    # customuser = Customuser.objects.get(username = request.user)  

    # print(addaddress)
    context = {
        'profile':profile,
        'addaddress':addaddress,
        # 'customuser':customuser,
    }
    return render(request, 'userside/profile.html',context)



def editprofile_view(request,id):

    user = Customuser.objects.get(id=id)
    
    profiles = UserProfile.objects.all()
    
    

    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')

        
        currentemail = user.email  #current email of the user
        curretnphone = user.phone_number  #current phone number of the user
        
        existemail = Customuser.objects.exclude(email = currentemail).filter(email = email)
        existphone = Customuser.objects.exclude(phone_number = curretnphone).filter(phone_number = phone_number)

        

        if existemail == email or existphone == phone_number:
            messages.error(request,'exist')
            return render(request, 'userside/editprofile.html')

        elif currentemail == email and curretnphone == phone_number:
            user.username = name
            messages.success(request,'Username changed succesfully')
            user.save()    
            return redirect(profile_view)
        else:
            user.username = name
            user.phone_number = phone_number
            user.email = email
            user.save() 
            messages.error(request,'Profile updated succesfully')
            return redirect(profile_view) 
        
       

    context = {
        'user':user,
        # 'profile':profile,
        'profiles':profiles
    }
    return render(request, 'userside/editprofile.html',context)    




def add_addressview(request):

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
            return redirect(add_addressview)


        email_pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"       #email verify pattern
        email_verify = re.match(email_pattern,email)


        if email_verify is None:
            messages.error(request,'Invalid Email')
            return redirect(add_addressview)


        addadress = AddAddress.objects.create(

                user = user, name = name, email = email, newaddress = newaddress, city = city,
                phonenumber = phonenumber, pincode = pincode, state = state, country = country

        )

        addadress.save()

        return redirect(profile_view)


    return render(request, 'userside/add_address.html')


def editpassword_view(request,id):

    user = Customuser.objects.get(id = id)
    if request.method == 'POST':
        
        oldpass = request.POST.get('oldpassword')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        user = Customuser.objects.get(id = id)
        phone = user.phone_number
        check = user.check_password(oldpass)
        
        
        if check == True:
            
            if password1 == "" or len(password1)<4:         # PASSWORD VERIFICATION 
                messages.error(request,'Password should contain atleast 5 letters')
                return render(request,'userside/editpassword.html')

            if password1 != password2:
                messages.error(request,'Password not equal')
                return render(request,'userside/editpassword.html')

            else:
                
                user.set_password(password1)
                user.save()
                usern = Customuser.objects.get(phone_number = phone)
                login(request,usern)
                messages.success(request,'password changed succesfully')
                return redirect(profile_view)    
        else:
            try:
                messages.error(request,'Incorrect password')
                return redirect(editpassword_view)
            except:
                pass    

    return render(request,'userside/editpassword.html')


def delete_address(request,id):
    address = AddAddress.objects.get(id = id)
    
    if request.user.is_authenticated:
        
        address.delete()
        messages.success(request,'Address deleted succesfully')
        return redirect(profile_view)    

    


   