from django.test import TestCase, TransactionTestCase
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.management import call_command
# from core.management.commands.initdb import Command
from .models import Product
# Create your tests here.

class TestCommand(TransactionTestCase):

    # Test custom command

    def test_initdb(self):

        call_command("fetch_api_data", "categories", "1", test=True)
        print('ok')
        print(Product.objects.all().order_by('product_name'))
        assert Product.objects.get(product_code='123456789').product_name ==  "product1"