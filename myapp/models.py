from django.db import models

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
    
    
class Human(models.Model):
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)
    
    def __str__(self):
        return self.username
    
    

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