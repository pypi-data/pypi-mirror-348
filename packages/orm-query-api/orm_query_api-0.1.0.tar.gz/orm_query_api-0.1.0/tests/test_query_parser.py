import datetime
import operator

import pytest
from sqlalchemy.orm import InstrumentedAttribute

from orm_query_api.parser.query_parser import ActionTree, parse_query, FilterAction, SortAction, SortOrder, NestedField


def test_simple_select():
    query = "q=(id, name)"
    expected = ActionTree()
    expected.select = ["id", "name"]

    result = parse_query(query)
    assert result.select == expected.select


def test_filter():
    query = "q=(id, name).filter(id=1)"
    expected = ActionTree()
    expected.select = ["id", "name"]
    expected.filters = [FilterAction("id", operator.eq, 1)]

    result = parse_query(query)
    assert result.select == expected.select
    assert result.filters[0].field.fields[0] == expected.filters[0].field


def test_sort():
    query = "q=(id, name).order(id,asc)"
    expected = ActionTree()
    expected.select = ["id", "name"]
    expected.sort = SortAction(SortOrder.ASC, NestedField(["id"]))

    result = parse_query(query)
    assert result.select == expected.select
    assert result.sort.order == expected.sort.order
    assert result.sort.field.fields == expected.sort.field.fields


def test_limit_and_offset():
    query = "q=(id).offset(5).limit(10)"
    expected = ActionTree()
    expected.select = ["id"]
    expected.limit = 10
    expected.offset = 5

    result = parse_query(query)
    assert result.select == expected.select
    assert result.limit == expected.limit
    assert result.offset == expected.offset


def test_nested_fields():
    query = "q=(id, user(id, name)).filter(user.id=1)"
    expected = ActionTree()
    expected.select = ["id"]
    user_tree = ActionTree()
    user_tree.name = "user"
    user_tree.select = ["id", "name"]
    expected.relations["user"] = user_tree
    expected.filters = [FilterAction(NestedField(["user", "id"]), operator.eq, 1)]

    result = parse_query(query)
    assert result.select == expected.select
    assert result.relations["user"].select == expected.relations["user"].select
    assert result.filters[0].field.fields == expected.filters[0].field.fields


def test_invalid_query():
    query = "q=(id, name).filter(id=)"
    with pytest.raises(Exception):
        parse_query(query)


def test_date_filter():
    query = "q=(id, created_at).filter(created_at=2022-01-01)"
    expected = ActionTree()
    expected.select = ["id", "created_at"]
    expected.filters = [
        FilterAction(
            "created_at",
            operator.eq,
            datetime.datetime.strptime("2022-01-01", "%Y-%m-%d").date(),
        )
    ]

    result = parse_query(query)
    assert result.select == expected.select
    assert result.filters[0].value == expected.filters[0].value


def test_in_operator():
    query = """q=(name).filter(name in "rfefef")"""
    expected = ActionTree()
    expected.select = ["name"]
    expected.filters = [FilterAction("name", InstrumentedAttribute.in_, "rfefef")]

    result = parse_query(query)
    assert result.select == expected.select
    assert result.filters[0].field.fields[0] == expected.filters[0].field
    assert result.filters[0].operator == expected.filters[0].operator
    assert result.filters[0].value == expected.filters[0].value


def test_is_null_operator():
    query = """q=(name).filter(name is_null "None")"""
    expected = ActionTree()
    expected.select = ["name"]
    expected.filters = [FilterAction("name", InstrumentedAttribute.is_, "None")]

    result = parse_query(query)
    assert result.select == expected.select
    assert result.filters[0].field.fields[0] == expected.filters[0].field
    assert result.filters[0].operator == expected.filters[0].operator
    assert result.filters[0].value == expected.filters[0].value
