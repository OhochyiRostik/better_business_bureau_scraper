import scrapy

from rmq.items import RMQItem


class BusinessItem(RMQItem):
    url = scrapy.Field()
    business_id = scrapy.Field()
    detail_page_url = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    address = scrapy.Field()
    country = scrapy.Field()
    region = scrapy.Field()
    city = scrapy.Field()
    street = scrapy.Field()
    postcode = scrapy.Field()
    link_to_website = scrapy.Field()
    link_to_image = scrapy.Field()
    phone_number = scrapy.Field()
    fax = scrapy.Field()
    working_hours_data = scrapy.Field()
    average_score = scrapy.Field()
    number_of_grades = scrapy.Field()
    accreditation_rating = scrapy.Field()
    date_of_accreditation = scrapy.Field()
    date_of_establishment = scrapy.Field()
    age_of_the_company = scrapy.Field()
    instagram_link = scrapy.Field()
    facebook_link = scrapy.Field()
    twitter_link = scrapy.Field()
    business_management = scrapy.Field()
    contact_information = scrapy.Field()
