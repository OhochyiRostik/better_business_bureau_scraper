from scrapy.exceptions import NotConfigured
from scrapy.utils.project import get_project_settings
from sqlalchemy import insert
from twisted.internet import defer
from twisted.enterprise import adbapi
from scrapy import signals

from database.models import Business
from rmq.utils.sql_expressions import compile_expression


class SaveToDatabasePipeline:
    """
    Connecting to the database and entering data
    """

    def __init__(self):
        self.logger = None
        self.dbpool = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signal=signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.logger = spider.logger
        self.logger.info("Spider opened: %s", spider.name)
        settings = get_project_settings()
        self.dbpool = adbapi.ConnectionPool(
            "MySQLdb",
            host=settings.get("DB_HOST"),
            port=settings.getint("DB_PORT"),
            user=settings.get("DB_USERNAME"),
            passwd=settings.get("DB_PASSWORD"),
            db=settings.get("DB_DATABASE"),
            charset="utf8mb4",
            use_unicode=True,
            cp_reconnect=True,
        )

    def spider_closed(self, spider):
        self.logger.info("Spider closed: %s", spider.name)
        if self.dbpool is not None:
            self.dbpool.close()

    def process_item(self, item, spider):
        if self.dbpool is None:
            raise NotConfigured("Database pool is not initialized")
        # SQL
        # query = self.dbpool.runOperation("INSERT INTO businesses (url) VALUES (%s)", (item["url"],))

        # SQLAlchemy
        insert_query = insert(Business).values(url=item["url"])
        query = self.dbpool.runOperation(*compile_expression(insert_query))

        query.addErrback(self.handle_error)
        return item

    def handle_error(self, failure):
        self.logger.error("Error while saving item to the database: %s", failure)
