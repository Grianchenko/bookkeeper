import datetime
import sqlite3

from bookkeeper.repository.sqlite_repository import SQLiteRepository  # CustomClass
from dataclasses import dataclass
import pytest


@pytest.fixture
def custom_class():
    @dataclass
    class Custom:
        pk: int = 0
        name: str = 'hebe'
        date: datetime.datetime = datetime.datetime(2023, 3, 6)
        test_float: float = 1.2451

    return Custom


@pytest.fixture
def repo(custom_class):
    return SQLiteRepository('new_db.db', custom_class)


def test_crud(repo, custom_class):
    obj = custom_class()
    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk) == obj, f'{pk}, {obj}, {repo.get(pk)}, {repo.fields}'
    obj2 = custom_class()
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2
    repo.delete(pk)
    assert repo.get(pk) is None


def test_cannot_add_with_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = None
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_delete_unexistent(repo, custom_class):
    obj = custom_class()
    pk = repo.add(obj)
    with pytest.raises(KeyError):
        repo.delete(pk + 10)


def test_cannot_update_without_pk(repo, custom_class):
    obj = custom_class()
    with pytest.raises(ValueError):
        repo.update(obj)


def test_get_all(repo, custom_class):
    objects = [custom_class() for i in range(5)]
    for o in objects:
        repo.add(o)
    assert repo.get_all() == objects


def test_get_all_with_condition(repo, custom_class):
    objects = []
    for i in range(5):
        o = custom_class()
        o.test_float = i + 2.4
        o.name = 'bababababa'
        repo.add(o)
        objects.append(o)
    assert repo.get_all({'test_float': 2.4}) == [objects[0]]
    assert repo.get_all({'name': 'bababababa'}) == objects
