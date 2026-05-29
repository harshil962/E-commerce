
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
    
    path('color-filter/', views.color_filter_view, name='color_filter_view'),
    path('size-filter/', views.size_filter_view, name='size_filter_view'),
    
    
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),

]
