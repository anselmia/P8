from home.models import Product, Category
import requests


def update_product():
    products = Product.objects.all()
    for product in products:
        product_id = product.url.split("/")[4]

        url = f"https://fr.openfoodfacts.org/api/v0/product/{product_id}&json=1"
        response = requests.get(url)
        data = response.json()

        if data["status_verbose"] == "product found":
            if not all(
                k in data["product"]
                for k in (
                    "product_name_fr",
                    "nutriscore_grade",
                    "categories",
                    "image_url",
                )
            ):
                product.delete()
                continue
            if not all(
                k in data["product"].get("nutriments")
                for k in ("fat_100g", "saturated-fat_100g", "sugars_100g", "salt_100g")
            ):
                product.delete()
                continue
            try:
                category = data["product"].get("categories")
                category_in_product = product.category_id.name
                if not category_in_product in category:
                    categories = category.split(",")
                    categories = [cat for cat in categories if "en:" not in cat]
                    category_in_product = categories[len(categories) - 1]
                    if not Category.objects.filter(name=category_in_product).exists():
                        Category.objects.create(name=category_in_product)
            except:
                continue

            try:
                product.name = data["product"].get("product_name_fr")
                product.category_id = Category.objects.get(name=category_in_product)
                product.nutriscore = data["product"].get("nutriscore_grade")
                product.photo = data["product"].get("image_url", "ND")
                product.ingredients = data["product"].get("image_ingredients_url", "ND")
                product.fat_100g = data["product"]["nutriments"].get("fat_100g", "ND")
                product.saturate_fat_100g = data["product"]["nutriments"].get(
                    "saturated-fat_100g", "ND"
                )
                product.salt_100g = data["product"]["nutriments"].get("salt_100g", "ND")
                product.sugars_100g = data["product"]["nutriments"].get(
                    "sugars_100g", "ND"
                )

                product.save()
            except Exception as a:
                pass
