from django.contrib import admin

from .models import *

admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Product)
admin.site.register(PriceBreak)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CartItem)
