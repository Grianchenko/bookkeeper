from itertools import count
from typing import Any
from dataclasses import dataclass

from bookkeeper.repository.abstract_repository import AbstractRepository, T
from inspect import get_annotations

import sqlite3


# @dataclass
# class CustomClass:
#     pk: int
#     name: str
#     # date: datetime


class SQLiteRepository(AbstractRepository[T]):
    def __init__(self, db_file: str, cls: type):
        self.cls: type = cls
        self.db_file: str = db_file
        self.table_name: str = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')

    def add(self, obj: T) -> int:
        names = ', '.join(self.fields.keys())
        p = ', '.join('?' * len(self.fields))
        values = [getattr(obj, i) for i in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f'INSERT INTO {self.table_name} ({names}) VALUES ({p})', values)
            con.commit()
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            res = cur.execute(f'SELECT * FROM {self.table_name} WHERE pk = {pk}')
            temp = res.fetchone()
        con.close()
        if temp is None:
            return None
        obj = self.cls(*temp)
        converted_temp = ()
        for i in range(len(temp)):
            try:
                converted_temp += (list(obj.__annotations__.values())[i](temp[i]),)
            except TypeError:
                converted_temp += (list(obj.__annotations__.values())[i].strptime(temp[i], '%Y-%m-%d %H:%M:%S'),)
        return self.cls(*converted_temp)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            res = cur.execute(f'SELECT * FROM {self.table_name}')
        if where is None:
            return [self.cls(*obj) for obj in res.fetchall()]
        return [self.cls(*obj) for obj in res.fetchall() if all(getattr(obj, attr) == value for attr, value in where.items())]

    def update(self, obj: T) -> None:
        names = list(self.fields.keys())
        values = [getattr(obj, i) for i in self.fields]
        pk = obj.pk
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            for i in range(len(names)):
                # assert False, f'{len(names)}, {names}, {names[i]}, {values}, {values[i]}'
                try:
                    cur.execute(f'UPDATE {self.table_name} SET {names[1]} = {repr(values[1])} WHERE pk = {pk}')
                except sqlite3.OperationalError:
                    cur.execute(f'UPDATE {self.table_name} SET {names[1]} = {repr(str(values[1]))} WHERE pk = {pk}')
            con.commit()
        con.close()

    def delete(self, pk: int) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'DELETE FROM {self.table_name} WHERE pk = {pk}')
            con.commit()
        con.close()

