# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.activities import Activities
from swagger_server.models.error import Error
from swagger_server.models.profile import Profile
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestUserController(BaseTestCase):
    """ UserController integration test stubs """

    def test_history_get(self):
        """
        Test case for history_get

        User Activity
        """
        query_string = [('offset', 56),
                        ('limit', 56)]
        response = self.client.open('/v1/history',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_me_get(self):
        """
        Test case for me_get

        User Profile
        """
        response = self.client.open('/v1/me',
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
