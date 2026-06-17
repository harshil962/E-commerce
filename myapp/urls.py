
# URL configuration for myproject project. # type: ignore

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.2/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))


from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('blog/', views.blog, name='blog'),
    path('blog-details/', views.blog_details, name='blog_details'),
    
    path('checkout/', views.checkout, name='checkout'),
    
    path('contact/', views.contact, name='contact'),
    path('main/', views.main, name='main'),
    
    path('shop-details/', views.shop_details, name='shop_details'),
    path('detail/<int:id>', views.detail, name='detail'),
    
    path('shop-grid/', views.shop_grid, name='shop_grid'),
    
    path('shoping-cart/', views.shoping_cart, name='shoping_cart'),           
    path('add-to-cart/<int:id>/',views.add_to_cart,name='add_to_cart'),
    path('remove-from-cart/<int:id>/',views.remove_from_cart,name='remove_from_cart'),
    path('increase-quantity/<int:id>/',views.increase_quantity,name='increase_quantity'),
    path('decrease-quantity/<int:id>/',views.decrease_quantity,name='decrease_quantity'),
    
    path('wishlist/', views.wishlist_page, name='wishlist_page'),
    path("wishlist/toggle/", views.toggle_wishlist_ajax, name="toggle_wishlist_ajax"),
    
    path('color-filter/', views.color_filter_view, name='color_filter_view'),
    path('size-filter/', views.size_filter_view, name='size_filter_view'),
    
    
    
    path(
    "search/",
    views.search_product,
    name="search_product"
),
    path("my_order/", views.my_order, name="my_order"),
    path("order_detail/<int:id>", views.order_detail, name="order_detail"),
    
    
    path("register/", views.register_page, name="register"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    
    
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-password/<uuid:token>/", views.reset_password, name="reset_password"),

]
