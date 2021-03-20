# -*- coding: utf-8 -*-

from tests.utils import BaseTest
from jsonschema import validate
import pytest
import store_schema


class TestStore(BaseTest):

    @classmethod
    def setup_class(cls):
        cls.store_endpoint_url = cls.get_service_url('store')
        cls.store_inventory_endpoint_url = cls.store_endpoint_url + 'inventory/'
        cls.store_order_endpoint_url = cls.store_endpoint_url + 'order/'
        cls.not_existing_order_id = '-1'

    def test_store_get_inventory_status(self):
        response = self._send_get_request_to_endpoint(url_name=self.store_inventory_endpoint_url)
        assert 200 == response.status_code
        validate(response.json(), store_schema.StoreSchema.inventory_schema)

    @pytest.mark.parametrize('order_id', ['invalid', '#@%@$@$@#$'])
    def test_store_place_invalid_order_for_pet(self, order_id):
        response = self._send_post_request_to_endpoint(url_name=self.store_order_endpoint_url,
                                                       request_data={"id": order_id, "petId": 198772, "quantity": 7,
                                                                     "shipDate": "2021-03-18T10:57:11.640Z",
                                                                     "status": "approved", "complete": True})
        assert response.status_code == 400

    @pytest.mark.parametrize('order_status', ['placed', 'approved', 'delivered'])
    @pytest.mark.parametrize('complete_status', [True, False])
    def test_store_place_order_for_pet_with_different_statuses(self, order_status, complete_status):
        response = self._place_random_order_for_pet(order_status, complete_status)
        assert 200 == response.status_code
        validate(response.json(), store_schema.StoreSchema.order_schema)

    def test_store_find_order_by_id(self):
        # Generate Order
        order = self._place_random_order_for_pet('placed', True)
        order_id = str(order.json()['id'])
        assert order.status_code == 200
        # Find order
        response = self._send_get_request_to_endpoint(url_name=self.store_order_endpoint_url + order_id)
        assert 200 == response.status_code
        validate(response.json(), store_schema.StoreSchema.order_schema)

    def test_store_find_order_with_non_existing_id(self):
        response = self._send_get_request_to_endpoint(
            url_name=self.store_order_endpoint_url + self.not_existing_order_id)
        assert response.status_code == 404
        assert response.text == 'Order not found'

    def test_store_find_order_with_invalid_id(self):
        response = self._send_delete_request_to_endpoint(url_name=self.store_order_endpoint_url + '')
        assert response.status_code == 405

    def test_store_delete_order_by_id(self):
        # Generate Order
        make_order = self._place_random_order_for_pet('placed', True)
        order_id = str(make_order.json()['id'])
        assert make_order.status_code == 200
        # Delete order
        deleted_order = self._send_delete_request_to_endpoint(url_name=self.store_order_endpoint_url + order_id)
        assert 200 == deleted_order.status_code
        # Make sure order is deleted
        response = self._send_get_request_to_endpoint(url_name=self.store_order_endpoint_url + order_id)
        assert 404 == response.status_code
        assert response.text == 'Order not found'

    def test_store_delete_order_by_invalid_id(self):
        response = self._send_delete_request_to_endpoint(url_name=self.store_order_endpoint_url + 'a')
        assert response.status_code == 400
