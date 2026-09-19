from django.shortcuts import render
from store.models import  product
def home (request):
    products=product.objects.all()
    context={
        'products':products
    }
    return render(request,"pstore2.html",context)
