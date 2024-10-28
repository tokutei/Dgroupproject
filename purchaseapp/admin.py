from django.contrib import admin
from .models import CartPost, OrderPost, OrderAitemPost

admin.site.register(CartPost)
admin.site.register(OrderPost)
admin.site.register(OrderAitemPost)

# Register your models here.
