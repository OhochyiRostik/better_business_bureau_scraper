# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, String, BigInteger, JSON, Date

from . import Base
from .mixins import MysqlPrimaryKeyMixin, MysqlTimestampsMixin, MysqlStatusMixin


class Business(Base, MysqlPrimaryKeyMixin, MysqlStatusMixin, MysqlTimestampsMixin):
    __tablename__ = 'businesses'

    url = Column(String(768), index=True, unique=True, nullable=False)
    business_id = Column(String(768), nullable=True, index=True)
    detail_page_url = Column(String(768), nullable=True)
    name = Column(String(255), nullable=True, index=True)
    category = Column(String(255), nullable=True, index=True)
    address = Column(String(768), nullable=True)
    country = Column(String(16), nullable=True, index=True)
    region = Column(String(32), nullable=True, index=True)
    city = Column(String(32), nullable=True, index=True)
    street = Column(String(128), nullable=True, index=True)
    postcode = Column(String(16), nullable=True, index=True)
    link_to_website = Column(String(768), nullable=True)
    link_to_image = Column(String(768), nullable=True)
    phone_number = Column(BigInteger, nullable=True)
    fax = Column(String(32), nullable=True)
    working_hours_data = Column(JSON, nullable=True)
    average_score = Column(String(16), nullable=True, index=True)
    number_of_grades = Column(Integer, nullable=True)
    accreditation_rating = Column(String(16), nullable=True, index=True)
    date_of_accreditation = Column(Date, nullable=True, index=True)
    date_of_establishment = Column(Date, nullable=True, index=True)
    age_of_the_company = Column(Integer, nullable=True, index=True)
    instagram_link = Column(String(768), nullable=True)
    facebook_link = Column(String(768), nullable=True)
    twitter_link = Column(String(768), nullable=True)
    business_management = Column(JSON, nullable=True)
    contact_information = Column(JSON, nullable=True)

    # for csv_exporter
    sent_to_customer = Column(Date, nullable=True)
