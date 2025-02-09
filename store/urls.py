from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("products", views.products, name="products"),
    path("products/<int:product_id>", views.product, name="product"),
    path("orders", views.orders, name="orders"),
]