from django.db import models
from home.models import Product
from django.conf import settings


class Substitute(models.Model):
    """ Favorites """

    product_id = models.ForeignKey(
        Product, related_name="product", on_delete=models.CASCADE
    )
    substitute_id = models.ForeignKey(
        Product, related_name="substitute", on_delete=models.CASCADE
    )

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product_id", "substitute_id", "user_id"],
                name="unique_relation",
            )
        ]
        verbose_name = "Favoris"
        verbose_name_plural = "Favoris"
