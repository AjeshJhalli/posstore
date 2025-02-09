from django.shortcuts import render
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
    return render(request, 'store/product.html', { "product": product, 'price_breaks': price_breaks })

