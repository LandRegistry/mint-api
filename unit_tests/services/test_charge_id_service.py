from unittest import TestCase
from mock import patch, MagicMock
from mint_api.utilities import charge_id

CHARGE_ID_SERVICE_PATH = 'mint_api.utilities.charge_id'
EXPECTED_ID = "1"
EXPECTED_EXCEPTION_MESSAGE = 'test exception'


class TestChargeIdService(TestCase):
    @patch('{}.LocalLandChargeId'.format(CHARGE_ID_SERVICE_PATH))
    @patch('{}.current_app'.format(CHARGE_ID_SERVICE_PATH))
    def test_generate_charge_id_success(self, mock_current_app, mock_local_land_charge_id):
        mock_current_app.logger = MagicMock()

        mock_local_land_charge_id.query = MagicMock()
        mock_local_land_charge_id.query.first.return_value.id = EXPECTED_ID
        mock_local_land_charge_id.query.session = MagicMock()
        mock_local_land_charge_id.delete = MagicMock()

        llc_id = charge_id.ChargeIdService.generate_charge_id()
        self.assertEqual(llc_id, EXPECTED_ID)
        self.assert_usual_methods_called(mock_local_land_charge_id)

        mock_local_land_charge_id.query.session.commit.assert_called_once()
        mock_local_land_charge_id.query.session.close.assert_called_once()

    @patch('{}.LocalLandChargeId'.format(CHARGE_ID_SERVICE_PATH))
    @patch('{}.current_app'.format(CHARGE_ID_SERVICE_PATH))
    def test_generate_charge_id_exception(self, mock_current_app, mock_local_land_charge_id):
        mock_current_app.logger = MagicMock()

        mock_local_land_charge_id.query = MagicMock()
        mock_local_land_charge_id.query.first.side_effect = Exception(EXPECTED_EXCEPTION_MESSAGE)
        mock_local_land_charge_id.query.session = MagicMock()
        mock_local_land_charge_id.delete = MagicMock()

        try:
            charge_id.ChargeIdService.generate_charge_id()
        except Exception:
            self.assert_usual_methods_called(mock_local_land_charge_id)

            mock_local_land_charge_id.query.session.rollback.assert_called_once()
            mock_current_app.logger.exception.assert_called_once_with('Failed to generate Charge ID: %s',
                                                                      EXPECTED_EXCEPTION_MESSAGE)
            mock_local_land_charge_id.query.session.close.assert_called_once()
        else:
            self.assertIsNotNone(None, "Exception expected")

    @staticmethod
    def assert_usual_methods_called(mock_local_land_charge_id):
        """Helper function so we don't have duplicated code between tests"""
        mock_local_land_charge_id.assert_called_with(charge_id.STUB_VALUE)
        mock_local_land_charge_id.query.session.execute.assert_called_once_with(charge_id.LOCK_TABLE)
        mock_local_land_charge_id.query.delete.assert_called_once()
        mock_local_land_charge_id.query.session.add.assert_called_once_with(mock_local_land_charge_id('a'))
        mock_local_land_charge_id.query.first.assert_called_once()
