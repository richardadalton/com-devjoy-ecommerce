from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

# Create your views here.
def product_list(request):
    products = Product.objects.all()   
    return redirect("product_detail", id=1)
    
    return render(request, "products/product_list.html", {'products': products})
    
    
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, "products/product_detail.html", {'product': product})