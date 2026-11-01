from django.shortcuts import render, get_object_or_404, redirect
from .models import product, order, orderitem, payment
from django.http import JsonResponse
from django.conf import settings
from django.db import transaction
import json
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import requests
from django.db.models import Prefetch


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
            'slug': product_item.slug,
            'description': product_item.description,
            'isnew': product_item.isnew,
            'isoffer': product_item.isoffer
        })
    return JsonResponse(data, safe=False)


def cart(request):
    return render(request, "store/pstorecart2.html")


@login_required
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
        if not type(item["quantity"]) is int or item["quantity"] <= 0:
            return JsonResponse({
                "message": "تعداد محصول نامعتبر است"
            }, status=400)
    for item in data:
        # if not isinstance(item["product_id"], int):
        if type(item["product_id"]) is not int:
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
                if stock < item["quantity"]:
                    return JsonResponse({
                        "message": "عدم موجودی"
                    }, status=409)
                total_price += product_obj.price * item["quantity"]
            new_order = order.objects.create(total_price=total_price, user=request.user)
            new_payment = payment.objects.create(order=new_order, amount=new_order.total_price, status="pending")
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
        "order_id": new_order.id,
        "total_price": new_order.total_price
    }, status=201)


def register_form(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        confirmpassword = request.POST["confirmpassword"]
        if User.objects.filter(username=username).exists():
            messages.warning(request, "نام کاربری تکراری")
            return render(request, "store/register.html")
        if password != confirmpassword:
            messages.warning(request, " عدم تطابق رمز عبور")
            return render(request, "store/register.html")
        else:
            User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            messages.success(request, "ثبت نام با موفقیت انجام شد")
            return redirect("/")
    return render(request, "store/register.html")


def login_form(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if not user:
            messages.warning(request, "نام کاربری یا رمز عبور اشتباه است")
            return render(request, "store/login.html")
        else:
            login(request, user)
            messages.success(request, "ورود موفق")
            return redirect("/")
    return render(request, "store/login.html")


def logout_form(request):
    logout(request)
    return redirect("/")


@login_required
def account(request):
    if request.method == "POST":
        currentpassword = request.POST["currentpassword"]
        if not request.user.check_password(currentpassword):
            messages.warning(request, "رمز عبور قیلی صحیح نمی باشد")
            return redirect("/account/")
        else:
            password = request.POST["password"]
            confirmpassword = request.POST["confirmpassword"]
            if password != confirmpassword:
                messages.warning(request, "عدم تطابق رمز عبور")
                return redirect("/account/")
            else:
                request.user.set_password(password)
                email = request.POST["email"]
                request.user.email = email
                request.user.save()
                messages.success(request, "اطلاعات با موفقیت ویرایش گردید")

    return render(request, "store/account.html")


@login_required
# def my_orders(request):
#     orders = order.objects.filter(user=request.user)
#     payments=payment.objects.get(order=orders)
#     if not orders:
#         messages.warning(request, "شما هنوز سفارشی ثبت نکرده اید")
#     context = {
#         "orders": orders,
#         "payment":payments.status,
#     }
#
#     return render(request, "store/myorders.html", context)
def my_orders(request):
    orders = order.objects.filter(
        user=request.user
    ).prefetch_related("payments")

    if not orders:
        messages.warning(
            request,
            "شما هنوز سفارشی ثبت نکرده‌اید"
        )

    for selected_order in orders:
        payments = list(selected_order.payments.all())

        # if any(p.status == "paid" for p in payments):
        #     selected_order.payment_status = "پرداخت شده"
        #
        # elif any(p.status == "pending" for p in payments):
        #     selected_order.payment_status = "در انتظار پرداخت"
        #
        # elif any(p.status == "failed" for p in payments):
        #     selected_order.payment_status = "پرداخت نشده"
        #
        # elif payments:
        #     selected_order.payment_status = "پرداخت نشده"
        #
        # else:
        #     selected_order.payment_status = "پرداخت  نشده"
        if any(p.status == "paid" for p in payments):
            selected_order.payment_status = "پرداخت‌شده"
        else:
            selected_order.payment_status = "پرداخت‌ نشده"

    return render(
        request,
        "store/myorders.html",
        {"orders": orders}
    )


@login_required
def order_details(request, order_id):
    select_order = get_object_or_404(order, id=order_id, user=request.user)

    order_item = orderitem.objects.filter(order=select_order)
    context = {
        "order": select_order,
        "order_item": order_item
    }
    return render(request, "store/orderdetail.html", context)


@login_required
def start_payment(request, order_id):
    select_order = get_object_or_404(
        order,
        id=order_id,
        user=request.user
    )

    select_payment = get_object_or_404(
        payment,
        order=select_order,
        status="pending",
    )
    if select_payment.authority:
        inquiry_url = settings.ZARINPAL_REQUEST_URL.replace(
            "request.json",
            "inquiry.json"
        )
        inquiry_data = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,
            "authority": select_payment.authority,
        }
        try:
            inquiry_response = requests.post(
                inquiry_url,
                json=inquiry_data,
                timeout=15,
            )
            inquiry_response.raise_for_status()
            inquiry_result = inquiry_response.json()


        except (requests.RequestException, ValueError):
            messages.warning(
                 request,
        "وضعیت پرداخت قبلی مشخص نشد؛ بعداً دوباره بررسی کنید."
    )
            return redirect("my_orders")


        inquiry_info = inquiry_result.get("data", {})
        inquiry_status = inquiry_info.get("status")
        inquiry_code = inquiry_info.get("code")
        if inquiry_code != 100 or not inquiry_status:
            messages.warning(
                request,
        "وضعیت پرداخت قبلی مشخص نشد."
    )
           return redirect("my_orders")
        if inquiry_status == "PAID":
           return payment_verify(request, select_payment)
        elif inquiry_status == "IN_BANK":
            messages.info(
                request,
                "تراکنش شما هنوز در حال انجام است."
            )
            return redirect("my_orders")
        elif inquiry_status == "VERIFIED":
            select_payment.status = "paid"
            select_payment.save(update_fields=["status"])
            messages.success(
                request,
                "پرداخت سفارش با موفقیت قبلا تأیید شده است."
            )
            return redirect("my_orders")
        elif inquiry_status == "FAILED":
            select_payment.status = "failed"
            select_payment.save(update_fields=["status"])

            payment.objects.create(
                order=select_order,
                amount=select_payment.amount,
                status="pending",
            )

            return redirect("start_payment", order_id=select_order.id)
        elif inquiry_status == "REVERSED":
            select_payment.status = "reversed"
            select_payment.save(update_fields=["status"])

            payment.objects.create(
                order=select_order,
                amount=select_payment.amount,
                status="pending",
            )
            return redirect("start_payment", order_id=select_order.id)
        else:
            messages.warning(
                request,
                "وضعیت تراکنش قابل تشخیص نیست؛ لطفاً بعداً دوباره بررسی کنید."
            )
            return redirect("my_orders")


# select_payment=select_order.payments.filter(status="pending")
# if select_payment.status == "pending":
    payment_status = "در انتظار پرداخت"
# elif select_payment.status == "paid":
#     payment_status = "پرداخت شده"
# elif select_payment.status == "failed":
#     payment_status = "پرداخت ناموفق"
    context = {
        "order": select_order,
        "payment": select_payment,
        "payment_status": payment_status
    }
    url_redirect = reverse("start_payment", kwargs={"order_id": order_id})
    if request.method == "POST":
    # if select_payment.status == "paid":
    #     messages.warning(request, "این سفارش قبلا پرداخت شده است")
    #     return redirect(url_redirect)
        callback_url = request.build_absolute_uri(
        reverse("payment_callback")
    )
        payment_data = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,
            "amount": select_payment.amount,
            "callback_url": callback_url,
            "description": f"Payment for order {select_order.id}",
    }
    # ارسال درخواست ایجاد پرداخت به زرین پال و مدیریت خطای ارتباطی
        try:
            response = requests.post(
            settings.ZARINPAL_REQUEST_URL,
            json=payment_data,
            timeout=15,
        )
            response.raise_for_status()
            result = response.json()

        except (requests.RequestException, ValueError):
            messages.error(request, "ارتباط با درگاه پرداخت برقرار نشد.")
            return redirect(url_redirect)
    # بررسی پاسخ زرین پال و استخراج authority
        payment_result = result.get("data", {})
        authority = payment_result.get("authority")

        if payment_result.get("code") != 100 or not authority:
            messages.error(request, "ایجاد درخواست پرداخت ناموفق بود.")
            return redirect(url_redirect)

        select_payment.authority = authority
        select_payment.save(update_fields=["authority"])

        return redirect(
        f"{settings.ZARINPAL_STARTPAY_URL}{authority}"
    )
    # else:

    #     select_payment.status = "paid"
    #     select_payment.save()
    #     messages.success(request, "سفارش شما با موفقیت پرداخت گردید")
    #     return redirect(url_redirect)
    return render(request, "store/payment.html", context)


