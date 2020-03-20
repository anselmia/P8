"""
    This module represent the definition of the object Category.
"""
from models.category import Category
from models.product import Product as Prod


class Favorite:
    """
    Instance of object Favorite.
    """

    # dictionnary to interpret returned object category from database
    from_db_to_obj = {"id": 0, "id_product": 1, "id_substitute": 2}

    def __init__(self, message, substitute_name, id_product, id_substitute):
        """
        Initialization of the Favorite object
        Attributes : substitute's name, product's id and substitute's id
        """
        self.message = message
        self.name = substitute_name
        self.id_product = id_product
        self.id_substitute = id_substitute

    def __str__(self):
        """
        Return the name of the object when converting object to string
        """
        return self.name

    def get_favorite(self, sql):
        """
            Method to get a favorite from the database
            arg : SQL - Global instance of the sql class

            return an instance of a product and a substitute
        """
        product_in_db = sql.select_where("product", ("id", self.id_product))
        substitute_in_db = sql.select_where("product", ("id", self.id_substitute))

        product = Prod.get_obj_from_db_result(self.message, product_in_db[0])
        substitute = Prod.get_obj_from_db_result(self.message, substitute_in_db[0])

        return product, substitute

    @staticmethod
    def add_favorite_substitute(sql, message, category, product, substitute):
        """
        Method to save a favorite in the database
        arg : SQL - Global instance of the sql class
              message - Global instance of the Message object
              category of the product/substitute
              Instance of a product
              Instance of a substitute

        return an instance of the saved Favorite if save performed
        else None
        """
        id_product = ""
        id_category = ""

        # Retrieve the id of the category in the database
        category_from_db = sql.select_first_row_one_attribute_where(
            "category", "id", ("id", product.id_category)
        )
        # if the category was not found in the database
        if category_from_db is None:
            message.not_in_db("category : " + category)
            category = Category(message, category)
            # save the category in the database
            id_category = category.save_in_db(sql)
        else:
            id_category = category_from_db[0]
        # Retrieve the id of the product in the database
        product_from_db = sql.select_first_row_one_attribute_where(
            "product", "id", ("name", product.name)
        )
        # if the category was not found in the database
        if product_from_db is None:
            message.not_in_db("product : " + product.name)
            # save the product in the database
            id_product = product.save_product_in_db(sql, id_category)
        else:
            id_product = product_from_db[0]

        id_substitute = ""
        # Retrieve the id of the substitute in the database
        substitute_from_db = sql.select_first_row_one_attribute_where(
            "product", "id", ("name", substitute.name)
        )
        # if the substitute was not found in the database
        if substitute_from_db is None:
            message.not_in_db("substitute : " + substitute.name)
            # save the substitute in the database
            id_substitute = substitute.save_product_in_db(sql, id_category)
        else:
            id_substitute = substitute_from_db[0]

        # Save the favorite in the database
        substitute_dic = {"id_product": id_product, "id_substitute": id_substitute}
        id_favorite = sql.insert("substitute", **substitute_dic)
        if id_favorite > 0:
            return Favorite(message, substitute.name, id_product, id_substitute)
        else:
            return None

    @staticmethod
    def get_all_favorites(sql, message):
        """
            Method that retrieves favorite from database.
            arg : SQL - Global instance of the sql class
                  message - Global instance of the QPlainTextEdit object
            return a list of Favorite Instance
        """
        message.loading("favorite substitutes", "Database")
        favorite_from_db = sql.select("substitute")

        favorites = []
        # Create a list of Favorite from favorite'row returned from the database
        for favorite in favorite_from_db:
            substitute_name = sql.select_first_row_one_attribute_where(
                "product", "name", ("id", favorite[Favorite.from_db_to_obj["id_substitute"]])
            )
            favorite_instance = Favorite(
                message,
                substitute_name[0],
                favorite[Favorite.from_db_to_obj["id_product"]],
                favorite[Favorite.from_db_to_obj["id_substitute"]],
            )
            favorites.append(favorite_instance)

        if len(favorites) > 0:
            message.done()
        else:
            message.impossible_to_load("favorite substitutes")

        return favorites
