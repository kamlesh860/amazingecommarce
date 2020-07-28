from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(register)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(UserDetail)
admin.site.register(Profile)
