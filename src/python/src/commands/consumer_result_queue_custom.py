from sqlalchemy import insert, update
from sqlalchemy.dialects import mysql

from database.models import Business
from rmq.commands import Consumer


class ConsumerResultQueueCustom(Consumer):
    def build_message_store_stmt(self, message_body):
        """If processing message task requires several queries to db or single query has extreme difficulty
        then this self.process_message method could be overridden.
        In this case using of self.build_message_store_stmt method is not required
        and could be overridden with pass statement"""

        stmt = update(Business).where(Business.url == message_body['url']).values(
            business_id=message_body["business_id"],
            detail_page_url=message_body["detail_page_url"],
            name=message_body["name"],
            category=message_body["category"],
            address=message_body["address"],
            country=message_body["country"],
            region=message_body["region"],
            city=message_body["city"],
            street=message_body["street"],
            postcode=message_body["postcode"],
            link_to_website=message_body["link_to_website"],
            link_to_image=message_body["link_to_image"],
            phone_number=message_body["phone_number"],
            fax=message_body["fax"],
            working_hours_data=message_body["working_hours_data"],
            average_score=message_body["average_score"],
            number_of_grades=message_body["number_of_grades"],
            accreditation_rating=message_body["accreditation_rating"],
            date_of_accreditation=message_body["date_of_accreditation"],
            date_of_establishment=message_body["date_of_establishment"],
            age_of_the_company=message_body["age_of_the_company"],
            instagram_link=message_body["instagram_link"],
            facebook_link=message_body["facebook_link"],
            twitter_link=message_body["twitter_link"],
            business_management=message_body["business_management"],
            contact_information=message_body["contact_information"],
        )
        return stmt

