from django.test import TestCase

# Create your tests here.
import json

from django.test import TestCase

from .models import product, order, orderitem


class CartApiTests(TestCase):

    def test_create_order_successfully(self):
        # 1. آماده‌سازی
        product_obj = product.objects.create(
            name="Test Product",
            slug="test-product",
            price=10000,
            stock=5,
            description="Test description"
        )

        cart_data = [
            {
                "product_id": product_obj.id,
                "quantity": 2
            }
        ]

        # 2. اجرای عملیات
        response = self.client.post(
            "/api/cart/",
            data=json.dumps(cart_data),
            content_type="application/json"
        )

        # 3. بررسی نتیجه
        self.assertEqual(response.status_code, 201)
        self.assertEqual(order.objects.count(), 1)
        self.assertEqual(orderitem.objects.count(), 1)

        created_order = order.objects.get()
        created_orderitem = orderitem.objects.get()
        updated_product = product.objects.get(id=product_obj.id)

        self.assertEqual(created_order.total_price, 20000)
        self.assertEqual(created_orderitem.quantity, 2)
        self.assertEqual(created_orderitem.unit_price, 10000)
        self.assertEqual(updated_product.stock, 3)

    def test_create_order_with_insufficient_stock(self):
        product_obj = product.objects.create(
            name="Test Product",
            slug="test-product",
            price=10000,
            stock=5,
            description="Test description"
        )

        cart_data = [
            {
                "product_id": product_obj.id,
                "quantity": 6
            }
        ]

        response = self.client.post(
            "/api/cart/",
            data=json.dumps(cart_data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 409)