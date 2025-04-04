"""Add status to ratings

Revision ID: fc557c3d4d3a
Revises: 11dfa3c075e1
Create Date: 2024-12-30 19:25:21.991603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc557c3d4d3a'
down_revision = '11dfa3c075e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ratings', schema=None) as batch_op:
        batch_op.drop_constraint('ratings_tourist_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['tourist_id'], ['user_id'])

    # with op.batch_alter_table('users', schema=None) as batch_op:
    #     batch_op.drop_constraint('users_email_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_unique_constraint('users_email_key', ['email'])

    with op.batch_alter_table('ratings', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('ratings_tourist_id_fkey', 'tourists', ['tourist_id'], ['user_id'])

    # ### end Alembic commands ###
