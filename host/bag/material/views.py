from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import razorpay
from django.utils.crypto import get_random_string # type: ignore
from django.core.mail import send_mail # type: ignore
# Create your views here.
def show(req):
    print("hii")
    return HttpResponse("hii")
def index(req):
    return render(req,"index.html")
def jewellery(req):
    return render(req,"log.html")
def fashion(req):
    return render(req,"fashion.html")
def electronic(req):
    return render(req,"electronic.html")
def about(req):
    return render(req,'about.html')
def reg(req):
    if req.method=='POST':
        a=req.POST['n1']
        b=req.POST['n2']
        c=int(req.POST['n3'])
        d=req.POST['n4']
        e=req.POST['n5']
        if register.objects.filter(email=b).exists():
            return HttpResponse("email.exists")
        elif register.objects.filter(number=c).exists():
            return HttpResponse("phone_number.exists")
        else:
            if d==e:
                register.objects.create(name=a,email=b,number=c,password=d).save()
            else:
                return HttpResponse("password not same!")
        return render(req, 'register.html',)
    return render(req, 'register.html')
def log(req):
    if req.method=='POST':
        b=req.POST['n2']
        c=req.POST['n4']
        try:
            data=register.objects.get(email=b)
            if data.password==c:
                req.session['user']=b
                messages.success(req,'login successfully')
                return redirect(user_prooduct)
            else:
                messages.error(req, 'incorrect pass')
                return redirect(log)
        except:
            if b=='admin@gmail.com' and c=='1234':
                req.session['admin']=b
                return redirect(admin)
            else:
                messages.error(req,'email incorrect')
                return redirect(log)
    return render(req,'login.html')
def update(request,v):
    data=register.objects.get(pk=v)
    if request.method=='POST':
        b=request.POST['n2']
        d=request.POST['n4']
        register.objects.filter(pk=v).update(email=b,password=d)
        return redirect(register)
    return render(request,'update.html',{'data':data})
def admin(req):
    return render(req,"admin.html")

def log_out(request):
    if 'user'in request.session or 'admin'in request.session:
        request.session.flush()
        return redirect(index)
    return redirect(index)
def add_product(request):
    if request.method=='POST':
        a=request.POST['n1']
        b=int(request.POST['n2'])
        c= request.POST['n3']
        d=request.FILES['n4']
        product_table.objects.create(name=a, price=b, quantity=c, image=d).save()
        return render(request, 'add_product.html', {'data': a, 'b': b, 'c': c, 'd': d,})
    return render(request,'add_product.html')

def manage_product(request):
    data = product_table.objects.all()
    return render(request, 'manage_product.html', {'data': data})

def dele(request,c):
    data=product_table.objects.get(pk=c)
    data.delete()
    return redirect(manage_product)
from .forms import *
def update1(request,x):
    data=product_table.objects.get(pk=x)
    data1=update_form(instance=data)
    if request.method=='POST':
        d=update_form(request.POST,request.FILES,instance=data)
        if d.is_valid():
            d.save()
            return redirect(manage_product)
        return redirect(manage_product)
    return render(request,'update.html',{'data':data1})

def user_prooduct(req):
    return render(req,'userpage.html')

def user_login(req):
    data = product_table.objects.all
    return render(req, 'userhome.html', {'data': data})



def addcart(request,d):
    if'user'in request.session:
        user=register.objects.get(email=request.session['user'])
        data=product_table.objects.get(pk=d)
        if cart.objects.filter(product_details=data, user_details=user).exists():
            messages.error(request,'already esists')
            return redirect(user_login)
        else:
            cart.objects.create(user_details=user,product_details=data,totalprice=data.price).save()
            return redirect(user_login)
    else:
        return render(log_out)



def cartview(request):
    user=register.objects.get(email=request.session['user'])
    data=cart.objects.filter(user_details=user)
    total=0
    quantity=0
    for i in data:
        total += i.totalprice
        quantity += 1

    return render(request,'cartview.html',{'data':data,'total':total,'quantity':quantity})



