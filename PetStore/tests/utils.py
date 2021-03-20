from random import randint
import random
import requests
import json
from tests.config import DefaultConfig
import re


class BaseTest:

    config = DefaultConfig()
    base_url = config.URLS.get('base_url')
    pet_url = config.URLS.get('pet')
    user_url = config.URLS.get('user')
    login_user_url = config.URLS.get('user') + 'login'
    store_url = config.URLS.get('store') + 'order'

    @classmethod
    def get_service_url(cls, service_name):
        return cls.config.URLS.get(service_name)

    @classmethod
    def _send_get_request_to_endpoint(cls, url_name=None, request_headers=None, request_params=None,
                                      request_cookies=None):
        request_url = '{}'.format(url_name)
        response = requests.get(url=request_url, headers=request_headers, params=request_params,
                                cookies=request_cookies)
        print('Get request sent to {}'.format(request_url))
        print('Request headers {}'.format(request_headers))
        print('Content of the request {}'.format(response.content))
        print('Status code of the request {}'.format(response.status_code))
        print('*' * 100)
        return response

    @classmethod
    def _send_post_request_to_endpoint(cls, url_name=None, request_headers=None, request_cookies=None,
                                       request_data=None, is_json=True):
        request_url = '{}'.format(url_name)

        if is_json:
            if not request_headers:
                request_headers = {}
            request_headers['Content-Type'] = 'application/json'

            request_data = json.dumps(request_data)

        response = requests.post(request_url, headers=request_headers, cookies=request_cookies, data=request_data)
        print('Post request sent to {}'.format(request_url))
        print('Request headers {}'.format(request_headers))
        print('Request data {}'.format(request_data))
        print('Content of the request {}'.format(response.content))
        print('Status code of the request {}'.format(response.status_code))
        print('*' * 100)
        return response

    @classmethod
    def _send_delete_request_to_endpoint(cls, url_name=None, request_headers=None,
                                         request_cookies=None, request_data=None):
        request_url = '{}'.format(url_name)
        response = requests.delete(request_url, headers=request_headers, cookies=request_cookies, data=request_data)
        print('Delete request sent to {}'.format(request_url))
        print('Request headers {}'.format(request_headers))
        print('Request data {}'.format(request_data))
        print('Content of the request {}'.format(response.content))
        print('Status code of the request {}'.format(response.status_code))
        print('*' * 100)
        return response

    @classmethod
    def _send_put_request_to_endpoint(cls, url_name=None, request_headers=None, request_cookies=None,
                                      request_data=None, request_json=None):
        request_url = '{}'.format(url_name)
        response = requests.put(url=request_url, headers=request_headers, cookies=request_cookies, data=request_data,
                                json=request_json)
        print('Put request sent to {}'.format(request_url))
        print('Request headers {}'.format(request_headers))
        print('Request data {}'.format(request_data))
        print('Request json {}'.format(request_json))
        print('Content of the request {}'.format(response.content))
        print('Status code of the request {}'.format(response.status_code))
        print('*' * 100)
        return response

    @classmethod
    def _place_random_order_for_pet(cls, order_status, complete_status):
        response = cls._send_post_request_to_endpoint(url_name=cls.store_url,
                                                      request_data={
                                                          "id": randint(1, 1000),
                                                          "petId": randint(100000, 200000),
                                                          "quantity": randint(1, 100),
                                                          "shipDate": "2021-03-17T20:52:38.559Z",
                                                          "status": order_status,
                                                          "complete": complete_status
                                                      })
        return response

    @classmethod
    def _generate_a_new_random_pet(cls):
        animals = ['doggy', 'kittie', 'fishy']
        categories = ['dogs', 'cats', 'fish']
        status = ['available', 'pending', 'sold']
        response = cls._send_post_request_to_endpoint(url_name=cls.pet_url,
                                                      request_data={
                                                          "id": randint(1, 1000),
                                                          "name": random.choice(animals),
                                                          "category": {"id": randint(1, 1000),
                                                                       "name": random.choice(categories)},
                                                          "photoUrls": ["string"],
                                                          "tags": [{"id": randint(1, 1000), "name": "string"}],
                                                          "status": random.choice(status)})
        return response

    @classmethod
    def _generate_a_new_random_user(cls):
        rand_id = randint(1, 1000)
        response = cls._send_post_request_to_endpoint(url_name=cls.user_url,
                                                      request_data={
                                                          "id": rand_id, "username": "theUser" + str(rand_id),
                                                          "firstName": "James", "lastName": "James",
                                                          "email": "john@email.com", "password": 12345,
                                                          "phone": 12345, "userStatus": 1})
        return response

    @classmethod
    def _generate_a_list_of_random_user_dicts(cls, num_of_users):
        user_list = []
        while num_of_users > 0:
            request_data = {
                "id": randint(1, 1000), "username": "theUser" + str(randint(1, 1000)), "firstName": "James",
                "lastName": "James", "email": "john@email.com", "password": 12345, "phone": 12345, "userStatus": 1}
            user_list.append(request_data)
            num_of_users = num_of_users - 1
        return user_list

    @classmethod
    def _login_user(cls, username, password):
        response = cls._send_get_request_to_endpoint(url_name=cls.login_user_url,
                                                     request_params={'username': username, 'password': password})
        assert 200 == response.status_code, 'failed to login user'
        return response

    @classmethod
    def _get_user_session(cls, username, password):
        raw_session = cls._login_user(username, password).text
        session = re.search('\\d+', raw_session)
        session = session.group(0)
        return session
