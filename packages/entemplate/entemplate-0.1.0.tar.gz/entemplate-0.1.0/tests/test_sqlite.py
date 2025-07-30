# type: ignore

from contextlib import closing


def test_execute():
    import sqlite3

    from entemplate._sqlite import execute

    with closing(sqlite3.connect(":memory:")) as connection, closing(connection.cursor()) as cursor:
        execute(cursor, "CREATE TABLE test(a, b)")
        execute(cursor, t"INSERT INTO test VALUES ({1}, {2})")
        execute(cursor, t"INSERT INTO test VALUES ({'1, 2); DROP TABLE test; --'}, {2})")
        execute(cursor, t"INSERT INTO test VALUES ({'hello'!r}, {4})")
        assert execute(cursor, t"SELECT * FROM test").fetchall() == [(1, 2), ('1, 2); DROP TABLE test; --', 2), ("'hello'", 4)]
