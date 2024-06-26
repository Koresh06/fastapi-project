"""add table BlacklistedToken

Revision ID: 9c4f35cd88a4
Revises: 4a31d7f1a0df
Create Date: 2024-06-05 23:21:41.004750

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c4f35cd88a4'
down_revision: Union[str, None] = '4a31d7f1a0df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklisted_token',
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('blacklisted_at', sa.DateTime(), nullable=False),
    sa.Column('uid', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('uid', name=op.f('pk_blacklisted_token')),
    sa.UniqueConstraint('uid', name=op.f('uq_blacklisted_token_uid'))
    )
    op.create_index(op.f('ix_blacklisted_token_token'), 'blacklisted_token', ['token'], unique=True)
    op.create_unique_constraint(op.f('uq_order_uid'), 'order', ['uid'])
    op.create_unique_constraint(op.f('uq_order_items_uid'), 'order_items', ['uid'])
    op.create_unique_constraint(op.f('uq_product_uid'), 'product', ['uid'])
    op.create_unique_constraint(op.f('uq_user_uid'), 'user', ['uid'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq_user_uid'), 'user', type_='unique')
    op.drop_constraint(op.f('uq_product_uid'), 'product', type_='unique')
    op.drop_constraint(op.f('uq_order_items_uid'), 'order_items', type_='unique')
    op.drop_constraint(op.f('uq_order_uid'), 'order', type_='unique')
    op.drop_index(op.f('ix_blacklisted_token_token'), table_name='blacklisted_token')
    op.drop_table('blacklisted_token')
    # ### end Alembic commands ###
