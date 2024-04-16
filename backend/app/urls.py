from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("product/<int:productid>", views.get_product, name="get_product"),
    path("cart", views.get_cart_product, name="get_cart_product"),
    path("addcart", views.add_to_cart, name="add_to_cart"),
    path("deleteProduct", views.delete_product_cart, name="delete_product_cart"),
    path(
        "product/cart/<int:productid>",
        views.get_product_quantity,
        name="get_product_quantity",
    ),
    path("deletecart", views.delete_cart, name="delete_cart"),
    path("cartprice", views.get_total_price, name="get_total_price"),
    path("firebase/products", views.firebaseProducts, name="firebaseProducts"),
]
