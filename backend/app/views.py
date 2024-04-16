from django.shortcuts import render
from .models import Product, Cart
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import serializers
import pyrebase
import json

# config = json.loads("../firebase.json")
config = {
    "apiKey": "AIzaSyB5WCScausKqRuTnitQhhcuOzEA9jVfuu4",
    "authDomain": "accoai-ea6d7.firebaseapp.com",
    "storageBucket": "accoai-ea6d7.appspot.com",
    "databaseURL": "https://accoai-ea6d7-default-rtdb.firebaseio.com",
    "appId": "1:747060134486:web:f30233c8944b5696ecb1f7",
    "projectId": "accoai-ea6d7",
    "messagingSenderId": "747060134486",
}


firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Cart
        fields = "__all__"


@api_view(["GET"])
def product_list(request):
    category = request.GET.getlist("category")
    print(category)
    pricelow = request.GET.getlist("pricelow")[0]
    pricehigh = request.GET.getlist("priceup")[0]
    print(pricelow, pricehigh)
    if category == []:
        data = []
    else:
        data = ProductSerializer(
            Product.objects.filter(
                productCategory__in=category,
                productPrice__gte=pricelow,
                productPrice__lte=pricehigh,
            ),
            many=True,
        ).data

    return JsonResponse(data, safe=False)


@api_view(["GET"])
def get_product(request, productid):
    product = ProductSerializer(
        Product.objects.filter(productId=productid), many=True
    ).data

    return JsonResponse(product[0], safe=False)


@api_view(["GET"])
def get_cart_product(request):

    cart = CartSerializer(Cart.objects.all(), many=True).data

    return JsonResponse(cart, safe=False)


@api_view(["GET", "POST"])
def add_to_cart(request):
    data = request.data
    productID = data["productid"]
    productQuantity = data["productQuantity"]
    product = Product.objects.filter(productId=productID)
    if Cart.objects.filter(product=product[0]).exists():
        cart = Cart.objects.filter(product=product[0])[0]
        cart.quantity = productQuantity
        cart.save()
    else:
        Cart.objects.create(product=product[0], quantity=productQuantity)
    cart = CartSerializer(Cart.objects.all(), many=True).data

    return JsonResponse(cart, safe=False)


@api_view(["DELETE"])
def delete_product_cart(request):
    data = request.data
    productID = data["productid"]
    product = Product.objects.filter(productId=productID)
    cart = Cart.objects.filter(product=product[0]).delete()
    cart = CartSerializer(Cart.objects.all(), many=True).data

    return JsonResponse(cart, safe=False)


@api_view(["GET"])
def get_product_quantity(request, productid):
    product = Product.objects.filter(productId=productid)
    if Cart.objects.filter(product=product[0]).exists():
        cart = Cart.objects.filter(product=product[0])[0]
        return JsonResponse({"exists": "true", "quantity": cart.quantity})
    else:
        return JsonResponse({"exists": "false", "quantity": 0})


@api_view(["DELETE"])
def delete_cart(request):
    for cart in Cart.objects.all().values():
        product = Product.objects.filter(productId=cart["product_id"])[0]
        product.productTotalQuantity -= cart["quantity"]
        if product.productTotalQuantity < 0:
            product.productTotalQuantity = 0
        product.save()
    cart = Cart.objects.all().delete()
    return HttpResponse("deleted")


@api_view(["GET"])
def get_total_price(request):

    totalprice = 0.0
    cart = Cart.objects.all().values()
    for prod in cart:
        product = Product.objects.filter(productId=prod["product_id"])
        productPrice = product[0].productPrice
        quantity = prod["quantity"]
        totalprice += float(productPrice) * float(quantity)
    return JsonResponse({"total": totalprice})


@api_view(["GET"])
def firebaseProducts(request):
    data = database.child().child("hii").get().val()
    print(data)
    ref = database.reference("/")
    best_sellers = ref.get()
    ref.set({"Books": {"Best_Sellers": -1}})
    database.push({"hii": "hii"})

    # id = database.child("hii").get().val()

    return JsonResponse({"data": ""})
