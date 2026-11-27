import psycopg2
from typing import Optional, Tuple, List, Any


class DbConnection:
    _instance: Optional["DbConnection"] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        dbname: str = "library",
        user: str = "postgres",
        password: str = "postgres",
    ):
        if self._initialized:
            return
        self._conn = psycopg2.connect(
            host=host, port=port, dbname=dbname, user=user, password=password
        )
        self._initialized = True

    def execute(self, sql: str, params: Tuple = (), commit: bool = False):
        cur = self._conn.cursor()
        cur.execute(sql, params)
        if commit:
            self._conn.commit()
        return cur

    def fetch_all(self, sql: str, params: Tuple = (), commit: bool = False) -> List[Tuple[Any, ...]]:
        cur = self.execute(sql, params, commit=commit)
        try:
            return cur.fetchall()
        finally:
            cur.close()

    def close(self) -> None:
        if self._conn and not self._conn.closed:
            self._conn.close()

    @classmethod
    def reset(cls) -> None:
        if cls._instance is not None:
            cls._instance.close()
        cls._instance = None