# -*- coding: utf-8 -*-

import pytest
from jsonschema import validate
from tests.utils import BaseTest
from pet_schema import pet_schema


class TestPet(BaseTest):

    @classmethod
    def setup_class(cls):
        cls.pet_endpoint_url = cls.get_service_url('pet')
        cls.find_pet_by_status_url = cls.pet_endpoint_url + 'findByStatus'
        cls.find_pet_by_tag_url = cls.pet_endpoint_url + 'findByTags'
        cls.upload_image_url = cls.pet_endpoint_url + 'uploadImage'
        cls.invalid_pet_id = 'invalid_pet'
        cls.non_existing_pet_id = '11111111'

    def test_pet_add_new(self):
        response = self._generate_a_new_random_pet()
        assert response.status_code == 200
        validate(response.json(), pet_schema)

    @pytest.mark.parametrize('status', ['available', 'pending', 'sold'])
    def test_pet_find_by_status(self, status):
        response = self._send_get_request_to_endpoint(url_name=self.find_pet_by_status_url,
                                                      request_params={'status': status})
        pets = response.json()
        assert response.status_code == 200
        for item in pets:
            assert status in item['status']

    def test_pet_find_by_tags(self):
        response = self._send_get_request_to_endpoint(url_name=self.find_pet_by_tag_url,
                                                      request_params={'tags': 'string'})
        pets = response.json()
        assert response.status_code == 200
        for item in pets:
            assert 'string' in item['tags'][0]['name']

    def test_pet_find_by_id(self):
        # Create a pet
        created_pet = self._generate_a_new_random_pet()
        pet_id = str(created_pet.json()['id'])
        assert created_pet.status_code == 200
        # Find the pet
        find_pet_response = self._send_get_request_to_endpoint(url_name=self.pet_endpoint_url + pet_id)
        assert find_pet_response.status_code == 200
        assert find_pet_response.json()['id'] == int(pet_id)

    def test_pet_find_with_invalid_id(self):
        response = self._send_get_request_to_endpoint(url_name=self.pet_endpoint_url + self.invalid_pet_id)
        assert response.status_code == 400

    def test_pet_find_with_non_existing_id(self):
        response = self._send_get_request_to_endpoint(url_name=self.pet_endpoint_url + self.non_existing_pet_id)
        assert response.status_code == 404
        assert response.text == 'Pet not found'

    def test_pet_update_pet_data_using_form(self):
        # Create a pet
        created_pet = self._generate_a_new_random_pet()
        pet_id = str(created_pet.json()['id'])
        response = self._send_post_request_to_endpoint(url_name=self.pet_endpoint_url+pet_id+'?name=rat')
        assert response.status_code == 200

    def test_pet_update_pet_data_using_invalid_form(self):
        # Create a pet
        created_pet = self._generate_a_new_random_pet()
        pet_id = str(created_pet.json()['id'])
        response = self._send_post_request_to_endpoint(url_name=self.pet_endpoint_url + pet_id,
                                                       request_data={'status': 'available'})
        assert response.status_code == 400
        assert response.text == 'No Name provided. Try again?'

    def test_pet_delete_pet(self):
        # Create a pet
        created_pet = self._generate_a_new_random_pet()
        pet_id = str(created_pet.json()['id'])
        assert created_pet.status_code == 200
        # Delete the pet
        delete_pet_response = self._send_delete_request_to_endpoint(url_name=self.pet_endpoint_url + pet_id)
        assert delete_pet_response.status_code == 200
        assert delete_pet_response.text == 'Pet deleted'
        # Find the pet
        find_pet_response = self._send_get_request_to_endpoint(url_name=self.pet_endpoint_url + pet_id)
        assert find_pet_response.status_code == 404
        assert find_pet_response.text == 'Pet not found'
