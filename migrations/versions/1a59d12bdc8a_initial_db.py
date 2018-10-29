"""Initial db

Revision ID: 1a59d12bdc8a
Revises: None
Create Date: 2017-03-31 12:38:43.841692

"""

# revision identifiers, used by Alembic.
revision = '1a59d12bdc8a'
down_revision = None


from alembic import op
import sqlalchemy as sa
from flask import current_app


def upgrade():
    op.create_table('local_land_charge_id',
                    sa.Column('id', sa.BigInteger(), primary_key=True),
                    sa.Column('stub', sa.String(1), default='', nullable=False, unique=True))

    op.execute("GRANT ALL ON ALL TABLES IN SCHEMA public TO " + current_app.config.get('APP_SQL_USERNAME'))
    op.execute("GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO " + current_app.config.get('APP_SQL_USERNAME'))
    pass


def downgrade():
    op.drop_table('local_land_charge_id')
