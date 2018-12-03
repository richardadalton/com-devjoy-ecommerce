from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category

# Create your views here.
def product_list(request):
    breadcrumbs = []
    if 'category' in request.GET:
        category = get_object_or_404(Category, pk=request.GET['category'])
        products = Product.objects.filter(category = category)
        categories = Category.objects.filter(parent = category)
        
        while category:
            breadcrumbs = [category] + breadcrumbs
            category = category.parent
        
    else:
        products = Product.objects.filter(category__isnull = True)
        categories = Category.objects.filter(parent__isnull = True)
        
    
        
    return render(request, "products/product_list.html", {'products': products, 'categories': categories, 'breadcrumbs': breadcrumbs})
    
    
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, "products/product_detail.html", {'product': product})