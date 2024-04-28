from commands.base import BaseCSVExporter
from typing import List, Dict
from sqlalchemy import Table
from database.models import Business


class CSVExporter(BaseCSVExporter):
    table: Table = Business
    file_timestamp_format: str = '%Y%b%d%H%M%S'
    export_date_column: str = 'sent_to_customer'
    file_extension: str = 'csv'
    chunk_size: int = 1000
    excluded_columns: List[str] = []
    specific_columns: List[str] = []
    headers: List[str] = []
    new_mapping: Dict[str, str] = {}
    filename_prefix: str = ''
    filename_postfix: str = ''
    file_path: str = ''
    file_exists: bool = True
