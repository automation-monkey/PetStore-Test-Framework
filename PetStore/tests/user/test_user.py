# -*- coding: utf-8 -*-

from tests.utils import BaseTest
from jsonschema import validate
from user_schema import user_schema


class TestUser(BaseTest):

    @classmethod
    def setup_class(cls):
        cls.user_endpoint_url = cls.get_service_url('user')
        cls.user_endpoint_url_login = cls.user_endpoint_url + 'login'
        cls.user_endpoint_url_logout = cls.user_endpoint_url + 'logout'
        cls.user_endpoint_generate_user_list_url = cls.user_endpoint_url + 'createWithList'
        cls.valid_username = 'theUser'
        cls.valid_password = '12345'
        cls.non_existing_username = 'YouCantFindMe!'

    def test_user_create_new_and_log_in(self):
        # Create user
        created_user = self._generate_a_new_random_user()
        assert created_user.status_code == 200, 'failed to create user'
        # Check user created according to schema
        validate(instance=created_user.json(), schema=user_schema)
        # Check user can login
        user_login = self._login_user(self.valid_username, self.valid_password)
        assert 'Logged in user session:' in user_login.text

    def test_create_user_new_fails_if_request_data_invalid(self):
        response = self._send_post_request_to_endpoint(url_name=self.user_endpoint_url, request_data='invalid body')
        assert response.status_code == 400

    def test_create_user_new_with_list(self):
        num_of_users = 5
        # Generate a list of user dicts
        new_users = self._generate_a_list_of_random_user_dicts(num_of_users)
        # Use list to create users
        response = self._send_post_request_to_endpoint(self.user_endpoint_generate_user_list_url,
                                                       request_data=new_users)
        user_list = response.json()
        assert response.status_code == 200
        # Check all users are created according to schema
        for user in user_list:
            validate(instance=user, schema=user_schema)

    def test_user_login(self):
        response = self._send_get_request_to_endpoint(url_name=self.user_endpoint_url_login,
                                                      request_params={'username': self.valid_username,
                                                                      'password': self.valid_password})
        assert 200 == response.status_code
        assert 'Logged in user session:' in response.text

    def test_user_logout(self):
        response = self._send_get_request_to_endpoint(url_name=self.user_endpoint_url_logout,
                                                      request_params={'username': self.valid_username,
                                                                      'password': self.valid_password})
        assert 200 == response.status_code
        assert response.text == 'User logged out'

    def test_user_get_info_with_valid_username(self):
        # Create User
        created_user = self._generate_a_new_random_user()
        username = created_user.json()['username']
        newly_created_user_info = created_user.json()
        assert created_user.status_code == 200, 'failed to create user'
        # Get user info for the user we just created
        get_user_info = self._send_get_request_to_endpoint(url_name=self.user_endpoint_url + username)
        assert get_user_info.status_code == 200
        assert get_user_info.json() == newly_created_user_info, 'expected response body does not match expected'
        validate(instance=get_user_info.json(), schema=user_schema)

    def test_user_get_info_with_invalid_username(self):
        response = self._send_get_request_to_endpoint(url_name=self.user_endpoint_url)
        assert 405 == response.status_code

    def test_user_get_info_with_non_existing_username(self):
        response = self._send_get_request_to_endpoint(url_name=self.user_endpoint_url + self.non_existing_username)
        assert response.status_code == 404
        assert 'User not found' == response.text

    def test_user_update(self):
        # Create User
        created_user = self._generate_a_new_random_user()
        user_id = created_user.json()['id']
        username = created_user.json()['username']
        assert created_user.status_code == 200, 'failed to create user'

        update_data = {"id": user_id, "username": "theUpdatedUser", "firstName": "John", "lastName": "James",
                       "email": "Updatedjohn@email.com", "password": "12345678", "phone": "12345678", "userStatus": 2}

        updated_user = self._send_put_request_to_endpoint(url_name=self.user_endpoint_url + username,
                                                          request_json=update_data)
        assert updated_user.status_code == 200
        # Check data was updated
        assert update_data == updated_user.json()

    def test_user_update_non_existing_user(self):
        update_data = {"id": '10', "username": "theUpdatedUser", "firstName": "John", "lastName": "James",
                       "email": "Updatedjohn@email.com", "password": "12345678", "phone": "12345678", "userStatus": 2}

        response = self._send_put_request_to_endpoint(url_name=self.user_endpoint_url + self.non_existing_username,
                                                      request_json=update_data)
        assert response.status_code == 404
        assert response.text == 'User not found'

    def test_delete_user(self):
        # Create User
        created_user = self._generate_a_new_random_user()
        username = created_user.json()['username']
        assert created_user.status_code == 200, 'failed to create user'
        # Delete User
        delete_user = self._send_delete_request_to_endpoint(url_name=self.user_endpoint_url + username)
        assert delete_user.status_code == 200, 'failed to delete user'
        # Make sure user is deleted
        verify_deleted = self._send_get_request_to_endpoint(url_name=self.user_endpoint_url + username)
        assert verify_deleted.status_code == 404, 'user was not deleted'
