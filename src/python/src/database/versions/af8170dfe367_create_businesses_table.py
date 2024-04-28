"""Create businesses table

Revision ID: af8170dfe367
Revises:
Create Date: 2024-03-18 09:02:28.242960

"""
import sqlalchemy as sa
from alembic import op

from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'af8170dfe367'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('businesses',
    sa.Column('id', mysql.BIGINT(unsigned=True), autoincrement=True, nullable=False),
    sa.Column('status', mysql.MEDIUMINT(unsigned=True), server_default=sa.text('0'), nullable=False),
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('url', sa.String(length=768), nullable=False),
    sa.Column('business_id', sa.String(length=768), nullable=True),
    sa.Column('detail_page_url', sa.String(length=768), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('category', sa.String(length=255), nullable=True),
    sa.Column('address', sa.String(length=768), nullable=True),
    sa.Column('country', sa.String(length=16), nullable=True),
    sa.Column('region', sa.String(length=32), nullable=True),
    sa.Column('city', sa.String(length=32), nullable=True),
    sa.Column('street', sa.String(length=128), nullable=True),
    sa.Column('postcode', sa.String(length=16), nullable=True),
    sa.Column('link_to_website', sa.String(length=768), nullable=True),
    sa.Column('link_to_image', sa.String(length=768), nullable=True),
    sa.Column('phone_number', sa.BigInteger(), nullable=True),
    sa.Column('fax', sa.String(length=32), nullable=True),
    sa.Column('working_hours_data', sa.JSON(), nullable=True),
    sa.Column('average_score', sa.String(length=16), nullable=True),
    sa.Column('number_of_grades', sa.Integer(), nullable=True),
    sa.Column('accreditation_rating', sa.String(length=16), nullable=True),
    sa.Column('date_of_accreditation', sa.Date(), nullable=True),
    sa.Column('date_of_establishment', sa.Date(), nullable=True),
    sa.Column('age_of_the_company', sa.Integer(), nullable=True),
    sa.Column('instagram_link', sa.String(length=768), nullable=True),
    sa.Column('facebook_link', sa.String(length=768), nullable=True),
    sa.Column('twitter_link', sa.String(length=768), nullable=True),
    sa.Column('business_management', sa.JSON(), nullable=True),
    sa.Column('contact_information', sa.JSON(), nullable=True),
    sa.Column('sent_to_customer', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_businesses_status'), 'businesses', ['status'], unique=False)
    op.create_index(op.f('ix_businesses_updated_at'), 'businesses', ['updated_at'], unique=False)
    op.create_index(op.f('ix_businesses_url'), 'businesses', ['url'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_businesses_url'), table_name='businesses')
    op.drop_index(op.f('ix_businesses_updated_at'), table_name='businesses')
    op.drop_index(op.f('ix_businesses_status'), table_name='businesses')
    op.drop_table('businesses')
