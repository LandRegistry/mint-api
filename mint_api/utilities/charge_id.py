from mint_api.models import LocalLandChargeId
from flask import current_app

LOCK_TABLE = 'LOCK TABLE local_land_charge_id IN ACCESS EXCLUSIVE MODE'
STUB_VALUE = 'a'


class ChargeIdService(object):
    @staticmethod
    def generate_charge_id():
        local_land_charge_id_entity = LocalLandChargeId
        local_land_charge_stub = LocalLandChargeId(STUB_VALUE)

        query = local_land_charge_id_entity.query

        try:
            current_app.logger.info("Lock local_land_charge_id table")
            query.session.execute(LOCK_TABLE)
            current_app.logger.info("Clear local_land_charge_id table")
            query.delete()
            current_app.logger.info("Add new row to local_land_charge_id")
            query.session.add(local_land_charge_stub)
            charge_id = query.first().id
            current_app.audit_logger.info("Update local_land_charge_id with Charge ID: %s", charge_id)
            query.session.commit()

            return charge_id
        except Exception as e:  # pragma: no cover
            current_app.logger.exception("Failed to generate Charge ID: %s", str(e))
            query.session.rollback()
            raise
        finally:
            query.session.close()
