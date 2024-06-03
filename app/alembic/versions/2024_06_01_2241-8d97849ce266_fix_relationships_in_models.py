"""Fix relationships in models

Revision ID: 8d97849ce266
Revises: 5d8de03dc5ce
Create Date: 2024-06-01 22:41:31.587672

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d97849ce266'
down_revision: Union[str, None] = '5d8de03dc5ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(op.f('uq_order_id'), 'order', ['id'])
    op.create_unique_constraint(op.f('uq_order_items_id'), 'order_items', ['id'])
    op.create_unique_constraint(op.f('uq_product_id'), 'product', ['id'])
    op.create_unique_constraint(op.f('uq_user_id'), 'user', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq_user_id'), 'user', type_='unique')
    op.drop_constraint(op.f('uq_product_id'), 'product', type_='unique')
    op.drop_constraint(op.f('uq_order_items_id'), 'order_items', type_='unique')
    op.drop_constraint(op.f('uq_order_id'), 'order', type_='unique')
    # ### end Alembic commands ###
