"""Add reset_code and reset_code_expiration to User

Revision ID: 342c5a8183a2
Revises: fea2448346c2
Create Date: 2024-08-08 18:34:19.698787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '342c5a8183a2'
down_revision = 'fea2448346c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('playing_with_neon')
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'promotions', ['promotion_id'], ['promotion_id'])

    with op.batch_alter_table('promotion_categories', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'promotions', ['promotion_id'], ['promotion_id'])

    with op.batch_alter_table('promotion_images', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'promotions', ['promotion_id'], ['promotion_id'])

    with op.batch_alter_table('tourist_ratings', schema=None) as batch_op:
        batch_op.drop_constraint('_tourist_branch_uc', type_='unique')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reset_code_expiration', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('reset_code_expiration')

    with op.batch_alter_table('tourist_ratings', schema=None) as batch_op:
        batch_op.create_unique_constraint('_tourist_branch_uc', ['tourist_id', 'branch_id'])

    with op.batch_alter_table('promotion_images', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    with op.batch_alter_table('promotion_categories', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    op.create_table('playing_with_neon',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('value', sa.REAL(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='playing_with_neon_pkey')
    )
    # ### end Alembic commands ###
