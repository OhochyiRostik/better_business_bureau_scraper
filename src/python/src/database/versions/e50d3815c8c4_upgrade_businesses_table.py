"""Upgrade businesses table

Revision ID: e50d3815c8c4
Revises: a80c9dea4bc4
Create Date: 2024-03-18 09:23:50.630144

"""
import sqlalchemy as sa
from alembic import op



# revision identifiers, used by Alembic.
revision = 'e50d3815c8c4'
down_revision = 'a80c9dea4bc4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(op.f('ix_businesses_date_of_accreditation'), 'businesses', ['date_of_accreditation'], unique=False)
    op.create_index(op.f('ix_businesses_date_of_establishment'), 'businesses', ['date_of_establishment'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_businesses_date_of_establishment'), table_name='businesses')
    op.drop_index(op.f('ix_businesses_date_of_accreditation'), table_name='businesses')
