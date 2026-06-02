from django.contrib.auth import logout
import re
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from functools import wraps
# Create your views here.
from django.core.paginator import Paginator



def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # Google login / Django auth
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)

        # Your old session login
        if request.session.get("user_id"):
            return view_func(request, *args, **kwargs)

        messages.error(request, "Please login first")
        return redirect("login")

    return wrapper

def register_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if Human.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        if Human.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("register")

        Human.objects.create(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Registration successful")
        return redirect("login")

    return render(request, "register.html")

def login_page(request):

    if request.user.is_authenticated or request.session.get("user_id"):
        return redirect("index")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = Human.objects.filter(
            username=username,
            password=password
        ).first()

        if user:
            request.session["user_id"] = user.id
            request.session["username"] = user.username

            messages.success(request, "Login successful")
            return redirect("index")

        messages.error(request, "Invalid username or password")
        return redirect("login")

    return render(request, "login.html")


def logout_page(request):
    logout(request)
    request.session.flush()

    messages.success(request, "Logged out successfully")
    return redirect("login")
     
     
@login_required_custom
def index(request):
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
        }

        return render(request, "index.html", context)
    

def blog(request):
    return render(request, 'blog.html')


def blog_details(request):
    return render(request, 'blog-details.html')


def checkout(request):
    return render(request, 'checkout.html')


def contact(request):
    
    return render(request, 'contact.html')


def main(request):
    return render(request, 'main.html')


def shop_details(request):
    return render(request, 'shop-details.html')

@login_required_custom
def detail(request,id):
    data = Departments.objects.all()
    pid = Product.objects.get(id=id)
    products = Product.objects.all()
    context = {
        "products" :products,
        "pid" :pid,
        "data": data,
    }
    return render(request, 'shop-details.html',context)


@login_required_custom
def shop_grid(request):
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
            
        paginator = Paginator(products,6)
        page_number = request.GET.get("page",1)
        try:
            page_number = int(page_number)
        except ValueError:
            page_number = 1 
        products = paginator.get_page(page_number)
        show_page=paginator.get_elided_page_range(page_number,on_each_side=1,on_ends=1)
           
        context = {
            "data": data,
            "products": products,
            "cf": cf,
            "size": size,
            "category_id": category_id,
            "min_price": min_price,
            "max_price": max_price,
            "show_page":show_page

        }

        return render(request, "shop-grid.html", context)

@login_required_custom
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


@login_required_custom

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

@login_required_custom
def shoping_cart(request):
    
    return render(request, 'shoping-cart.html')