"""add new order fields to order

Revision ID: 624c6e837145
Revises: 1a82b365f2a1
Create Date: 2026-08-24 14:24:33.698153

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '624c6e837145'
down_revision = '1a82b365f2a1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('order', sa.Column('weight_g', sa.Integer(), nullable=True))
    op.add_column('order', sa.Column('category', sa.String(length=100), nullable=True))
    op.add_column('order', sa.Column('payment_type', sa.String(length=32), nullable=True))
    op.add_column('order', sa.Column('seller_state', sa.String(length=2), nullable=True))
    op.add_column('order', sa.Column('customer_state', sa.String(length=2), nullable=True))


def downgrade():
    op.drop_column('order', 'customer_state')
    op.drop_column('order', 'seller_state')
    op.drop_column('order', 'payment_type')
    op.drop_column('order', 'category')
    op.drop_column('order', 'weight_g')