def payment_callback(request):
    authority = request.GET.get("Authority")
    gateway_status = request.GET.get("Status")
    if not authority:
        messages.error(request, "اطلاعات بازگشت پرداخت نامعتبر است")
        return redirect("/")
    select_payment = get_object_or_404(
        payment,
        authority=authority,
        status="pending"
    )
    if gateway_status != "OK":
        select_payment.status = "failed"
        select_payment.save(update_fields=["status"])
        # ایجاد یک ردیف پرداخت جدید و ارسال به صفحه پرداخت برای اتصال به درگاه
        payment.objects.create(
            order=select_payment.order,
            amount=select_payment.amount,

            status="pending",
        )

        messages.error(request, "پرداخت انجام نشد یا توسط کاربر لغو شد.")

        return redirect(
            "my_orders",
        )
    return payment_verify(request, select_payment)


def payment_verify(request, select_payment):
    verify_data = {
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "authority": select_payment.authority,
        "amount": select_payment.amount,
    }

    verify_url = settings.ZARINPAL_REQUEST_URL.replace(
        "request.json",
        "verify.json",
    )

    try:
        response = requests.post(
            verify_url,
            json=verify_data,
            timeout=15,
        )
        response.raise_for_status()
        verify_result = response.json()

    except (requests.RequestException, ValueError):
        messages.error(
            request,
            "تأیید پرداخت از درگاه دریافت نشد؛ وضعیت پرداخت تغییر نکرد."
        )
        return redirect("start_payment", order_id=select_payment.order_id)

    verify_data_result = verify_result.get("data", {})
    verify_code = verify_data_result.get("code")

    if verify_code in (100, 101):
        select_payment.status = "paid"
        update_fields = ["status"]
        ref_id = verify_data_result.get("ref_id")

        if ref_id is not None:
          select_payment.ref_id = ref_id
          update_fields.append("ref_id")
        select_payment.save(update_fields=update_fields)
        messages.success(request, "پرداخت با موفقیت تأیید شد.")
        return redirect(
            "order_details",
            order_id=select_payment.order_id
        )

    else:
        select_payment.status = "failed"
        select_payment.save(update_fields=["status"])

        messages.error(request, "تأیید پرداخت ناموفق بود.")

        return redirect("start_payment", order_id=select_payment.order_id)
