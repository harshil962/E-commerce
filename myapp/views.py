from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import logout
import re
from django.contrib import messages
from .models import *
from functools import wraps
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings



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

        if password != request.POST.get("confirm_password"):
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
    password=make_password(password)
)

        messages.success(request, "Registration successful")
        return redirect("login")

    return render(request, "register.html")



def login_page(request):
    if request.session.get("user_id"):
        return redirect("index")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = Human.objects.filter(username=username).first()

        if user and check_password(password, user.password):
            request.session["user_id"] = user.id
            request.session["username"] = user.username
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
        products = Product.objects.filter(department__isnull=False).order_by('?')[:8]
        latest_products = Product.objects.all().order_by('-created_at')[:6]
        top_rated_products = Product.objects.all().order_by('-price')[:6]
        review_products = Product.objects.all().order_by('?')[:6]
        category_id = request.GET.get('category')
       
        wishlist_products = []
        wishlist_count = 0

        user_id = request.session.get("user_id")

        if user_id:
            wishlist_qs = Wishlist.objects.filter(user_id=user_id)
            wishlist_products = wishlist_qs.values_list("product_id", flat=True)
            wishlist_count = wishlist_qs.count()


        
        if category_id:
            products = products.filter(
                department_id=category_id
            )
            
        context = {
            "data": data,
            "departments": departments,
            "products": products,
            "latest_products": latest_products,
            "top_rated_products": top_rated_products,
            "review_products": review_products,
            "category_id": category_id,
            "wishlist_products": wishlist_products,
            "wishlist_count": wishlist_count, 

        }

        return render(request, "index.html", context)
    

def blog(request):
    return render(request, 'blog.html')


def blog_details(request):
    return render(request, 'blog-details.html')

@login_required_custom
def checkout(request):
    data = Departments.objects.all()
    user_id = request.session.get("user_id")
    user = get_object_or_404(Human,id=user_id)
    
    cart_items = Cart.objects.filter(user=user)
    
    total = 0
    for item in cart_items:
        item.subtotal = item.product.price * item.quantity
        total += item.subtotal
    
    if request.method == "POST":
        order = Order.objects.create(
            user=user,
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            address=request.POST.get("address"),
            city=request.POST.get("city"),
            phone=request.POST.get("phone"),
            email=request.POST.get("email"),
            total_amount=total
        ) 
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        cart_items.delete()
        
        messages.success(request, "Order placed successfully")
        return redirect("index")
        
        
    context = {
        "data":data,
        "cart_items":cart_items,
        "total":total
    }
    return render(request, 'checkout.html',context)


def contact(request):
    
    return render(request, 'contact.html')


def main(request):
    return render(request, 'main.html')


def shop_details(request):
    product = Product.objects.first()

    return render(request, "shop-details.html", {
        "pid": product
    })

@login_required_custom
def detail(request,id):
    data = Departments.objects.all()

    pid = get_object_or_404(Product, id=id)
    user_id = request.session.get("user_id")
    user = get_object_or_404(Human, id=user_id)

    cart_item = Cart.objects.filter(
    user=user,
    product=pid
    ).first()
    wishlist_products = list(
    Wishlist.objects.filter(
        user=user
    ).values_list("product_id", flat=True)
)
    products = Product.objects.all()
    context = {
        "products" :products,
        "pid" :pid,
        "data": data,
        "cart_item": cart_item,
        "wishlist_products": wishlist_products,
    }
    return render(request, 'shop-details.html',context)


@login_required_custom
def shop_grid(request):
        data = Departments.objects.all()
        products = Product.objects.all().order_by("-id")
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


        wishlist_products = []
        user_id = request.session.get("user_id")
        if user_id:
            wishlist_products = Wishlist.objects.filter(
                user_id=user_id
            ).values_list("product_id", flat=True)
            
        context = {
            "data": data,
            "products": products,
            "cf": cf,
            "size": size,
            "category_id": category_id,
            "min_price": min_price,
            "max_price": max_price,
            "show_page":show_page,
            "total_count": paginator.count,
            "wishlist_products": wishlist_products,  
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
    paginator = Paginator(products, 6)
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)

    show_page = paginator.get_elided_page_range(
        products.number,
        on_each_side=1,
        on_ends=1
    )
    
    context = {
        "data": data,
        "products": products,
        "cf": cf,
        "size": size,
        "color_id": color_id,
        "col_fil": col_fil,
        "show_page":show_page
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
    
    paginator = Paginator(products, 6)
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)

    show_page = paginator.get_elided_page_range(
        products.number,
        on_each_side=1,
        on_ends=1
    )

    context = {
        "data": data,
        "products": products,
        "cf": cf,
        "size": size,
        "size_id": size_id,
        "size_fil": size_fil,
        "show_page":show_page
    }

    return render(request, "shop-grid.html", context)

@login_required_custom
def shoping_cart(request):
    data = Departments.objects.all()

    user_id = request.session.get("user_id")

    user = get_object_or_404(Human, id=user_id)

    cart_items = Cart.objects.filter(user=user)

    total = 0
    total_quantity = 0

    for item in cart_items:
        item.subtotal = item.product.price * item.quantity
        total += item.subtotal
        total_quantity += item.quantity

    context = {
        "data": data,
        "cart_items": cart_items,
        "total": total,
        "total_quantity": total_quantity,
    }

    return render(request, "shoping-cart.html", context)


