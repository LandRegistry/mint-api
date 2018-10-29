from mint_api.main import app
from unittest import mock
import unittest
import json
from flask import g
from jwt_validation.exceptions import ValidationFailure


SIGNING_PATH = 'mint_api.views.v1_0.signing'
MOCK_CHARGE_ID = 1
EXPECTED_REGISTER_RESPONSE = {"igonedone": "insertedthis"}
EXPECTED_MINT_RESPONSE = {"local-land-charge": MOCK_CHARGE_ID, "igonedone": "insertedthis"}


class TestSigning(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @mock.patch('mint_api.app.validate')
    def test_no_item(self, validate):
        res = self.app.post('/v1.0/records',
                            headers={'Authorization': 'Fake JWT'})
        self.assertEqual((res.status_code, json.loads(res.get_data().decode('utf-8'))),
                         (400, {"error_message": "POST request must contain JSON", "error_code": "E102"}))

    @mock.patch('mint_api.app.validate')
    @mock.patch('{}.ChargeIdService'.format(SIGNING_PATH))
    @mock.patch('mint_api.utilities.cryptography.CryptographicSigning.sign_payload')
    @mock.patch('mint_api.app.requests.Session')
    def test_minified_json_to_sign_payload(self, session, mock_cryptography, mock_charge_id_service, validate):
        with app.test_request_context():
            g.session = mock.MagicMock()
            response = mock.MagicMock()
            response.status_code = 202
            response.json.return_value = EXPECTED_REGISTER_RESPONSE
            session.return_value.post.return_value = response
            mock_cryptography.return_value = "rs256:test_sig", "sha-256:test_hash"
            mock_charge_id_service.generate_charge_id.return_value = MOCK_CHARGE_ID

            res = self.app.post('/v1.0/records',
                                data='{"my-key": "my-value"}',
                                content_type="application/json",
                                headers={'Authorization': 'Fake JWT'})
            actual_result = json.loads(res.get_data().decode('utf-8'))

            mock_cryptography.assert_called_with(
                '{{"{}":{},"my-key":"my-value"}}'.format('local-land-charge', MOCK_CHARGE_ID))
            self.assertEqual((res.status_code, actual_result), (202, EXPECTED_MINT_RESPONSE))

    @mock.patch('mint_api.app.validate')
    @mock.patch('{}.ChargeIdService'.format(SIGNING_PATH))
    @mock.patch('mint_api.app.requests.Session')
    def test_valid_add(self, session, mock_charge_id_service, validate):
        with app.test_request_context():
            g.session = mock.MagicMock()
            response = mock.MagicMock()
            response.status_code = 202
            response.json.return_value = EXPECTED_REGISTER_RESPONSE
            session.return_value.post.return_value = response
            mock_charge_id_service.generate_charge_id.return_value = MOCK_CHARGE_ID

            res = self.app.post('/v1.0/records',
                                data='{"test_field": "w00t"}',
                                content_type="application/json",
                                headers={'Authorization': 'Fake JWT'})
            actual_result = json.loads(res.get_data().decode('utf-8'))

            self.assertEqual((res.status_code, actual_result),
                             (202, EXPECTED_MINT_RESPONSE))
            mock_charge_id_service.generate_charge_id.assert_called_once()

    @mock.patch('mint_api.app.validate')
    @mock.patch('{}.ChargeIdService'.format(SIGNING_PATH))
    @mock.patch('mint_api.app.requests.Session')
    def test_valid_update(self, session, mock_charge_id_service, validate):
        with app.test_request_context():
            g.session = mock.MagicMock()
            response = mock.MagicMock()
            response.status_code = 202
            response.json.return_value = EXPECTED_REGISTER_RESPONSE
            session.return_value.post.return_value = response

            res = self.app.post('/v1.0/records',
                                data='{"local-land-charge": 1}',
                                content_type="application/json",
                                headers={'Authorization': 'Fake JWT'})
            actual_result = json.loads(res.get_data().decode('utf-8'))

            self.assertEqual((res.status_code, actual_result),
                             (202, EXPECTED_MINT_RESPONSE))
            mock_charge_id_service.assert_not_called()

    @mock.patch('mint_api.app.validate')
    @mock.patch('{}.ChargeIdService'.format(SIGNING_PATH))
    @mock.patch('mint_api.app.requests.Session')
    def test_valid_register_fail(self, session, mock_charge_id_service, validate):
        with app.test_request_context():
            expected_register_result = {
                "error": "Bad times",
                "details": []
            }

            g.session = mock.MagicMock()
            response = mock.MagicMock()
            response.status_code = 400
            response.json.return_value = expected_register_result
            response.text.return_value = b'Bad times'
            session.return_value.post.return_value = response
            mock_charge_id_service.generate_charge_id.return_value = MOCK_CHARGE_ID

            res = self.app.post('/v1.0/records',
                                data='{"local-land-charge": "w00t"}',
                                content_type="application/json",
                                headers={'Authorization': 'Fake JWT'})
            actual_result = res.get_data().decode('utf-8')

            self.assertEqual(res.status_code, 400)
            self.assertEqual(True, 'error' in actual_result)
            self.assertEqual(True, 'details' in actual_result)
            self.assertEqual(True, 'Bad times' in actual_result)

    @mock.patch('mint_api.app.validate')
    def test_invalid_token(self, validate):
        validate.side_effect = ValidationFailure("Validate failed")
        res = self.app.post('/v1.0/records',
                            data='{"local-land-charge": "w00t"}',
                            content_type="application/json",
                            headers={'Authorization': 'Fake JWT'})
        self.assertEqual(res.status_code, 401)

    def test_no_token(self):
        with app.test_request_context():
            res = self.app.post('/v1.0/records',
                                data='{"local-land-charge": 1}',
                                content_type="application/json")
            self.assertEqual(res.status_code, 401)
