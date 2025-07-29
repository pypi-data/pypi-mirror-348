from __future__ import annotations

from secrets import token_hex
from typing import Any, Iterator

import psycopg2
from pandas import DataFrame
from pgcopy import CopyManager
from sqlalchemy import create_engine


class PostgresDatabase:
    def __init__(self, conn: str, table: str) -> None:
        self.__conn = conn
        self.__table = table
        self.__table_rename = f"rename_{table}_{token_hex(nbytes=8)}"
        self.__tmp_table = f"tmp_{table}_{token_hex(nbytes=8)}"
        self.__destination = psycopg2.connect(conn)
        self.__destination.autocommit = False
        self.__cursor = self.__destination.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.__cursor.itersize = 10000

    def save(self, columns, data, first=True) -> bool:
        if first:
            return self.__initial_saver(columns, data)
        return self.__copy_manager_saver(columns, data)

    def close(self) -> None:
        self.__cursor.execute(
            f"ALTER TABLE IF EXISTS {self.__table} RENAME TO {self.__table_rename}"
        )
        self.__cursor.execute(f"ALTER TABLE IF EXISTS {self.__tmp_table} RENAME TO {self.__table}")
        self.__cursor.execute(f"DROP TABLE IF EXISTS {self.__table_rename}")
        self.__cursor.execute(f"DROP TABLE IF EXISTS {self.__tmp_table}")
        self.__destination.commit()
        self.__cursor.close()
        self.__destination.close()

    def __enter__(self) -> PostgresDatabase:
        return self

    def __exit__(self, type, value, traceback) -> None:
        self.close()

    def __initial_saver(self, columns: Iterator[Any], data: Iterator[Any]) -> bool:
        try:
            # Create the table with the first itens ...
            engine = create_engine(self.__conn, echo=False)
            df = DataFrame(data, columns=columns)
            df.to_sql(f"{self.__tmp_table}", index=False, con=engine)
            engine.dispose()
        except Exception as e:
            print(e)
            return False
        return True

    def __copy_manager_saver(self, columns: Iterator[Any], data: Iterator[Any]) -> bool:
        try:
            mgr = CopyManager(self.__destination, f"{self.__tmp_table}", columns)
            mgr.copy(data)
            self.__destination.commit()
        except Exception as e:
            print(e)
            return False
        return True