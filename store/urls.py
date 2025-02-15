from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("products", views.products, name="products"),
    path("products/<int:product_id>", views.product, name="product"),
    path("products/<int:product_id>/price-breakdown", views.price_breakdown, name="product_price_breakdown"),
    path("orders", views.orders, name="orders"),
]