from django.shortcuts import render,redirect
from django.http import HttpResponse
from firstapp.models import Product,CartItem
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request,'index.html',context={'products':products})

def view_cart(request):
    cart_items = CartItem.objects.filter(user = request.user)
    total_price = sum(item.product.price*item.quantity for item in cart_items)
    return render(request,'cart.html',{'cart_item':cart_items,'total_price':total_price})
    # return render(request,'cart.html')

def add_to_cart(request,product_id):
    product = Product.objects.get(id =  product_id)
    cart_item, created = CartItem.objects.get_or_create(product = product,user = request.user)
    cart_item.quantity+=1
    cart_item.save()
    # return redirect('viewcart')
    return redirect('productlist')

def remove_cart(request,item_id):
    cart_item = CartItem.objects.get(id =  item_id)
    if cart_item.quantity == 1:
        cart_item.delete()
    else:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('viewcart')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username = username).exists():
            messages.error(request,"Invalid Username")
            return redirect('/login/')
        user = authenticate(username = username,password = password)
        if user is None:
            messages.error("request","Invalid Password")
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('productlist')
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('/login/')


def register_view(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')  # Fixed typo: "passowrd"
        confirm_password = request.POST.get('confirm_password')

        # Check if password and confirm_password match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        # Check if username or email already exist
        if User.objects.filter(username=user_name).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Username or Email already exists")
            return redirect('register')

        # Create user
        user = User.objects.create_user(
            username=user_name,
            email=email
        )
        user.set_password(password)
        user.save()

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'register.html')
