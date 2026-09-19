from django.db import models


class product(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام محصول")
    slug = models.SlugField(max_length=200, unique=True)
    price = models.PositiveIntegerField(verbose_name="قیمت واحد")
    stock = models.PositiveIntegerField(verbose_name="موجودی")
    # image=models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/')
    isnew = models.BooleanField(default=False)
    isoffer = models.BooleanField(default=False)
    description = models.TextField()

    def __str__(self):
        return f"({self.name} )"


class order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان سفارش")
    total_price = models.PositiveIntegerField(verbose_name="جمع کل")

    def __str__(self):
        return f"سفارش شماره {self.id}"


class orderitem(models.Model):
    order = models.ForeignKey(
        order,
        on_delete=models.CASCADE,
        verbose_name="شماره سفارش"
    )

    product = models.ForeignKey(
        product,
        on_delete=models.PROTECT,
        verbose_name="نام محصول"
    )

    quantity = models.PositiveIntegerField(verbose_name="تعداد سفارش")

    unit_price = models.PositiveIntegerField(verbose_name="قیمت واحد")

    def __str__(self):
        return f"({self.product.name})"
