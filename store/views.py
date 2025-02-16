from django.shortcuts import render
from django.http import HttpResponseServerError, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse, QueryDict
from .models import Product, PriceBreak, CartItem
import json


def index(request):
    cart_item_count = CartItem.objects.count()
    return render(request, 'store/index.html', { 'cart_item_count': cart_item_count })
    

def orders(request):
    cart_item_count = CartItem.objects.count()
    return render(request, 'store/orders.html', { 'cart_item_count': cart_item_count })
    
    
def products(request):
    products = Product.objects.all()
    cart_item_count = CartItem.objects.count()
    return render(request, 'store/products.html', { "products": products, 'cart_item_count': cart_item_count })


def product(request, product_id):
    
    product = Product.objects.filter(id=product_id).first()
    
    if product is None:
        return HttpResponseNotFound('Error 404 - Product could not be found')
    
    price_breaks = PriceBreak.objects.filter(product_id=product.pk)
    
    try:
        minimum_quantity = min([price_break.minimum_units for price_break in price_breaks])
    except ValueError:
        minimum_quantity = 0
    
    if minimum_quantity < 0:
        return HttpResponseServerError()
    
    price_breakdown, total = product.get_price_breakdown(minimum_quantity)
    
    cart_item = CartItem.objects.filter(product_id=product.pk).first()    
    
    if cart_item is not None:
        quantity = cart_item.quantity
    else:
        quantity = minimum_quantity
    
    cart_item_count = CartItem.objects.count()
    
    return render(request, 'store/product.html', { "product": product, 'price_breaks': price_breaks, 'price_breakdown': price_breakdown, 'total': total, 'minimum_quantity': minimum_quantity, 'cart_item_count': cart_item_count, 'in_cart': cart_item is not None, 'quantity': quantity })


def price_breakdown(request, product_id):
    
    try:
        quantity = int(request.POST.get('quantity', ''))
    except TypeError:
        quantity = 0
    
    product = Product.objects.filter(id=product_id).first()
    
    if product is None:
        return HttpResponseNotFound()
    
    price_breaks = PriceBreak.objects.filter(product_id=product.pk)
    
    minimum_quantity = min([price_break.minimum_units for price_break in price_breaks])
    
    if minimum_quantity < 0:
        return HttpResponseServerError()
    
    price_breakdown, total = product.get_price_breakdown(quantity)
    
    cart_item_count = CartItem.objects.count()
    
    return render(request, 'store/price_breakdown.html', { 'price_breakdown': price_breakdown, 'total': total, 'cart_item_count': cart_item_count })
  

def add_to_cart(request, product_id):
    
    try:
        quantity = int(request.POST.get('quantity', ''))
    except TypeError:
        return HttpResponseBadRequest()
    
    product = Product.objects.filter(id=product_id).first()
    
    if product is None:
        return HttpResponseNotFound()
    
    existing_cart_item = CartItem.objects.filter(product_id=product_id).first()
    
    if existing_cart_item is None:
        cart_item = CartItem.objects.create(product=product, quantity=quantity)
        cart_item.save()
    else:
        existing_cart_item.quantity = quantity
        existing_cart_item.save()
    
    cart_item_count = CartItem.objects.count()
    
    response = render(request, 'store/navbar_cart_button.html', { 'cart_item_count': cart_item_count })
    response['HX-Trigger'] = 'added_to_cart';
    
    return response

def cart(request):
    
    if request.method == 'DELETE':
        
        data = QueryDict(request.body.decode('utf-8'))
        item_id = data.get('item_id')
        
        cart_item = CartItem.objects.filter(id=item_id)
        cart_item.delete()
        
        response = HttpResponse('')
        response['HX-Refresh'] = 'true'
        
        return response
    
    cart = CartItem.objects.all()
    
    return render(request, 'store/cart.html', { 'cart': cart, 'cart_item_count': len(cart) })
    