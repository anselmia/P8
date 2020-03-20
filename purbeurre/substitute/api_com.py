"""
    This library is uesd to communicate with the OpenFoodFact API
"""

import requests
from .product import Product


class OpenFoodFactsApi:
    """ This library regroup methods to interogate the OpenFoodFact API """

    def get_results_from_search(self, query):
        """ return aliments for a basic query """
        data = self.api_call_results_search(query)
        if data['products']:
            Product.propositionslst = self.clean_datanewtest(data)
            return Product.propositionslst
        else:
            return []
    
    def api_call_results_search(self, query):
        """ simple query call on openfoodfacts api"""
        url = "https://fr.openfoodfacts.org/cgi/search.pl?"
        params = {
            'action'       : 'process',
            'search_terms' : query,
            'search_simple': 1,
            'json'         : 1,
        }
        response = requests.get(url=url, params=params)
        data = response.json()
        return data

    @staticmethod
    def fetch_categories_data_api(Message):
        """
            Method allowing the program to search categories' data online
            with the Open Food Facts API.
            Exceptions like HTTP, TimeOut, Connexion and other will be catched
            Return a list of category as dictionnary
        """
        category_names = []
        try:
            # Recover data from Open Food Facts URL API with request get.
            response = requests.get("https://fr.openfoodfacts.org/categories.json", timeout=3)
            # raise an exception if the request was unsuccessful
            response.raise_for_status()
            # Save the json data in a variable.
            json_data_file = response.json()
            # Get only the data needed: data besides the one in the "tags"
            # list are irrelevant here.
            # Input are filtered to avoid getting ":" in the name attribute or empty name
            category_names = [
                category.get("name")
                for category in json_data_file.get("tags")
                if (":" not in category.get("name") and len(category.get("name")) > 1)
            ]

        except requests.exceptions.HTTPError:
            Message.http_error()
        except requests.exceptions.ConnectionError:
            Message.connexion_error()
        except requests.exceptions.Timeout:
            Message.timeout()
        except requests.exceptions.RequestException:
            Message.other_api_exception()

        finally:
            return category_names

    @staticmethod
    def fetch_products_data_api(Message, category, filtered_tags):
        """
            Method allowing the program to search product' data online
            with the Open Food Facts API.
            Exceptions like HTTP, TimeOut, Connexion and other will be catched
            Return a list of products as dictionnary
            Arg : category of product and tags to filter in product tags
        """
        products = []
        # Properties to filter the product queries
        filters = {
            "action": "process",
            "tagtype_0": "categories",  # which subject is selected (categories)
            "tag_contains_0": "contains",  # contains or not
            "tag_0": category,  # parameters to choose
            "sort_by": "unique_scans_n",
            "countries": "France",
            "page_size": 1000,
            "page": 1,
            "json": 1,
        }

        try:
            # Recover data from Open Food Facts URL API with request get.
            response = requests.get("https://fr.openfoodfacts.org/cgi/search.pl", params=filters)
            # Save the json data in a variable.
            json_data_file = response.json()
            # Get only the data needed: data besides the one in the "products"
            data_products = json_data_file.get("products")

            # Create a list of product as dictionary from the dictionary of
            # products data_products
            # {key: product[key] for key in product.keys() & {i: None for i in filtered_tags}}
            # --> create a product dictionary filtering the keys using filtered_tags
            # all(item in list(product.keys()) for item in filtered_tags)
            # --> Filtered the product to match all keys present in filtered_tags
            products = [
                {key: product[key] for key in product.keys() & {i: None for i in filtered_tags}}
                for product in data_products
                if all(item in list(product.keys()) for item in filtered_tags)
            ]

        except requests.exceptions.HTTPError:
            Message.http_error()
        except requests.exceptions.ConnectionError:
            Message.connexion_error()
        except requests.exceptions.Timeout:
            Message.timeout()
        except requests.exceptions.RequestException:
            Message.other_api_exception()

        finally:
            return products

    def clean_datanewtest(self, data):
        """return the best aliments by checking completness and already entred aliments"""
        newdata = []
        i = 0
        fulltry = True
        nutry = True
        nametry = True
        finaltry = True
        if data['count'] < 20:
            maxresult = data['count']
        else:
            maxresult = 20

        while len(newdata) <= 5 and finaltry is not False:
            aliment = {'product_name_fr': 'default name',
                       'img'            : 'default img', 'nutriscore': 'nutri', 'nutriletter': '?',
                       'code'           : '0', 'url_nutri': 'default nutriimg',
                       'categorie'      : 'en:cocoa-and-hazelnuts-spreads', 'info': [], 'stores'
                                        : 'no stores', 'nova_groups': 'nova', 'novascore': 'nova'}

            if i == maxresult and fulltry:
                i = 0
                fulltry = False
            elif i == maxresult and nutry:
                i = 0
                nutry = False
            elif i == maxresult and nametry:
                i = 0
                nametry = False
            elif i == maxresult and finaltry:
                i = 0
                finaltry = False

            if not newdata:
                if fulltry:
                    result = OFFA.get_aliment_dict_hard(data, aliment, i)
                    if result is not None:
                        newdata.append(result)
                    i += 1
                elif nametry:
                    if 'product_name_fr' in data['products'][i]:
                        result = OFFA.get_aliment_dict_hard(data, aliment, i)
                        if result is not None:
                            newdata.append(result)
                    i += 1
                elif finaltry:
                    if 'product_name_it' in data['products'][i] or 'product_name_en' in data[
                        'products'][i] or 'product_name' in data['products'][i]:
                        newdata.append(OFFA.get_aliment_dict(data, aliment, i))
                    i += 1
            else:
                if fulltry:
                    if 'product_name_fr' in data['products'][i]:
                        if data['products'][i]['product_name_fr'] is not '':
                            if not any(
                                    d['product_name_fr'] == data['products'][i]['product_name_fr']
                                    for d in newdata):
                                result = OFFA.get_aliment_dict_hard(data, aliment, i)
                                if result is not None:
                                    newdata.append(result)
                    i += 1
                elif nametry:
                    if 'product_name_fr' in data['products'][i]:
                        if data['products'][i]['product_name_fr'] is not '':
                            result = OFFA.get_aliment_dict_hard(data, aliment, i)
                            if result is not None:
                                newdata.append(result)
                    i += 1
                elif finaltry:
                    if 'product_name_it' in data['products'][i] or 'product_name_en' in data[
                        'products'][i] or 'product_name' in data['products'][i]:
                        result = OFFA.get_aliment_dict(data, aliment, i)
                        if result is not None:
                            newdata.append(result)
                    i += 1
        return newdata

    def select_categorie(self, data):
        """return the best category"""
        referencenumber = 1000000
        finalcategory = ''
        lstofuselesscategory = ["en:plant-based-foods-and-beverages", "en:plant-based-foods",
                                "en:snacks", "en:beverages", "en:sweet-snacks", "en:dairies",
                                "en:meats", "en:non-alcoholic-beverages", "en:meals",
                                "en:fruits-and-vegetables-based-foods",
                                "en:cereals-and-potatoes", "en:fermented-foods",
                                "en:fermented-milk-products", "en:spreads", "en:biscuits-and-cakes",
                                "en:groceries", "en:prepared-meats",
                                "en:cereals-and-their-products", "en:cheeses", "en:breakfasts",
                                "en:plant-based-beverages", "en:fruits-based-foods", "en:desserts",
                                "en:sauces", "en:sweet-spreads", "en:frozen-foods",
                                "en:canned-foods", "en:vegetables-based-foods", "en:seafood",
                                "en:confectioneries", "en:alcoholic-beverages",
                                "en:plant-based-spreads", "en:biscuits", "en:fruit-based-beverages",
                                "en:chocolates", "en:fishes", "en:salty-snacks", "en:fats",
                                "en:juices-and-nectars", "en:sweetened-beverages", "en:condiments",
                                "en:meat-based-products", "en:yogurts", "en:cakes",
                                "en:fruit-juices-and-nectars", "en:french-cheeses",
                                "en:fresh-foods", "en:poultries", "en:appetizers",
                                "en:fruit-preserves", "en:breads", "en:dried-products",
                                "en:fruit-juices", "en:jams", "en:meals-with-meat",
                                "en:cow-cheeses", "en:legumes-and-their-products",
                                "en:canned-plant-based-foods", "en:salted-spreads",
                                "en:unsweetened-beverages", "en:sweeteners",
                                "en:nuts-and-their-products", "en:fruit-jams", "en:seeds",
                                "en:hot-beverages", "en:chickens", "en:farming-products",
                                "en:vegetable-fats", "en:pastas", "en:wines",
                                "en:breakfast-cereals", "en:milks", "en:hams", "en:legumes",
                                "en:vegetable-oils", "en:chips-and-fries", "en:carbonated-drinks"]
        i = 0
        newlstdata = []
        while i < len(data):
            if data[i] != '':
                newlstdata.append(data[i])
            i += 1
        for category in newlstdata:
            if category not in lstofuselesscategory:
                url = "https://world.openfoodfacts.org/category/" + category + ".json"
                response = requests.get(url)
                newdata = response.json()
                if newdata['count'] < referencenumber:
                    referencenumber = newdata['count']
                    finalcategory = category
        return finalcategory

    def get_results_from_category(self, categorie, nutriscore):
        """return best aliments with the best category """
        data = self.api_call_results_category(categorie, nutriscore)
        Product.substituteslst = self.clean_data_category(data)
        return Product.substituteslst

    def get_results_from_category_nova(self, categorie, novascore):
        """return best aliments with the best category """
        data = self.api_call_results_category_nova(categorie, novascore)
        Product.substituteslst = self.clean_data_category(data)
        return Product.substituteslst

    def get_aliment_dict_hard(self, data, aliment, i):
        """return only full documented aliments"""
        if all(name in data['products'][i].keys() for name in ('product_name_fr', 'image_url',
                                                               'image_nutrition_url',
                                                               'nutrition_grades', 'id',
                                                               'categories_tags', 'stores_tags',
                                                               'nova_groups')):
            aliment['product_name_fr'] = data['products'][i]['product_name_fr']
            aliment['img'] = data['products'][i]['image_url']
            aliment['url_nutri'] = data['products'][i]['image_nutrition_url']
            aliment['nutriletter'] = data['products'][i]['nutrition_grades'].upper()
            aliment['nova_groups'] = data['products'][i]['nova_groups']
            aliment['code'] = data['products'][i]['id']
            aliment['categorie'] = data['products'][i]['categories_tags']
            if data['products'][i]['stores_tags'] != '':
                aliment['stores'] = data['products'][i]['stores_tags']
            aliment['nutriscore'] += aliment['nutriletter'].lower()
            aliment['novascore'] += str(aliment['nova_groups'])
            aliment['url'] = "https://fr.openfoodfacts.org/produit/" + aliment['code']
            aliment['info'].append(aliment['categorie'])
            aliment['info'].append(aliment['nutriletter'])
            return aliment

    def api_call_results_category(self, category, previousnutri):
        """create query for better nutriscore"""
        dictofbestresulsts = {'products': [], 'count': 0}
        lstofnutri = ['A', 'B', 'C', 'D', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E',
                      'E', 'E', 'E', 'E']
        id = 0
        while len(dictofbestresulsts['products']) < 6 and id < 6:
            url = "https://world.openfoodfacts.org/cgi/search.pl?"
            nutriscore = lstofnutri[id]
            params = {
                'tagtype_0'     : 'categories',
                'tag_contains_0': 'contains',
                'tag_0'         : category,
                'tagtype_1'     : 'nutrition_grades',
                'tag_contains_1': 'contains',
                'tag_1'         : nutriscore,
                'sort_by'       : 'completeness',
                'page_size'     : '20',
                'axis_x'        : 'energy',
                'axis_y'        : 'product_n',
                'action'        : 'process',
                'json'          : '1',
            }
            response = requests.get(url=url, params=params)
            data = response.json()
            i = 0
            for product in data['products']:
                if 'product_name_fr' in data['products'][i]:
                    if not any(d['product_name_fr'] == data['products'][i]['product_name_fr']
                               for d in dictofbestresulsts['products']):
                        dictofbestresulsts['products'].append(product)
                        dictofbestresulsts['count'] += 1
                i += 1
            id += 1
        return dictofbestresulsts

    def api_call_results_category_nova(self, category, previousnutri):
        """create query for better nutriscore"""
        dictofbestresulsts = {'products': [], 'count': 0}
        lstofnutri = ['1', '2', '3', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4',
                      '4', '4', '4', '4']
        id = 0
        while len(dictofbestresulsts['products']) < 6 and id < 6:
            url = "https://world.openfoodfacts.org/cgi/search.pl?"
            nutriscore = lstofnutri[id]
            params = {
                'tagtype_0'     : 'categories',
                'tag_contains_0': 'contains',
                'tag_0'         : category,
                'tagtype_1'     : 'nova_groups',
                'tag_contains_1': 'contains',
                'tag_1'         : nutriscore,
                'sort_by'       : 'completeness',
                'page_size'     : '20',
                'axis_x'        : 'energy',
                'axis_y'        : 'product_n',
                'action'        : 'process',
                'json'          : '1',
            }
            response = requests.get(url=url, params=params)
            data = response.json()
            i = 0
            for product in data['products']:
                if 'product_name_fr' in data['products'][i]:
                    if not any(d['product_name_fr'] == data['products'][i]['product_name_fr']
                               for d in dictofbestresulsts['products']):
                        dictofbestresulsts['products'].append(product)
                        dictofbestresulsts['count'] += 1
                i += 1
            id += 1
        return dictofbestresulsts

    def clean_data_category(self, data):
        """return a cleaned aliment"""
        newdata = []
        i = 0
        if len(data['products']) < 6:
            maxresult = len(data['products'])
        else:
            maxresult = 5
        while len(newdata) <= maxresult - 1:
            aliment = {'product_name_fr': 'default name',
                       'img'            : 'default img', 'nutriscore': 'nutri', 'nutriletter': '?',
                       'code'           : '0', 'url_nutri': 'default nutriimg',
                       'categorie'      : 'en:cocoa-and-hazelnuts-spreads', 'info': [], 'stores'
                                        : 'no stores', 'nova_groups': 'nova', 'novascore': 'nova'}
            newdata.append(a.get_aliment_dict(data, aliment, i))
            i += 1
        return newdata

OFFA = OpenFoodFactsApi()