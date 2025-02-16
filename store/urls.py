from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("products", views.products, name="products"),
    path("products/<int:product_id>", views.product, name="product"),
    path("products/<int:product_id>/price-breakdown", views.price_breakdown, name="product_price_breakdown"),
    path("products/<int:product_id>/add-to-cart", views.add_to_cart, name="product_add_to_cart"),
    path("orders", views.orders, name="orders"),
    path("cart", views.cart, name="cart"),
]