@login_required_custom
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    user_id = request.session.get("user_id")
    user = get_object_or_404(Human, id=user_id)

    cart_item = Cart.objects.filter(
        user=user,
        product=product
    ).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart.objects.create(
            user=user,
            product=product,
            quantity=1
        )

    return redirect("shoping_cart")

@login_required_custom
def remove_from_cart(request, id):
    user_id = request.session.get("user_id")
    user = get_object_or_404(Human, id=user_id)

    cart_item = get_object_or_404(
        Cart,
        id=id,
        user=user
    )

    cart_item.delete()

    return redirect("shoping_cart")

@login_required_custom
def increase_quantity(request, id):
    user_id = request.session.get("user_id")
    user = get_object_or_404(Human, id=user_id)
    cart_item = get_object_or_404(Cart, id=id, user=user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect(request.META.get('HTTP_REFERER', 'shoping_cart'))

@login_required_custom
def decrease_quantity(request, id):
    user_id = request.session.get("user_id")
    user = get_object_or_404(Human, id=user_id)
    cart_item = get_object_or_404(Cart, id=id, user=user)
    cart_item.quantity -= 1
    if cart_item.quantity <= 0:
        cart_item.delete()
    else:
        cart_item.save()
    return redirect(request.META.get('HTTP_REFERER', 'shoping_cart'))



@login_required_custom
def toggle_wishlist_ajax(request):
    if request.method == "POST":
        try:
            product_id = request.POST.get("product_id")

            if not product_id:
                return JsonResponse({"status": "error", "message": "Product ID missing"}, status=400)

            user_id = request.session.get("user_id")
            user = get_object_or_404(Human, id=user_id)
            product = get_object_or_404(Product, id=product_id)

            wishlist_item = Wishlist.objects.filter(user=user, product=product).first()

            if wishlist_item:
                wishlist_item.delete()
                return JsonResponse({"status": "success", "action": "removed", "in_wishlist": False})
            else:
                Wishlist.objects.create(user=user, product=product)
                return JsonResponse({"status": "success", "action": "added", "in_wishlist": True})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


@login_required_custom
def wishlist_page(request):
    user_id = request.session.get("user_id")
    user = get_object_or_404(Human, id=user_id)

    wishlist_items = Wishlist.objects.filter(user=user).select_related("product")

    context = {
        "wishlist_items": wishlist_items,
        "data": Departments.objects.all(), 
    }
    return render(request, "wishlist.html", context)

@login_required_custom
def my_order(request):
    user_id = request.session.get("user_id")
    user = get_object_or_404(Human, id=user_id)

    orders = Order.objects.filter(user=user).order_by("-created_at")

    return render(request, "my-orders.html", {
        "orders": orders,
        "data": Departments.objects.all(), 
    })


@login_required_custom
def order_detail(request, id):
    user_id = request.session.get("user_id")
    user = get_object_or_404(Human, id=user_id)

    order = get_object_or_404(
        Order,
        id=id,
        user=user
    )

    order_items = OrderItem.objects.filter(order=order)

    context = {
        "order": order,
        "order_items": order_items,
        "data": Departments.objects.all()
    }

    return render(request, "order_detail.html", context)


def search_product(request):
    data = Departments.objects.all()
    cf = Color_filter.objects.all()
    size = Size.objects.all()

    query = request.GET.get("search", "").strip()

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    user_id = request.session.get("user_id")
    wishlist_products = []

    if user_id:
        wishlist_products = Wishlist.objects.filter(
            user_id=user_id
        ).values_list("product_id", flat=True)

    context = {
        "products": products,
        "data": data,
        "cf": cf,
        "size": size,
        "query": query,
        "wishlist_products": wishlist_products,
        "total_count": products.count(),
    }

    return render(request, "shop-grid.html", context)


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = Human.objects.get(email=email)
            # delete old tokens first
            PasswordResetToken.objects.filter(user=user).delete()
            token_obj = PasswordResetToken.objects.create(user=user)
            domain = get_current_site(request).domain
            reset_link = f"http://{domain}/reset-password/{token_obj.token}/"
            send_mail(
                "Reset Your Password",
                f"Click this link to reset your password:\n\n{reset_link}\n\nThis link expires in 15 minutes.",
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            return render(request, "forgot_password.html", {
                "message": "Reset link sent! Check your email."
            })
        except Human.DoesNotExist:
            return render(request, "forgot_password.html", {
                "error": "No account found with that email."
            })
    return render(request, "forgot_password.html")


def reset_password(request, token):
    try:
        token_obj = PasswordResetToken.objects.get(token=token)
    except PasswordResetToken.DoesNotExist:
        return render(request, "reset_password.html", {"error": "Invalid link."})

    if token_obj.is_expired():
        token_obj.delete()
        return render(request, "reset_password.html", {"error": "Link expired."})
    if request.method == "POST":
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if new_password != confirm_password:
            return render(request, "reset_password.html", {"error": "Passwords do not match.", "token": token})
        human = Human.objects.get(id=token_obj.user.id)
        human.password = make_password(new_password)
        human.save()
        token_obj.delete()
        messages.success(request, "Password reset successful. Please login.")
        return redirect("login")

    return render(request, "reset_password.html", {"token": token})