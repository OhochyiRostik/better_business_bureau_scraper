from sqlalchemy import insert, update

from database.models import Business
from rmq.commands import Consumer


class ConsumerReplyQueueCustom(Consumer):
    def build_message_store_stmt(self, message_body):
        """If processing message task requires several queries to db or single query has extreme difficulty
        then this self.process_message method could be overridden.
        In this case using of self.build_message_store_stmt method is not required
        and could be overridden with pass statement"""

        stmt = update(Business).where(Business.url == message_body['url']).values(
            status=message_body["status"]
        )
        return stmt

