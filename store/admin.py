from django.contrib import admin
from .models import product,order,orderitem
admin.site.register(product)
# admin.site.register(order)
@admin.register(orderitem)
class OrderitemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity","unit_price")
class orderiteminline(admin.TabularInline):
    model = orderitem
    extra = 0
    readonly_fields = ("order","product", "quantity", "unit_price")
@admin.register(order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "total_price")
    inlines = [orderiteminline]
    readonly_fields = ("total_price",)

# Register your models here.
