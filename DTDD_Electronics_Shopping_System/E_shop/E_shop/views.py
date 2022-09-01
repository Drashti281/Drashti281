from cart.cart import Cart
from django.shortcuts import render,redirect,HttpResponse
from store_app.models import Product,Categories,Filter_Price,Color,Brand,Tag,Contact_us,Order,OrderItem
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


import razorpay

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRECT))



def BASE(request):
    return render(request,'Main/base.html')


def HOME(request):
    product = Product.objects.filter(status = 'Publish')

    context = {
        'product':product,
    }

    return render(request, 'Main/index.html',context)


def PRODUCT(request):

    categories = Categories.objects.all()
    filter_price = Filter_Price.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()


    CATID = request.GET.get('categories')
    PRICE_FILTER_ID = request.GET.get('filter_price')
    COLORID = request.GET.get('color')
    BRANDID = request.GET.get('brand')

    ATOZID = request.GET.get('ATOZ')
    ZTOAID = request.GET.get('ZTOA')

    PRICE_LOWTOHIGH = request.GET.get('PRICE_LOWTOHIGH')
    PRICE_HIGHTOLOW = request.GET.get('PRICE_HIGHTOLOW')

    NEW_PRODUCTID = request.GET.get('NEW_PRODUCT')
    OLD_PRODUCTID = request.GET.get('OLD_PRODUCT')


    print(PRICE_FILTER_ID)
    if CATID:
        product = Product.objects.filter(categories = CATID,status = 'Publish')
    elif PRICE_FILTER_ID:
        product = Product.objects.filter(filter_price = PRICE_FILTER_ID,status = 'Publish')
    elif COLORID:
        product = Product.objects.filter(color = COLORID,status = 'Publish')
    elif BRANDID:
        product = Product.objects.filter(brand = BRANDID,status = 'Publish')
    elif ATOZID:
        product = Product.objects.filter(status = 'Publish').order_by('name')
    elif ZTOAID:
        product = Product.objects.filter(status = 'Publish').order_by('-name')
    elif PRICE_LOWTOHIGH:
        product = Product.objects.filter(status = 'Publish').order_by('price')
    elif PRICE_HIGHTOLOW:
        product = Product.objects.filter(status = 'Publish').order_by('price')
    elif NEW_PRODUCTID:
        product = Product.objects.filter(status = 'Publish',condition = 'New').order_by('-id')
    elif OLD_PRODUCTID:
        product = Product.objects.filter(status = 'Publish',condition = 'Old').order_by('-id')
    else:
        product = Product.objects.filter(status='Publish').order_by('-id')



    context = {
        'product': product,
        'categories':categories,
        'filter_price':filter_price,
        'color':color,
        'brand':brand,

    }
    return render(request,'Main/product.html',context)


def SEARCH(request):
    query = request.GET.get('query')
    product = Product.objects.filter(name__icontains = query)

    context = {
        'product':product
    }
    return render(request,'Main/search.html',context)


def PRODUCT_DETAIL_PAGE(request,id):
    prod = Product.objects.filter(id = id).first()

    context ={
        'prod':prod
    }
    return render(request,'Main/product_single.html',context)


def Contact_Page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact_us(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )

        subject = subject
        message = message
        email_from = settings.EMAIL_HOST_USER
        try:
            send_mail(subject,message,email_from, ['tandeldrashti28@gmail.com'])
            contact.save()
            return  redirect('home')
        except:
            return redirect('contact')

    return render(request,'Main/contact.html')


