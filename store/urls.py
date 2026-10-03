from  .import views
from django.urls import  path

urlpatterns=[
    path('',views.home),
    path('product/<slug:slug_field>/',views.productdetails),
    path('api/products/',views.products_api),
    path("cart/",views.cart),
    path("api/cart/",views.cart_api),
    path("register/",views.register_form),
    path("login/",views.login_form),
    path("logout/",views.logout_form),
    path("account/",views.account),
    path("myorders/",views.my_orders)
]
