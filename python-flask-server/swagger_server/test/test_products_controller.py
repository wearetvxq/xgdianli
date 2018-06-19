# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.error import Error
from swagger_server.models.product import Product
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestProductsController(BaseTestCase):
    """ ProductsController integration test stubs """

    def test_products_get(self):
        """
        Test case for products_get

        Product Types
        """
        query_string = [('latitude', 1.2),
                        ('longitude', 1.2)]
        response = self.client.open('/v1/products',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
