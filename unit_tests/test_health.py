from mint_api.main import app
from mint_api.exceptions import ApplicationError
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime


class TestHealth(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_health(self):
        self.assertEqual((self.app.get('/health')).status_code, 200)

    @patch("mint_api.dependencies.postgres.psycopg2")
    @patch('mint_api.app.requests.Session')
    def test_health_cascade(self, requests, pg):
        with app.test_request_context():
            response = MagicMock()
            response.status_code = 200
            response.headers = {'content-type': 'application/unit+test'}
            response.json.return_value = {}
            requests.return_value.get.return_value = response
            pg.connect.return_value.cursor.return_value.fetchone.return_value = [datetime.now()]

            resp = self.app.get('/health/cascade/4')
            self.assertEqual(resp.status_code, 200)

    @patch("mint_api.views.general.postgres")
    @patch('mint_api.app.requests.Session')
    def test_health_cascade_no_postgres(self, requests, pg):
        pg.get_current_timestamp.side_effect = ApplicationError("blah", 400)
        response = self.app.get('/health/cascade/4')
        self.assertEqual(response.status_code, 500)
