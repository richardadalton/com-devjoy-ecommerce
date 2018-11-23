from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from products.models import Product
from .forms import MakePaymentForm, OrderForm
from .models import OrderLineItem
from django.conf import settings
from django.contrib import messages
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

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
    context = { 'order_form': order_form, 'payment_form': payment_form, 'publishable': settings.STRIPE_PUBLISHABLE_KEY }
    
    context.update(cart_items_and_total)
    
    return render(request, "checkout/checkout.html", context)


def submit_payment(request):
    
    cart = request.session.get('cart', {})
    cart_items_and_total = get_cart_items_and_total(cart)

    payment_form = MakePaymentForm(request.POST)    
    order_form = OrderForm(request.POST)
    
    if order_form.is_valid() and payment_form.is_valid():
        
        # Save the Order to the Database
        order = order_form.save()
        cart = request.session.get('cart', {})
        for product_id, quantity in cart.items():
            line_item = OrderLineItem()
            line_item.product_id = product_id
            line_item.quantity = quantity
            line_item.order = order
            line_item.save()
        
        
        # Grab the money and run
        total = cart_items_and_total['cart_total']
        stripe_token=payment_form.cleaned_data['stripe_id']

        try:
            total_in_cent = int(total*100)
            customer = stripe.Charge.create(
                amount=total_in_cent,
                currency="EUR",
                description="Dummy Transaction",
                card=stripe_token,
            )

        except stripe.error.CardError:
            messages.error(request, "Your card was declined!")

        if customer.paid:
            messages.error(request, "You have successfully paid")

        # Clear the cart
        del request.session['cart']   
        
        # Redirect to home
        return redirect("/")