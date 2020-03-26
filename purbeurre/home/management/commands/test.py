from home.models import Product, Category
from django.core.management.base import BaseCommand

import requests
from django.db import IntegrityError

cats = {
    "1":"barres-chocolatees",
    "2":"boissons-avec-sucre-ajoute",
    "3":"desserts-glaces",
    "4":"desserts-lactes",
    "5":"chocolats",
    "6":"viennoiseries",
    "7":"bonbons",
    "8":"confiseries-chocolatees",
    "9":"pates-a-tartiner",
    "10":"laits-aromatises",
    "11":"nectars-d-orange",
    "12":"nectars-de-pomme",
    "13":"jus-de-pomme",
    "14":"jus-d-orange",
    "15":"jus-de-fruits-a-base-de-concentre",
    "16":"pizzas",
    "17":"pizzas-surgelees",
    "18":"plats-prepares-frais",
    "19":"box",
    "20":"pates-instantanees",
    "21":"lasagnes-preparees",
    "22":"plats-au-boeuf",
    "23":"plats-a-la-volaille",
    "24":"jus-multifruits",
    "25":"desserts-au-chocolat"
    }

class Command(BaseCommand):
    def handle(self, **options):
        # now do the things that you want with your models here
    # cycle : saves category -> loops through all products of the said category
        for number in cats:
            category = cats[number]
            try:
                Category.objects.create(name=category)
            except:
                pass

            url = (
                f"https://fr.openfoodfacts.org/cgi/search.pl?"
                f"action=process&tagtype_0=categories&"
                f"tag_contains_0=contains&tag_0={category}&"
                f"sort_by=unique_scans_n&page_size=500&json=1"
            )
            response = requests.get(url)

            data = response.json()

            for product in data["products"]:                
                try:
                    Product.objects.create(
                        name=product.get("product_name_fr"),
                        category_id=Category.objects.get(
                            name=category
                        ),
                        nutriscore=product.get("nutriscore_grade"),
                        photo=product.get("image_url", "ND"),
                        url=product.get("url", "ND"),
                        ingredients=product.get('image_ingredients_url','ND'),
                        # nutriments
                        fat_100g=product["nutriments"].get(
                            "fat_100g", "ND"
                        ),
                        saturate_fat_100g=product["nutriments"].get(
                            "saturated-fat_100g", "ND"
                        ),
                        salt_100g=product["nutriments"].get(
                            "salt_100g", "ND"
                        ),
                        sugars_100g=product["nutriments"].get(
                            "sugars_100g", "ND"
                        ),
                    )
                except:
                    print("que")

                #try:
                #    t = Product.objects.get(name=product.get("product_name_fr"))
                #    t.ingredients = product.get('image_ingredients_url','ND')
                #    t.save()
                #except:
                #    pass
                