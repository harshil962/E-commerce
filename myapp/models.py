from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import timedelta
from django.utils import timezone
# Create your models here.

class Departments(models.Model):
    name = models.CharField(max_length=40)
    
    def __str__(self):
        return self.name


class Color_filter(models.Model):
    c_name = models.CharField(max_length=40)
    
    def __str__(self):
        return self.c_name
    
class Size(models.Model):
    s_name = models.CharField(max_length=40)
    
    def __str__(self):
        return self.s_name
    
class Product(models.Model):

    department = models.ForeignKey(Departments, on_delete=models.CASCADE,blank=True,null=True)
    color_filter = models.ForeignKey(Color_filter, on_delete=models.CASCADE,blank=True,null=True)
    
    size_filter = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    created_at  = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.order.id} - {self.product.name}"
    
class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
       return self.created_at < timezone.now() - timedelta(minutes=15)
    