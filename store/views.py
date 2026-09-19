from django.shortcuts import render, get_object_or_404
from .models import product,order,orderitem
from django.http import JsonResponse
from django.conf import settings
from django.db import transaction
import json


# Create your views here.
def home(request):
    return render(request, "store/pstore2.html")


def productdetails(request, slug_field):
    # selectproduct=product.objects.get(id=product_id)
    selectproduct = get_object_or_404(product, slug=slug_field)
    context = {
        'selectproduct': selectproduct,
    }
    return render(request, "store/product.html", context)


def products_api(request):
    products = product.objects.all()
    # print("MEDIA_URL:", settings.MEDIA_URL)
    # for product_item in products:
    #     print("IMAGE NAME:", product_item.image.name)
    #     print("IMAGE URL:", product_item.image.url)
    data = []
    for product_item in products:
        data.append({
            'id': product_item.id,
            'image': product_item.image.url,
            'name': product_item.name,
            'price': product_item.price,
            'stock': product_item.stock,
            'slug': product_item.slug
        })
    return JsonResponse(data, safe=False)


def cart(request):
    return render(request, "store/pstorecart2.html")


def cart_api(request):
    # if request.method == "POST":
    if request.method != "POST":
        return JsonResponse({
            "message": "این API فقط درخواست POST را قبول می‌کند"
        }, status=405)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "message": "داده JSON نامعتبر است"
        }, status=400)
    if not data:
        return JsonResponse({
            "message": "سبد خرید خالی است"
        }, status=400)
    for item in data:
        if "product_id" not in item or "quantity" not in item:
            return JsonResponse({
                "message": "داده ها نامعتبر است"
            }, status=400)
    for item in data:
        # if not isinstance(item["quantity"] , int) or item["quantity"] <= 0:
        if not type(item["quantity"] is int) or item["quantity"] <= 0:
            return JsonResponse({
                "message": "تعداد محصول نامعتبر است"
            }, status=400)
    for item in data:
        # if not isinstance(item["product_id"], int):
        if type(item["product_id"] is int):
            return JsonResponse({
                "message": "شناسه محصول نامعتبر است"
            }, status=400)
    ordered_data = sorted(
        data, key=lambda item: item["product_id"]
    )
    product_by_id = {}
    try:
        with transaction.atomic():
            # for item in data:
            total_price = 0
            for item in ordered_data:
                # product_obj = get_object_or_404(product, id=item["product_id"])
                # برای مدیریت دو درخواست همزمان باید هنگام تراکنش اول رکورد محصول را قفل کنیم
                # product_obj = get_object_or_404(product.objects.select_for_update(), id=item["product_id"])
                try:
                    product_obj = product.objects.select_for_update().get(
                        id=item["product_id"]
                    )
                except product.DoesNotExist:
                    return JsonResponse({
                        "message": "محصول مورد نظر پیدا نشد"
                    }, status=400)
                stock = product_obj.stock
                product_by_id[item["product_id"]] = product_obj
                if stock >= item["quantity"]:
                    print("موجودی کافی")
                else:
                    # print("")
                    return JsonResponse({
                        "message": "عدم موجودی"
                    },status=409)
                total_price += product_obj.price * item["quantity"]

            new_order = order.objects.create(total_price=total_price)
            for item in data:
                # product_obj = product.objects.get(id=item["product_id"])
                product_obj = product_by_id[item["product_id"]]
                orderitem.objects.create(order=new_order, product_id=product_obj.id, quantity=item["quantity"],
                                         unit_price=product_obj.price)
                product_obj.stock -= item["quantity"]
                product_obj.save()
    # except Exception:
    #     return JsonResponse({
    #         "message":"خطا در ثبت سفارش"},
    #         status=500
    #     )
    except Exception as error:
        print(type(error).__name__)
        print(error)

        return JsonResponse({
            "message": "خطا در ثبت سفارش"
        }, status=500)


    # print(data)
    return JsonResponse({
        "message": "سفارش با موفقیت ثبت شد",
        "order_id":new_order.id,
        "total_price": new_order.total_price
    },status=201)