def HandleRegister(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        customer = User.objects.create_user(username,email,pass1)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.save()
        return redirect('home')


    return render(request,'Registartion/auth.html')


def HandleLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username,password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return redirect('login')

    return render(request, 'Registartion/auth.html')


def HandleLogout(request):
     logout(request)


     return redirect('home')



@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    return render(request, 'Cart/cart_details.html')


def Check_out(request):
    amount_str = request.POST.get('amount')
    amount_float = float(amount_str)
    amount = int(amount_float)


    payment =  client.order.create({
      "amount": amount,
      "currency":"INR",
      "payment_capture":"1"
      })

    order_id = payment['id']
    context = {
        'order_id':order_id,
         'payment':payment,
    }
    return render(request,'Cart/checkout.html',context)


def PLACE_ORDER(request):
    if request.method == "POST":
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id=uid)
        cart = request.session.get('cart')
        print(cart)

        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        amount = request.POST.get('amount')


        order_id = request.POST.get('order_id')
        payment = request.POST.get('payment')

        context = {
            'order_id':order_id,
        }
        order = Order(
            user = user,
            firstname = firstname,
            lastname=lastname,
            country = country,
            address = address,
            city = city,
            state = state,
            postcode = postcode,
            phone = phone,
            email = email,
            payment_id = order_id,
            amount = amount,
        )
        order.save()
        for i in cart:
            a = (int(cart[i]['price']))
            b = cart[i]['quantity']
            total = a * b


            item = OrderItem(
                user = user,
                order = order,
                product = cart[i]['name'],
                image = cart[i]['image'],
                quantity = cart[i]['quantity'],
                price = cart[i]['price'],
                total = total
           )

            item.save()



        return render(request,'Cart/placeorder.html',context)

@csrf_exempt
def SUCCESS(request):
      if request.method == "POST":
          a = request.POST
          order_id =""
          for key, val in a.items():
             if key == 'razorpay_order_id':
               order_id = val
               break
          user = Order.objects.filter(payment_id =order_id).first()
          user.paid = True
          user.save()
      return render(request,'Cart/thank-you.html')


def Your_Order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)

    order = OrderItem.objects.filter(user = user)
    context={
        'order':order,
    }

    return render(request,'Main/your_order.html',context)


def ABOUT(request):
    return render(request,'Main/about.html')


def Blog_Grid(request):
    return render(request,'Main/blog-grid.html')


def Blog_List(request):
    return render(request,'Main/blog-list.html')


def Blog_Grid_Left_Sidebar(request):
    return render(request,'Main/blog-grid-left-sidebar.html')


def Blog_Grid_Right_Sidebar(request):
   return render(request,'Main/blog-grid-right-sidebar.html')


def Blog_List_Left_Sidebar(request):
    return render(request,'Main/blog-list-left-sidebar.html')


def Blog_List_Right_Sidebar(request):
    return render(request,'Main/blog-list-right-sidebar.html')


def Single_Blog(request):
    return render(request,'Main/single-blog.html')


def Single_Blog_Left_Sidebar(request):
    return render(request,'Main/single-blog-left-sidebar.html')


def Single_Blog_Right_Sidebar(request):
    return render(request,'Main/single-blog-right-sidebar.html')


def Shop_3_Column(request):
    return render(request,'Shop/shop-3-column.html')


def Shop_4_Column(request):
    return render(request,'Shop/shop-4-column.html')


def Shop_Left_Sidebar(request):
    return render(request,'Shop/shop-left-sidebar.html')


def Shop_Right_Sidebar(request):
    return render(request,'Shop/shop-right-sidebar.html')


def Shop_List_Left_Sidebar(request):
    return render(request,'Shop/shop-list-left-sidebar.html')


def Shop_List_Right_Sidebar(request):
    return render(request,'Shop/shop-list-right-sidebar.html')


def Product_Group(request):
    return render(request,'Product/product-group.html')


def Product_Tab_2(request):
    return render(request,'Product/product-tab-2.html')


def Product_Tab_3(request):
    return render(request,'Product/product-tab-3.html')


def Product_Slider(request):
    return render(request,'Product/product-slider.html')


def Product_Account(request):
    return render(request,'Product/product-account.html')

def Empty_Product(request):
    return render(request,'Product/empty-product.html')



def Coming_Soon_Page(request):
    return render(request,'Page/coming-soon-page.html')


def Home_1(request):
    return render(request,'Page/home-1.html')


def Whishlist(request):
    return render(request,'Product/whishlist.html')



