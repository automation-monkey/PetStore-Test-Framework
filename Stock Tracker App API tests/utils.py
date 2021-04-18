import json
import requests


class BaseTest:

    BASE_URL = 'http://localhost:8080/api/'

    @classmethod
    def _get_request(cls, url=None, headers=None, params=None):
        request_url = '{}'.format(url)
        response = requests.get(url=request_url,
                                headers=headers,
                                params=params)
        print('Get request sent to {}'.format(request_url))
        print('Request headers {}'.format(headers))
        print('Content of the request {}'.format(response.content))
        print('Status code of the request {}'.format(response.status_code))
        print('*' * 100)
        return response

    @classmethod
    def _post_request(cls, url=None, headers=None, cookies=None, data=None):
        request_url = '{}'.format(url)
        response = requests.post(url, headers=headers, cookies=cookies, data=data)
        print('Post request sent to {}'.format(url))
        print('Request headers {}'.format(headers))
        print('Request data {}'.format(data))
        print('Content of the request {}'.format(response.content))
        print('Status code of the request {}'.format(response.status_code))
        print('*' * 100)
        return response

    @classmethod
    def _delete_request(cls, url=None, headers=None, cookies=None, data=None):
        request_url = '{}'.format(url)
        response = requests.delete(request_url, headers=headers, cookies=cookies, data=data)
        print('Delete request sent to {}'.format(request_url))
        print('Request headers {}'.format(headers))
        print('Request data {}'.format(data))
        print('Content of the request {}'.format(response.content))
        print('Status code of the request {}'.format(response.status_code))
        print('*' * 100)
        return response

    @classmethod
    def _put_request(cls, url=None, headers=None, cookies=None, data=None):
        request_url = '{}'.format(url)
        response = requests.delete(request_url, headers=headers, cookies=cookies, data=data)
        print('Put request sent to {}'.format(request_url))
        print('Request headers {}'.format(headers))
        print('Request data {}'.format(data))
        print('Content of the request {}'.format(response.content))
        print('Status code of the request {}'.format(response.status_code))
        print('*' * 100)
        return response

    @classmethod
    def _get_user_portfolio(cls):
        r = cls._get_request(url=cls.BASE_URL+'portfolio')
        portfolio = json.loads(r.content)
        return portfolio
