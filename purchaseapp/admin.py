from django.contrib import admin
from .models import CartPost, OrderPost, OrderAitemPost, Product, Price, BuyJudge, Payment_intent


class PriceInlineAdmin(admin.TabularInline):
    model = Price
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [PriceInlineAdmin]


admin.site.register(CartPost)
admin.site.register(OrderPost)
admin.site.register(OrderAitemPost)
admin.site.register(Product, ProductAdmin)
admin.site.register(Price)
admin.site.register(BuyJudge)
admin.site.register(Payment_intent)

# Register your models here.
