"""This module represent the definition of the object Product."""


class Product:

    propositionslst = []
    substituteslst = []

    def __init__(self, name, img, nutriimg, nutriletter, code, category, nutriscore):
        self.name = name
        self.img = img
        self.nutriimg = nutriimg
        self.nutriletter = nutriletter
        self.code = code
        self.url = "https://fr.openfoodfacts.org/produit/" + self.code
        self.apiurl = "https://fr.openfoodfacts.org/api/v0/produit/" + self.code
        self.category = category
        self.nutriscore = nutriscore

    def create_list(self, lst):
        newlist = []
        for product in lst:
            new_product = Product(product['name'], product['img'], product['url_nutri'],
                           product['nutriletter'], product['code'], product['categorie'],
                           product['nutriscore'])
            newlist.append(new_product)
            return newlist