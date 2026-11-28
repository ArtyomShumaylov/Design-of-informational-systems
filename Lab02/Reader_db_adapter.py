# reader_db_adapter.py
from typing import List, Optional
from repository import ReaderRepository
from reader_rep_db import ReaderRepDb
from db_connection import DbConnection
from ReaderData_mapper_overloading import ReaderFull, ReaderBrief


class ReaderRepDbAdapter(ReaderRepository):

    def __init__(self, conn: DbConnection):
        self._impl = ReaderRepDb(conn)

    def read_all(self) -> List[ReaderFull]:
        return self._impl.read_all()

    def get_by_id(self, client_id: int) -> Optional[ReaderFull]:
        return self._impl.get_by_id(client_id)

    def get_k_n_short_list(self, k: int, n: int) -> List[ReaderBrief]:
        return self._impl.get_k_n_short_list(k, n)

    def sort_by_last_name(self) -> None:
        pass

    def add(self, reader: ReaderFull) -> int:
        return self._impl.add(reader)

    def replace(self, client_id: int, reader: ReaderFull) -> bool:
        return self._impl.replace(client_id, reader)

    def delete(self, client_id: int) -> bool:
        return self._impl.delete(client_id)

    def get_count(self) -> int:
        return self._impl.get_count()