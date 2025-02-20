import datetime
from typing import List
from fastmcp import FastMCP
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
)

mcp = FastMCP("Choose MCP Server")

sqlalchemy_url = 'bigquery://choose-data-prod/core'
engine = create_engine(sqlalchemy_url)
db = SQLDatabase(engine)

get_schema_tool = InfoSQLDatabaseTool(db=db)
list_tables_tool = ListSQLDatabaseTool(db=db)


@mcp.tool()
def get_tables() -> List[str]:
    """
    Get the list of tables in the database.

    Returns:
        List[str]: The list of tables in the database.
    """

    return list_tables_tool.invoke("")


@mcp.tool()
def get_schema(table: str) -> str:
    """
    Get the schema of a table in the database, along with the description of each available field.
    """
    return get_schema_tool.invoke(table)


@mcp.tool()
def db_query_tool(query: str) -> str:
    """
    Input to this tool is a detailed and correct SQL query, output is a result from the database. If the query is not correct, an error message will be returned. If an error is returned, rewrite the query, check the query, and try again. If you encounter an issue with Unknown column 'xxxx' in 'field list', use get_schema to query the correct table fields.
    Execute a SQL query against the database and get back the result.
    If the query is not correct, an error message will be returned.
    If an error is returned, rewrite the query, check the query, and try again.
    """
    result = db.run_no_throw(query)
    if not result:
        return "Error: Query failed. Please rewrite your query and try again."
    return result


if __name__ == "__main__":
    mcp.run()