"""
    This module represent the definition of the object Category.
"""
from lib.api_com import OpenFoodFactsApi as api


class Category:
    """
    Instance of object Category.
    initilaze with the attribute name.
    """

    # dictionnary to interpret returned object category from database
    # object attribute : DataBase Column Number
    from_db_to_obj = {"id": 0, "name": 1}

    def __init__(self, message, name):
        """
        Initialization of the Category object
        Attributes : name
        """
        self.name = name
        self.message = message

    def __str__(self):
        """
        Return the name of the object when converting object to string
        """
        return self.name

    def save_in_db(self, sql):
        """
        Method to save the object in the database
        arg : SQL - Global instance of the sql class

        return the id of the inserted row in the database
        """
        return sql.insert(
            "category", **{key: self.__dict__[key] for key in self.__dict__ if key != "message"}
        )

    @staticmethod
    def select_from_db(sql, message):
        """
        Method that retrieves categories in the database
        arg : SQL - Global instance of the sql class
              message - Global instance of the text class

        return a list of Category object
        """
        message.loading("category", "DataBase")
        database_categories = sql.select("category")

        categories = []
        for category in database_categories:
            cat = Category(message, category[Category.from_db_to_obj["name"]])
            categories.append(cat)

        if len(categories) > 0:
            message.done()
        else:
            message.load_instead("category")

        return categories

    @staticmethod
    def select_from_api(message):
        """
        Method that retrieves categories in the API
              message - Global instance of the text class

        return a list of Category object
        """
        message.loading("category", "API")
        api_categories = api.fetch_categories_data_api(message)

        categories = []
        for category in api_categories:
            cat = Category(message, category)
            categories.append(cat)

        if len(categories) > 0:
            message.done()
        else:
            message.impossible_to_load("categories")

        return categories

    @staticmethod
    def get_name_from_id(sql, id_category):
        """
        Method that retrieves a category's name given it's ID
        arg : sql - Global instance of SQL Class
              id_category
        return th name of the category (string)
        """

        category_name = sql.select_first_row_one_attribute_where(
            "category", "name", ("id", id_category)
        )

        if category_name is not None:
            return category_name[0]
        else:
            return category_name