def increment(req,d):
    if 'user' in req.session:
        data= cart.objects.get(pk=d)
        data.quantityes+=1
        data.totalprice=data.quantityes*data.product_details.price
        data.save()
        return redirect(cartview)
    else:
        return render(log)

def decrement(req,d):
    if 'user' in req.session:
        data= cart.objects.get(pk=d)
        if data.quantityes<=1:
            data.delete()
            return redirect(cartview)
        else:
            data.quantityes-=1
            data.totalprice = data.quantityes * data.product_details.price
            data.save()
            return redirect(cartview)
    else:
        return render(log)

def rem(request,d):
    data=cart.objects.get(pk=d)
    data.delete()
    return redirect(cartview)
def addwish(req,d):
    if 'user' in req.session:
        user= register.objects.get(email=req.session['user'])
        data= product_table.objects.get(pk=d)
        if wishlist.objects.filter(product_details=data,user_details=user).exists():
            messages.error(req,'already esists')
            return redirect(user_login)
        else:
            wishlist.objects.create(user_details=user,product_details=data).save()
            return redirect(user_login)
    else:
        return render(log_out)
def wishview(req):
    if 'user' in req.session:
        user = register.objects.get(email=req.session['user'])
        data = wishlist .objects.filter(user_details=user)
        return render(req, 'log.html', {'data': data})
    else:
        return render(log_out)
def reme(request,d):
    data=wishlist.objects.get(pk=d)
    data.delete()
    return redirect(wishview)

def payment(request, id):
    amount = id*100
    order_currency = 'INR'
    client = razorpay.Client(
        auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    return render(request, "pay.html",{'amount':amount,'id':id})

def order(request):
    user = register.objects.get(email=request.session['user'])
    data = cart.objects.filter(user_details=user)
    import datetime
    d = datetime.datetime.now()
    for i in data:
        a = product_table.objects.filter(name=i.product_details.name).first()
        a.quantity = int(a.quantity) - int(i.quantityes)
        print(a.quantity)
        a.save()
        orders.objects.create(user_details=user,product_details=a,quantity=i.quantityes,amount=i.totalprice,order_date=d).save()
    data.delete()
    return render(request,"success.html")
def myorder(request):
    user = register.objects.get(email=request.session['user'])
    data = orders.objects.filter(user_details=user)
    return render(request,'myorder.html',{'data':data})
def adorder(req):
    data = orders.objects.all()
    return render(req, 'adminorder.html', {'data': data})
def alert(request):
    low_stock_products = product_table.objects.filter(quantity__lt=5)
    return render(request, "alerts.html", {'low_stock_products':low_stock_products})
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = register.objects.get(email=email)
        except Exception as e:
            print (e)# noqa: E722
            messages.info(request, "Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user_details=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:9898/reset_password/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}',
                      'settings.EMAIL_HOST_USER', [email], fail_silently=False)
            # return render(request, 'emailsent.html')

        except Exception as e:
            print(e)# noqa: E722
            messages.info(request, "Network connection failed")
            return redirect(forgot_password)

    return render(request,'forgot.html')

def reset_password(request,token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    # usr = User.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user_details.password=new_password
            password_reset.user_details.save()
            # password_reset.delete()
            return redirect(log)
    return render(request, 'reset_password.html', {'token': token})

def booking_details(request):
    data = orders.objects.all()
    return render(request,'hhh.html',{'data':data})

def display_details(request):
    data=register.objects.all()
    return render(request,'display_details.html',{'data':data})
def update_status(request, pk):
    if request.method == 'POST':
        if orders.objects.filter(pk=pk).exists():
            order = orders.objects.get(pk=pk)
            new_status = request.POST.get('n1')
            if new_status:
                order.product_status = new_status
                order.save()
                return redirect(booking_details)
    return redirect(booking_details)