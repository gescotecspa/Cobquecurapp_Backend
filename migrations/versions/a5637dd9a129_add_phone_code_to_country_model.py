"""Add phone_code to Country model

Revision ID: a5637dd9a129
Revises: a87c63466647
Create Date: 2024-08-12 10:50:22.440289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5637dd9a129'
down_revision = 'a87c63466647'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('countries', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone_code', sa.String(length=10), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('countries', schema=None) as batch_op:
        batch_op.drop_column('phone_code')

    # ### end Alembic commands ###
