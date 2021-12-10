from tests.test_main import BaseTestCase
from flask import json

from flask import request, session


class ProductsViewsTests(BaseTestCase):
    def setUp(self):
        username = "test"
        password = "123"
        self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def tearDown(self):
        username = "test"
        password = "123"
        self.client.get('/logout', follow_redirects=True)

    def test_create_product(self):
        name = " kefir"
        units = "ea."
        quantity = 2
        category = "milk product"
        response = self.client.put('/api/products', data=json.dumps({'name': name, 'units': units, 'quantity': quantity,
                                                                     "category": category}),
                                    content_type='application/json',)
        self.assert_status(response, 200, message="OK")

    def test_get_products(self):
        name = " kefir"
        units = "ea."
        quantity = 2
        category = "milk product"
        response = self.client.get('/api/products')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data["data"][0]["name"], name)
        self.assert_status(response, 200, message="OK")