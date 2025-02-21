import datetime
from fastmcp import FastMCP
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
)


mcp = FastMCP("Choose MCP Server")
sqlalchemy_url = f"bigquery://choose-data-prod/core"
engine = create_engine(sqlalchemy_url)
db = SQLDatabase(engine)


@mcp.tool()
def fetch_current_time() -> str:
    """
    Fetch the current time in UTC.

    Returns:
        str: The current time in UTC.
    """

    return datetime.datetime.now().isoformat()


@mcp.tool()
def get_tables() -> str:
    """
    Get the list of tables in the database.

    Returns:
        str: The list of tables in the database.
    """

    return ListSQLDatabaseTool(db=db).invoke("")


@mcp.tool()
def get_schema(table: str) -> str:
    """
    Get the schema of a table in the database, along with the description of each available field.
    
    Args:
        table (str): The name of the table in the database.

    Returns:
        str: The schema of the table in the database.
    """
    return InfoSQLDatabaseTool(db=db).invoke(table)


@mcp.tool()
def db_query_tool(query: str) -> str:
    """
    Execute a SQL query against the database and get back the result.
    Input to this tool is a detailed and correct SQL query, output is a result from the database. If the query is not correct, an error message will be returned. If an error is returned, rewrite the query, check the query, and try again. If you encounter an issue with Unknown column 'xxxx' in 'field list', use get_schema to query the correct table fields.
    If the query is not correct, an error message will be returned.
    If an error is returned, rewrite the query, check the query, and try again.
    """
    result = db.run_no_throw(query)
    if not result:
        return "Error: Query failed. Please rewrite your query and try again."
    return result


if __name__ == "__main__":
    mcp.run()