from django.db import models as djmodels
from django.conf import settings
from django.utils import timezone


class Product(djmodels.Model):
    productId = djmodels.AutoField(primary_key=True)
    productURL = djmodels.CharField(max_length=500)
    productName = djmodels.CharField(max_length=200)
    productDescription = djmodels.TextField()
    productCategory = djmodels.CharField(max_length=200)
    productPrice = djmodels.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    productTotalQuantity = djmodels.IntegerField(default=20)

    def __str__(self):
        return self.productName

    @classmethod
    def create(cls, **kwargs):
        products = Product.objects.create(
            productURL=kwargs["productURL"],
            productName=kwargs["productName"],
            productDescription=kwargs["productDescription"],
            productCategory=kwargs["productCategory"],
            productPrice=kwargs["productPrice"],
            productTotalQuantity=kwargs["productTotalQuantity"],
        )
        return products


class Cart(djmodels.Model):
    product = djmodels.ForeignKey(Product, on_delete=djmodels.CASCADE)
    quantity = djmodels.PositiveIntegerField(default=0)
    date_added = djmodels.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.productName}"
