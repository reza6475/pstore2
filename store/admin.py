from django.contrib import admin
from .models import product, order, orderitem, payment
from django.template.response import TemplateResponse
from .forms import OrderDateRangeForm

admin.site.register(product)


# admin.site.register(order)
# class OrderDateRangeFilter(admin.SimpleListFilter):
class OrderDateRangeFilter(admin.ListFilter):
    title = "بازه تاریخ سفارش"
    template = "store/filter_date_range.html"

    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)
        self.date_form = OrderDateRangeForm(request.GET or None)

        params.pop("start_date", None)
        params.pop("end_date", None)

    @property
    def media(self):
        return OrderDateRangeForm().media

    def has_output(self):
        return True

    def expected_parameters(self):
        return ["start_date", "end_date"]

    def choices(self, changelist):
        return []

    def queryset(self, request, queryset):
        date_form = OrderDateRangeForm(request.GET)
        if date_form.is_valid():
            start_date = date_form.cleaned_data["start_date"]
            end_date = date_form.cleaned_data["end_date"]
            if start_date:
                queryset = queryset.filter(
                    created_at__date__gte=start_date)
            if end_date:
                queryset = queryset.filter(
                    created_at__date__lte=end_date
                )

        return queryset


@admin.register(orderitem)
class OrderitemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "unit_price")


class orderiteminline(admin.TabularInline):
    model = orderitem
    extra = 0
    readonly_fields = ("order", "product", "quantity", "unit_price")


@admin.register(order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "total_price")
    inlines = [orderiteminline]
    readonly_fields = ("total_price",)
    ordering = ("-created_at",)
    search_fields = ("user__username",)
    list_filter = ("created_at",)
    list_filter = (OrderDateRangeFilter,)


admin.site.register(payment)

# Register your models here.
