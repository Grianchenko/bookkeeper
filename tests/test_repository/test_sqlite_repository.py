from bookkeeper.repository.sqlite_repository import SQLiteRepository, CustomClass
from dataclasses import dataclass
import pytest


@pytest.fixture
def custom_class():
    @dataclass
    class Custom:
        pk: int = 0
        name: int = 'bebebe'
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
