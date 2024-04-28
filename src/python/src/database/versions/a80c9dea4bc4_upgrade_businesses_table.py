"""Upgrade businesses table

Revision ID: a80c9dea4bc4
Revises: af8170dfe367
Create Date: 2024-03-18 09:19:42.997112

"""
import sqlalchemy as sa
from alembic import op



# revision identifiers, used by Alembic.
revision = 'a80c9dea4bc4'
down_revision = 'af8170dfe367'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(op.f('ix_businesses_accreditation_rating'), 'businesses', ['accreditation_rating'], unique=False)
    op.create_index(op.f('ix_businesses_age_of_the_company'), 'businesses', ['age_of_the_company'], unique=False)
    op.create_index(op.f('ix_businesses_average_score'), 'businesses', ['average_score'], unique=False)
    op.create_index(op.f('ix_businesses_business_id'), 'businesses', ['business_id'], unique=False)
    op.create_index(op.f('ix_businesses_category'), 'businesses', ['category'], unique=False)
    op.create_index(op.f('ix_businesses_city'), 'businesses', ['city'], unique=False)
    op.create_index(op.f('ix_businesses_country'), 'businesses', ['country'], unique=False)
    op.create_index(op.f('ix_businesses_name'), 'businesses', ['name'], unique=False)
    op.create_index(op.f('ix_businesses_postcode'), 'businesses', ['postcode'], unique=False)
    op.create_index(op.f('ix_businesses_region'), 'businesses', ['region'], unique=False)
    op.create_index(op.f('ix_businesses_street'), 'businesses', ['street'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_businesses_street'), table_name='businesses')
    op.drop_index(op.f('ix_businesses_region'), table_name='businesses')
    op.drop_index(op.f('ix_businesses_postcode'), table_name='businesses')
    op.drop_index(op.f('ix_businesses_name'), table_name='businesses')
    op.drop_index(op.f('ix_businesses_country'), table_name='businesses')
    op.drop_index(op.f('ix_businesses_city'), table_name='businesses')
    op.drop_index(op.f('ix_businesses_category'), table_name='businesses')
    op.drop_index(op.f('ix_businesses_business_id'), table_name='businesses')
    op.drop_index(op.f('ix_businesses_average_score'), table_name='businesses')
    op.drop_index(op.f('ix_businesses_age_of_the_company'), table_name='businesses')
    op.drop_index(op.f('ix_businesses_accreditation_rating'), table_name='businesses')
