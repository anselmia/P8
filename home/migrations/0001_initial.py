# Generated by Django 3.0.4 on 2020-03-25 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, unique=True, verbose_name="Nom"),
                ),
            ],
            options={"verbose_name": "Catégorie",},
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Nom du produit"
                    ),
                ),
                (
                    "nutriscore",
                    models.CharField(max_length=1, verbose_name="Nutriscore"),
                ),
                ("url", models.URLField(unique=True, verbose_name="URL")),
                ("photo", models.URLField(verbose_name="Photo")),
                ("ingredients", models.URLField(null=True, verbose_name="Ingredients")),
                (
                    "fat_100g",
                    models.DecimalField(decimal_places=2, max_digits=4, null=True),
                ),
                (
                    "sugars_100g",
                    models.DecimalField(decimal_places=2, max_digits=4, null=True),
                ),
                (
                    "salt_100g",
                    models.DecimalField(decimal_places=2, max_digits=4, null=True),
                ),
                (
                    "saturate_fat_100g",
                    models.DecimalField(decimal_places=2, max_digits=4, null=True),
                ),
                (
                    "category_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="category",
                        to="home.Category",
                        verbose_name="Catégorie ID",
                    ),
                ),
            ],
            options={"verbose_name": "Produit",},
        ),
    ]
