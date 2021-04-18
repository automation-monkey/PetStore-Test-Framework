import json
import pytest
from utils import BaseTest


class TestStockTrackerApp(BaseTest):

    VALUATION = {'valuation': float}

    USER_PORTFOLIO_EXPECTED = {'AMZN': 1}

    # Initiate portfolio with expected test data
    @pytest.fixture(autouse=True, scope='session')
    def create_user_portfolio(self):
        self._post_request(url='http://localhost:8080/api/holding', data={'ticker': 'AMZN', 'units': 1})

    @classmethod
    def setup_class(cls):
        cls.tracker_endpoint_url = BaseTest.BASE_URL
        cls.holding_endpoint = cls.tracker_endpoint_url + 'holding'
        cls.portfolio_endpoint = cls.tracker_endpoint_url + 'portfolio'
        cls.valuation_endpoint = cls.tracker_endpoint_url + 'valuation'

    def test_get_portfolio_check_data_type(self):
        portfolio = self._get_user_portfolio()
        # Compare response portfolio to expected result
        assert portfolio == self.USER_PORTFOLIO_EXPECTED

    def test_get_valuation_check_type_and_structure(self):
        r = self._get_request(url=self.valuation_endpoint)
        valuation = json.loads(r.content)
        assert r.status_code == 200
        assert valuation['valuation'] > 0
        for key in valuation:
            # Verify returned valuation dict types and structure
            assert isinstance(valuation[key], self.VALUATION.get(key)), '{} key incorrect format'.format(key)
            assert all(key in valuation for key in self.VALUATION), '{} key is missing'.format(key)

    def test_add_update_and_remove_holding(self):
        # This test adds the twitter stock to the portfolio,
        # updates and deletes it. Verification is made for the whole flow.
        ticker = 'TWTR'

        # Add new ticker
        r_add_ticker = self._post_request(url=self.holding_endpoint, data={'ticker': ticker, 'units': 5})
        assert r_add_ticker.status_code == 201

        # Check ticker is created
        user_portfolio = self._get_user_portfolio()
        assert ticker in user_portfolio and user_portfolio[ticker] == 5

        # Update ticker value
        r_update_ticker = self._post_request(url=self.holding_endpoint, data={'ticker': ticker, 'units': 6})
        assert r_update_ticker.status_code == 201

        # Check ticker is updated
        user_portfolio = self._get_user_portfolio()
        assert ticker in user_portfolio and user_portfolio[ticker] == 6

        # # Delete ticker
        r_del_ticker = self._delete_request(url=self.holding_endpoint, data={'ticker': ticker})
        assert r_del_ticker.status_code == 204

        # Check ticker is deleted
        user_portfolio = self._get_user_portfolio()
        assert ticker not in user_portfolio

    @pytest.mark.parametrize('ticker', ('A A P L', '!@#$%', '    ', 'VOW3.DE', '1234'))
    def test_add_new_stock_using_invalid_tracker(self, ticker):
        r = self._post_request(url=self.holding_endpoint, data={'ticker': ticker, 'units': 1})
        assert r.status_code == 400

    @pytest.mark.parametrize('units', ('A', 'a', '@', ' ', '.'))
    def test_add_new_stock_using_invalid_units(self, units):
        r = self._post_request(url=self.holding_endpoint, data={'ticker': 'AAPL', 'units': units})
        assert r.status_code == 400
