"""Remove username and use email instead

Revision ID: 5321d5cbf3e3
Revises: af03a9b2599d
Create Date: 2024-07-15 19:31:21.695994

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5321d5cbf3e3'
down_revision = 'af03a9b2599d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('users_username_key', type_='unique')
        batch_op.drop_column('username')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.VARCHAR(length=80), autoincrement=False, nullable=False))
        batch_op.create_unique_constraint('users_username_key', ['username'])

    # ### end Alembic commands ###
