from django.shortcuts import render, get_object_or_404
from products.models import Product
from .forms import MakePaymentForm, OrderForm

def get_cart_items_and_total(cart):
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
    
    return { 'cart_items': cart_items, 'cart_total': cart_total }
    
    



# Create your views here.
def show_checkout(request):
    
    cart = request.session.get('cart', {})
    cart_items_and_total = get_cart_items_and_total(cart)

    payment_form = MakePaymentForm()
    order_form = OrderForm()
    context = { 'order_form': order_form, 'payment_form': payment_form }
    
    context.update(cart_items_and_total)
    
    return render(request, "checkout/checkout.html", context)
