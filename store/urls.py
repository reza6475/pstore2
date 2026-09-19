from  .import views
from django.urls import  path

urlpatterns=[
    path('',views.home),
    path('product/<slug:slug_field>/',views.productdetails),
    path('api/products/',views.products_api),
    path("cart/",views.cart),
    path("api/cart/",views.cart_api)
]
