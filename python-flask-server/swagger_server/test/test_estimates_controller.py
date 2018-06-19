# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.error import Error
from swagger_server.models.price_estimate import PriceEstimate
from swagger_server.models.product import Product
java.util.UUID
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestEstimatesController(BaseTestCase):
    """ EstimatesController integration test stubs """

    def test_estimates_price_get(self):
        """
        Test case for estimates_price_get

        Price Estimates
        """
        query_string = [('start_latitude', 1.2),
                        ('start_longitude', 1.2),
                        ('end_latitude', 1.2),
                        ('end_longitude', 1.2)]
        response = self.client.open('/v1/estimates/price',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_estimates_time_get(self):
        """
        Test case for estimates_time_get

        Time Estimates
        """
        query_string = [('start_latitude', 1.2),
                        ('start_longitude', 1.2),
                        ('customer_uuid', UUID()),
                        ('product_id', 'product_id_example')]
        response = self.client.open('/v1/estimates/time',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
