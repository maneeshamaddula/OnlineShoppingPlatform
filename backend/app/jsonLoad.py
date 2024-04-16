import json
from .models import Product

# you can also keep this inside a view
with open("data.json", encoding="utf-8") as data_file:
    json_data = json.loads(data_file.read())

    for data in json_data:
        products = Product.create(**data)
