import sqlite3

from entemplate import Template, normalize

__all__ = ['execute']


def execute(cursor: sqlite3.Cursor, sql: Template | str) -> sqlite3.Cursor:
    """
    Execute a SQL statement using the provided cursor.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor to execute the SQL statement.
        sql (Template | str): The SQL statement to execute.

    Returns:
        sqlite3.Cursor: The cursor after executing the SQL statement.
    """
    if isinstance(sql, str):
        return cursor.execute(sql)

    query = []
    params = []
    for item in sql:
        if isinstance(item, str):
            query.append(item)
        else:
            query.append("?")
            params.append(normalize(item))
    return cursor.execute(''.join(query), params)
