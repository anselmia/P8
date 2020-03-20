from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    """
    Instance of object Product.
    """

    name = models.CharField(max_length=100)
    id_category = models.ForeignKey('Category', on_delete=models.CASCADE, default='1')
    url = models.URLField()
    url_img = models.TextField()
    url_nutri = models.TextField()
    stores = models.TextField()
    nutriscore = models.CharField(max_length=1)
    novascore = models.CharField(max_length=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='1')

    # List of attributes to show from object
    attributes = [
        "name",
        "brands",
        "url",
        "nutrition_grade",
        "fat",
        "saturated_fat",
        "sugar",
        "salt",
    ]

    # dictionnary to interpret returned object product from database
    # object attribute : DataBase Column Number
    from_db_to_obj = {
        "id": 0,
        "name": 1,
        "brands": 2,
        "url": 3,
        "nutrition_grade": 4,
        "fat": 5,
        "saturated_fat": 6,
        "sugar": 7,
        "salt": 8,
        "id_category": 9,
    }
        

    def __str__(self):
        """
        Return the name of the object when converting object to string
        """
        return self.name

class Favorite(models.Model):
    """
    Instance of object Favorite.
    """
    name = models.CharField(max_length=100)
    id_product = models.CharField(max_length=6)
    id_substitute = models.CharField(max_length=6)
    # dictionnary to interpret returned object category from database
    from_db_to_obj = {"id": 0, "id_product": 1, "id_substitute": 2}

class Category(models.Model):
    """
    Instance of object Category.
    initilaze with the attribute name.
    """

    # dictionnary to interpret returned object category from database
    # object attribute : DataBase Column Number
    from_db_to_obj = {"id": 0, "name": 1}

    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Return the name of the object when converting object to string
        """
        return self.name