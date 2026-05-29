import re
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
# Create your views here.


def register_page(request):

    if request.method == "POST":

        username = request.POST['username']
        email = request.session['email'] = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        context = {
            "username": username,
            "email": email,
        }

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'register.html', context)

        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'register.html', context)

        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, 'register.html', context)

        elif len(password) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return render(request, 'register.html', context)

        elif not re.search(r"[A-Z]", password):
            messages.error(request, "Password must contain one uppercase letter")
            return render(request, 'register.html', context)

        elif not re.search(r"[a-z]", password):
            messages.error(request, "Password must contain one lowercase letter")
            return render(request, 'register.html', context)

        elif not re.search(r"[0-9]", password):
            messages.error(request, "Password must contain one number")
            return render(request, 'register.html', context)

        elif not re.search(r"[!@#$%^&*()_+=]", password):
            messages.error(request, "Password must contain one special character")
            return render(request, 'register.html', context)

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'register.html')

# LOGIN
def login_page(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        context = {
            "username": username
        }

        # CHECK EMPTY

        if username == "" or password == "":
            messages.error(request, "All fields are required")
            return render(request, 'login.html', context)

        # AUTHENTICATE USER

        user = authenticate(
            request,
            username=username,
            password=password
        )

        # LOGIN SUCCESS

        if user is not None:

            login(request, user)

            messages.success(request, "Login Successful")

            return redirect('index')

        # INVALID LOGIN

        else:

            messages.error(request, "Invalid Username or Password")

            return render(request, 'login.html', context)

    return render(request, 'login.html')

# LOGOUT
def logout_page(request):

    logout(request)
    return redirect('login')

def index(request):
    if 'email' in request.session:
        uid=register_page.objects.get(email=request.session['email'])  
        data = Departments.objects.all()
        
        departments = data
        products = Product.objects.all()
        latest_products = Product.objects.all().order_by('-created_at')[:6]
        top_rated_products = Product.objects.all().order_by('-price')[:6]
        review_products = Product.objects.all().order_by('?')[:6]
        

        context = {
            "data": data,
            "departments": departments,
            "products": products,
            "latest_products": latest_products,
            "top_rated_products": top_rated_products,
            "review_products": review_products,
            "uid":uid
        }

        return render(request, "index.html", context)
    else:
        return render(request, "login.html")
    

def blog(request):
    return render(request, 'blog.html')


def blog_details(request):
    return render(request, 'blog-details.html')


def checkout(request):
    return render(request, 'checkout.html')


def contact(request,id):
    
    return render(request, 'contact.html')


def main(request):
    return render(request, 'main.html')


def shop_details(request):
    return render(request, 'shop-details.html')

def detail(request,id):
    pid = Product.objects.get(id=id)
    products = Product.objects.all()
    context = {
        "products" :products,
        "pid" :pid
    }
    return render(request, 'shop-details.html',context)

def shop_grid(request):
    if 'email' in request.session:
        uid=register_page.objects.get(email=request.session['email'])        
        data = Departments.objects.all()
        products = Product.objects.all()
        cf = Color_filter.objects.all()
        size = Size.objects.all()

        category_id = request.GET.get('category')

        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        if category_id:
            products = products.filter(
                department_id=category_id
            )

        if min_price and max_price:

            print("min price",min_price)
            print("max_price", max_price)

            products = products.filter(
                price__gte=int(min_price[1:]),
                price__lte=int(max_price[1:])
            )
            
        context = {
            "data": data,
            "products": products,
            "cf": cf,
            "size": size,
            "category_id": category_id,
            "min_price": min_price,
            "max_price": max_price,
            "uid":uid
        }

        return render(request, "shop-grid.html", context)
    return render(request, "login.html")


def color_filter_view(request):
    data = Departments.objects.all()
    products = Product.objects.all()
    cf = Color_filter.objects.all()
    size = Size.objects.all()

    color_id = request.GET.getlist('color')

    col_fil = []

    if color_id:
        col_fil.append(color_id)

        products = products.filter(
            color_filter_id__in=color_id
        )

    context = {
        "data": data,
        "products": products,
        "cf": cf,
        "size": size,
        "color_id": color_id,
        "col_fil": col_fil,
    }

    return render(request, "shop-grid.html", context)

def size_filter_view(request):
    data = Departments.objects.all()
    products = Product.objects.all()
    cf = Color_filter.objects.all()
    size = Size.objects.all()

    size_id = request.GET.getlist('size')

    size_fil = []

    if size_id:
        size_fil.append(size_id)

        products = products.filter(
            size_filter_id__in=size_id
        )

    context = {
        "data": data,
        "products": products,
        "cf": cf,
        "size": size,
        "size_id": size_id,
        "size_fil": size_fil,
    }

    return render(request, "shop-grid.html", context)

def shoping_cart(request):
    
    return render(request, 'shoping-cart.html')