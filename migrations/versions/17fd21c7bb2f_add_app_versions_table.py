"""Add app_versions table

Revision ID: 17fd21c7bb2f
Revises: 493eb4adb377
Create Date: 2025-01-14 09:00:29.370856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17fd21c7bb2f'
down_revision = '493eb4adb377'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ratings', schema=None) as batch_op:
        batch_op.alter_column('status_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ratings', schema=None) as batch_op:
        batch_op.alter_column('status_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
