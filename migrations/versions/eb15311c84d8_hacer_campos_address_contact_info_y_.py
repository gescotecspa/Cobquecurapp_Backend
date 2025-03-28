"""Hacer campos address, contact_info y business_type opcionales

Revision ID: eb15311c84d8
Revises: 7d9e7d23af10
Create Date: 2024-08-26 19:07:44.514225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb15311c84d8'
down_revision = '7d9e7d23af10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('partner_details', schema=None) as batch_op:
        batch_op.alter_column('address',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('contact_info',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('partner_details', schema=None) as batch_op:
        batch_op.alter_column('contact_info',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
        batch_op.alter_column('address',
               existing_type=sa.TEXT(),
               nullable=False)

    # ### end Alembic commands ###
