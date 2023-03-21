from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings
from django.contrib import messages
from django.db.models import Sum

from .models import Product, CartItem,Order,OrderItem
from django.db.models import Q
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_order_confirmation_email(order):
    subject = 'Order Confirmation'
    message = render_to_string('ecommerce/order_confirmation.html', {'order': order})
    from_email = 'your-email@example.com'
    recipient_list = [order.customer_email]
    send_mail(subject, message, from_email, recipient_list)

def Ecommerce_index(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query)
        )
    else:
        products = Product.objects.all()
    context = {'products': products}
    return render(request, 'ecommerce/ecommerce_index.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    return render(request, 'ecommerce/product_detail.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_session_key = request.session.session_key or SessionStore().session_key
    cart_item, created = CartItem.objects.get_or_create(
        product=product, user_session_key=user_session_key)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.name} was added to your cart!")
    return redirect('ecommerce:cart')


def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_session_key = request.session.session_key or SessionStore().session_key
    cart_item = CartItem.objects.get(product=product, user_session_key=user_session_key)
    if cart_item.quantity == 1:
        cart_item.delete()
    else:
        cart_item.quantity -= 1
        cart_item.save()
    messages.success(request, f"{product.name} was removed from your cart.")
    return redirect('ecommerce:cart')

def cart(request):
    user_session_key = request.session.session_key or SessionStore().session_key
    cart_items = CartItem.objects.filter(user_session_key=user_session_key)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Create a new order
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total_price
            order.save()

            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    product=cart_item.product,
                    order=order,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

            # Clear the cart
            CartItem.objects.filter(user_session_key=user_session_key).delete()

            # Redirect to the confirmation page
            return redirect('ecommerce:order_confirmation', order_id=order.id)
    else:
        form = OrderForm()

    context = {'cart_items': cart_items, 'total_price': total_price, 'form': form}
    return render(request, 'ecommerce/cart.html', context)

@login_required
def checkout(request):
    user_session_key = request.session.session_key or SessionStore().session_key
    cart_items = CartItem.objects.filter(user_session_key=user_session_key)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Create a new order
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total_price
            order.save()

            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    product=cart_item.product,
                    order=order,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

            # Clear the cart
            CartItem.objects.filter(user_session_key=user_session_key).delete()

            # Send order confirmation email
            send_order_confirmation_email(order)

            # Redirect to the confirmation page
            return redirect('ecommerce:order_confirmation', order_id=order.id)
    else:
        form = OrderForm()

    context = {'cart_items': cart_items, 'total_price': total_price, 'form': form}
    return render(request, 'ecommerce/checkout.html', context)

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'ecommerce/order_confirmation.html', context)