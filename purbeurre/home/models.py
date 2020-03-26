from django.db import models


class Category(models.Model):
    """ Product Categories """

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nom"
    )

    class Meta:
        verbose_name = "Catégorie"

    def __str__(self):
        return self.name

class Product(models.Model):
    """ Product """

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nom du produit"
    )
    category_id = models.ForeignKey(
        Category,
        related_name='category',
        verbose_name="Catégorie ID",
        on_delete=models.CASCADE
    )

    nutriscore = models.CharField(max_length=1, verbose_name="Nutriscore")
    url = models.URLField(unique=True, verbose_name="URL")
    photo = models.URLField(verbose_name="Photo")
    ingredients = models.URLField(verbose_name="Ingredients", null = True)
    fat_100g = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True
    )
    sugars_100g = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True
    )
    salt_100g = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True
    )
    saturate_fat_100g = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Produit"
