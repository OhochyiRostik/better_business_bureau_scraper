from sqlalchemy import select, update
from database.models import Business
from rmq.commands import Producer

from rmq.utils import TaskStatusCodes


class ProducerCustom(Producer):
    def build_task_query_stmt(self, chunk_size):
        """This method must returns sqlalchemy Executable or string that represents valid raw SQL select query"""

        stmt = select(Business.id, Business.url, Business.status).where(
            Business.status == TaskStatusCodes.NOT_PROCESSED.value,
        ).order_by(Business.id.asc()).limit(chunk_size)
        return stmt

    def build_task_update_stmt(self, db_task, status):
        """This method must returns sqlalchemy Executable or string that represents valid raw SQL update query"""

        return update(Business).where(Business.id == db_task['id']).values({'status': status})
