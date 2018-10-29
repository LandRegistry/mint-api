from mint_api.extensions import db


class LocalLandChargeId(db.Model):
    __tablename__ = 'local_land_charge_id'
    id = db.Column(db.BigInteger, primary_key=True)
    stub = db.Column(db.String, default='', nullable=False, unique=True)

    def __init__(self, stub):
        self.stub = stub
