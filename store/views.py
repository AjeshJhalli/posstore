from django.shortcuts import render
from django.http import HttpResponseServerError
from .models import Product, PriceBreak


def index(request):
    return render(request, 'store/index.html', {})
    

def orders(request):
    return render(request, 'store/orders.html', {})
    
    
def products(request):
    products = Product.objects.all()
    return render(request, 'store/products.html', { "products": products })


def product(request, product_id):
    
    product = Product.objects.get(id=product_id)
    price_breaks = PriceBreak.objects.filter(product_id=product.pk)
    
    minimum_quantity = min([price_break.minimum_units for price_break in price_breaks])
    
    if minimum_quantity < 0:
        return HttpResponseServerError()
    
    price_breakdown, total = product.get_price_breakdown(minimum_quantity)
    
    return render(request, 'store/product.html', { "product": product, 'price_breaks': price_breaks, 'price_breakdown': price_breakdown, 'total': total, 'minimum_quantity': minimum_quantity })


def price_breakdown(request, product_id):
    
    try:
        quantity = int(request.POST.get('quantity', ''))
    except TypeError:
        quantity = 0
    
    product = Product.objects.get(id=product_id)
    price_breaks = PriceBreak.objects.filter(product_id=product.pk)
    
    minimum_quantity = min([price_break.minimum_units for price_break in price_breaks])
    
    if minimum_quantity < 0:
        return HttpResponseServerError()
    
    price_breakdown, total = product.get_price_breakdown(quantity)
    
    return render(request, 'store/price_breakdown.html', { 'price_breakdown': price_breakdown, 'total': total })
  