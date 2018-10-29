"""Limit DB user

Revision ID: 0999b9bda8c7
Revises: 1a59d12bdc8a
Create Date: 2017-09-21 07:58:06.194639

"""

# revision identifiers, used by Alembic.
revision = '0999b9bda8c7'
down_revision = '1a59d12bdc8a'

from alembic import op
import sqlalchemy as sa
from flask import current_app


def upgrade():
    op.execute("REVOKE ALL ON ALL TABLES IN SCHEMA public FROM " + current_app.config.get('APP_SQL_USERNAME'))
    op.execute("REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM " + current_app.config.get('APP_SQL_USERNAME'))
    op.execute("GRANT DELETE, INSERT, SELECT ON local_land_charge_id TO " + current_app.config.get('APP_SQL_USERNAME'))
    op.execute("GRANT SELECT, UPDATE ON local_land_charge_id_id_seq TO " + current_app.config.get('APP_SQL_USERNAME'))


def downgrade():
    op.execute("GRANT ALL ON ALL TABLES IN SCHEMA public TO " + current_app.config.get('APP_SQL_USERNAME'))
    op.execute("GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO " + current_app.config.get('APP_SQL_USERNAME'))
