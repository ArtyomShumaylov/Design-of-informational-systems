# reader_rep_db.py
from typing import List, Optional
from ReaderData_mapper_overloading import ReaderFull, ReaderBrief
from db_connection import DbConnection


class ReaderRepDb:
    TABLE = "readers"

    def __init__(self, conn: DbConnection):
        self._conn = conn
        self._ensure_table()

    def _ensure_table(self) -> None:
        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.TABLE} (
            client_id SERIAL PRIMARY KEY,
            last_name VARCHAR(100) NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            sur_name VARCHAR(100) NOT NULL,
            address VARCHAR(255) NOT NULL,
            phone_number VARCHAR(30) NOT NULL
        );
        """
        self._conn.execute(sql, commit=True)

    def read_all(self) -> List[ReaderFull]:
        sql = f"SELECT client_id, last_name, first_name, sur_name, address, phone_number FROM {self.TABLE};"
        rows = self._conn.fetch_all(sql)
        return [self._row_to_reader(r) for r in rows]

    def get_by_id(self, client_id: int) -> Optional[ReaderFull]:
        sql = f"SELECT client_id, last_name, first_name, sur_name, address, phone_number FROM {self.TABLE} WHERE client_id = %s;"
        rows = self._conn.fetch_all(sql, (client_id,))
        return self._row_to_reader(rows[0]) if rows else None

    def get_k_n_short_list(self, k: int, n: int) -> List[ReaderBrief]:
        if k < 0 or n < 0:
            raise ValueError("k и n должны быть неотрицательными")
        sql = f"""
            SELECT last_name, first_name, sur_name
            FROM {self.TABLE}
            ORDER BY last_name
            LIMIT %s OFFSET %s;
        """
        rows = self._conn.fetch_all(sql, (k, n * k))
        return [
            ReaderBrief(last_name=r[0], first_name=r[1], sur_name=r[2])
            for r in rows
        ]

    def add(self, reader: ReaderFull) -> int:
        sql = f"""
            INSERT INTO {self.TABLE} (last_name, first_name, sur_name, address, phone_number)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING client_id;
        """
        rows = self._conn.fetch_all(
            sql,
            (reader.last_name, reader.first_name, reader.sur_name,
             reader.address, reader.phone_number),
            commit=True,
        )
        return rows[0][0]

    def replace(self, client_id: int, reader: ReaderFull) -> bool:
        sql = f"""
            UPDATE {self.TABLE}
            SET last_name = %s, first_name = %s, sur_name = %s,
                address = %s, phone_number = %s
            WHERE client_id = %s;
        """
        cur = self._conn.execute(
            sql,
            (reader.last_name, reader.first_name, reader.sur_name,
             reader.address, reader.phone_number, client_id),
            commit=True,
        )
        return cur.rowcount > 0

    def delete(self, client_id: int) -> bool:
        sql = f"DELETE FROM {self.TABLE} WHERE client_id = %s;"
        cur = self._conn.execute(sql, (client_id,), commit=True)
        return cur.rowcount > 0

    def get_count(self) -> int:
        sql = f"SELECT COUNT(*) FROM {self.TABLE};"
        rows = self._conn.fetch_all(sql)
        return rows[0][0]

    @staticmethod
    def _row_to_reader(row) -> ReaderFull:
        return ReaderFull(
            client_id=row[0],
            last_name=row[1],
            first_name=row[2],
            sur_name=row[3],
            address=row[4],
            phone_number=row[5],
        )