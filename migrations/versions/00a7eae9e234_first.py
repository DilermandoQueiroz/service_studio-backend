"""first

Revision ID: 00a7eae9e234
Revises: 
Create Date: 2022-12-28 22:19:19.016504

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '00a7eae9e234'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sell', 'scheduled_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.create_unique_constraint(None, 'service_provider', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'service_provider', type_='unique')
    op.alter_column('sell', 'scheduled_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###
