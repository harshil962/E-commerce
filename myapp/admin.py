from django.contrib import admin
from .models import * 
# Register your models here.

admin.site.register(Departments)
admin.site.register(Product)
admin.site.register(Color_filter)
admin.site.register(Size)
admin.site.register(Order)
admin.site.register(OrderItem)