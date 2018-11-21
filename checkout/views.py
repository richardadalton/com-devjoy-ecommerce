from django.shortcuts import render, get_object_or_404
from products.models import Product
from .forms import MakePaymentForm


# Create your views here.
def show_checkout(request):
    cart = request.session.get('cart', {})
    
    cart_items = []
    cart_total = 0
    
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        item_total = product.price * quantity
        cart_items.append({
            'id': product.id,
            'name': product.name,
            'brand': product.brand,
            'sku': product.sku,
            'description': product.description,
            'image': product.image,
            'price': product.price,
            'stock': product.stock,
            'quantity': quantity,
            'total': item_total
        })
        cart_total += item_total


    
    form = MakePaymentForm()

    return render(request, "checkout/checkout.html", {'cart_items': cart_items, 'cart_total': cart_total, 'payment_form': form})
