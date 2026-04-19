import sqlite3
import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional

# Create an MCP server
mcp = FastMCP("SQLite Browser")

def get_db_connection(db_path: str, read_only: bool = True):
    """Create a database connection to the SQLite database. Default is read-only."""
    try:
        if read_only:
            # Construct a URI for read-only access
            # This is the strongest protection at the engine level
            db_uri = f"file:{db_path}?mode=ro"
            conn = sqlite3.connect(db_uri, uri=True)
        else:
            conn = sqlite3.connect(db_path)
            
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        raise ValueError(f"Could not connect to database at {db_path}: {str(e)}")

@mcp.tool()
def create_database(db_path: str) -> str:
    """
    Create a new empty SQLite database file at the specified path.
    """
    if os.path.exists(db_path):
        return f"Error: Database file already exists at {db_path}"
    
    # Ensure the directory exists
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        try:
            os.makedirs(db_dir, exist_ok=True)
        except Exception as e:
            return f"Error creating directory {db_dir}: {str(e)}"

    try:
        # Simply connecting and closing creates the file
        conn = sqlite3.connect(db_path)
        conn.close()
        return f"Successfully created a new SQLite database at {db_path}"
    except Exception as e:
        return f"Error creating database: {str(e)}"

@mcp.tool()
def list_databases(path: str = ".") -> List[str]:
    """
    List all SQLite database files (.db, .sqlite, .sqlite3) in the specified directory.
    Default is the current directory.
    """
    db_extensions = {".db", ".sqlite", ".sqlite3"}
    p = Path(path)
    if not p.exists():
        return [f"Error: Path {path} does not exist."]
    
    databases = [f.name for f in p.glob("*") if f.suffix.lower() in db_extensions]
    return databases if databases else ["No SQLite databases found in this directory."]

@mcp.tool()
def list_tables(db_path: str) -> List[str]:
    """
    List all tables in the specified SQLite database.
    """
    if not os.path.exists(db_path):
        return [f"Error: Database file not found at {db_path}"]
    
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row["name"] for row in cursor.fetchall()]
            return tables if tables else ["No tables found in this database."]
    except Exception as e:
        return [f"Error listing tables: {str(e)}"]

@mcp.tool()
def describe_table(db_path: str, table_name: str) -> Dict[str, Any]:
    """
    Get the schema (columns) and a few sample rows from the specified table.
    """
    if not os.path.exists(db_path):
        return {"error": f"Database file not found at {db_path}"}
    
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            
            # Get schema
            cursor.execute(f"PRAGMA table_info('{table_name}');")
            columns = [dict(row) for row in cursor.fetchall()]
            
            # Get sample data
            cursor.execute(f"SELECT * FROM '{table_name}' LIMIT 5;")
            rows = [dict(row) for row in cursor.fetchall()]
            
            return {
                "table": table_name,
                "columns": columns,
                "sample_rows": rows
            }
    except Exception as e:
        return {"error": f"Error describing table {table_name}: {str(e)}"}

@mcp.tool()
def get_schema_summary(db_path: str) -> Dict[str, Any]:
    """
    Get a comprehensive summary of the entire database schema,
    including all tables and their column definitions.
    """
    if not os.path.exists(db_path):
        return {"error": f"Database file not found at {db_path}"}
    
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = [row["name"] for row in cursor.fetchall()]
            
            schema_summary = {}
            for table in tables:
                cursor.execute(f"PRAGMA table_info('{table}');")
                columns = [f"{row['name']} ({row['type']})" for row in cursor.fetchall()]
                schema_summary[table] = columns
                
            return {
                "database": os.path.basename(db_path),
                "tables_count": len(tables),
                "schema": schema_summary
            }
    except Exception as e:
        return {"error": f"Error getting schema summary: {str(e)}"}

@mcp.tool()
def add_record(db_path: str, table_name: str, title: str, content: str) -> str:
    """
    Add a new record to the specified table in the database.
    If the table doesn't exist, it will be created with columns: 
    id, title, content, and created_at.
    """
    try:
        with get_db_connection(db_path, read_only=False) as conn:
            cursor = conn.cursor()
            # Ensure the specified table exists
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS "{table_name}" (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # Insert the record
            cursor.execute(
                f'INSERT INTO "{table_name}" (title, content) VALUES (?, ?)',
                (title, content)
            )
            conn.commit()
            return f"Successfully saved to table '{table_name}' in {db_path}"
    except Exception as e:
        return f"Error saving record to {table_name}: {str(e)}"

@mcp.tool()
def search_databases(path: str, query: str) -> List[Dict[str, Any]]:
    """
    Search for a keyword in all SQLite databases within a directory.
    Searches table names and column names to help discover relevant data.
    """
    db_extensions = {".db", ".sqlite", ".sqlite3"}
    p = Path(path)
    if not p.exists():
        return [{"error": f"Path {path} does not exist."}]
    
    results = []
    query_lower = query.lower()
    
    # Get all potential database files
    try:
        db_files = [f for f in p.glob("*") if f.suffix.lower() in db_extensions]
    except Exception as e:
        return [{"error": f"Error scanning directory: {str(e)}"}]
    
    for db_file in db_files:
        db_path = str(db_file)
        try:
            with get_db_connection(db_path) as conn:
                cursor = conn.cursor()
                
                # Search table names
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
                tables = [row["name"] for row in cursor.fetchall()]
                
                for table in tables:
                    # Match table name
                    if query_lower in table.lower():
                        results.append({
                            "database": db_file.name,
                            "table": table,
                            "match_type": "table_name",
                            "context": f"Table '{table}' matches query"
                        })
                    
                    # Search column names
                    cursor.execute(f"PRAGMA table_info('{table}');")
                    for col_row in cursor.fetchall():
                        col_name = col_row["name"]
                        if query_lower in col_name.lower():
                            results.append({
                                "database": db_file.name,
                                "table": table,
                                "column": col_name,
                                "match_type": "column_name",
                                "context": f"Column '{col_name}' in table '{table}' matches query"
                            })
        except Exception:
            # Skip files that aren't valid databases or are locked
            continue
            
    return results if results else [{"message": f"No matches found for '{query}' in {path}"}]

@mcp.tool()
def execute_query(db_path: str, query: str) -> List[Dict[str, Any]]:
    """
    Execute a SELECT query on the specified SQLite database.
    Strictly enforced as READ-ONLY: only SELECT statements are allowed.
    """
    if not os.path.exists(db_path):
        return [{"error": f"Database file not found at {db_path}"}]
    
    clean_query = query.strip().upper()
    
    # Security Check 1: Must start with SELECT
    if not clean_query.startswith("SELECT"):
        return [{"error": "Security violation: Only SELECT queries are allowed."}]
    
    # Security Check 2: Prevent multiple statements (semicolon injection)
    if ";" in query.strip()[:-1]: # Allow trailing semicolon but not middle ones
        return [{"error": "Security violation: Multiple SQL statements are not allowed."}]

    # Security Check 3: Forbidden keywords for extra safety
    forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "CREATE", "RENAME", "TRUNCATE", "REPLACE"]
    for word in forbidden:
        if f" {word} " in f" {clean_query} ":
            return [{"error": f"Security violation: Forbidden keyword '{word}' detected."}]
    
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = [dict(row) for row in cursor.fetchall()]
            return rows if rows else [{"message": "Query returned no results."}]
    except Exception as e:
        return [{"error": f"Error executing query: {str(e)}"}]
