"""
Database utility module for connecting to and querying databases.
"""

import sqlite3
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file.
    
    Args:
        db_file (str): Path to the SQLite database file
        
    Returns:
        Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logger.info(f"Connected to database: {db_file}")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
    
    return conn

def create_table(conn, create_table_sql):
    """Create a table from the create_table_sql statement.
    
    Args:
        conn (Connection): Connection object
        create_table_sql (str): SQL statement to create a table
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        logger.info("Table created successfully")
        return True
    except sqlite3.Error as e:
        logger.error(f"Error creating table: {e}")
        return False

def insert_data(conn, table, columns, values):
    """Insert data into a table.
    
    Args:
        conn (Connection): Connection object
        table (str): Table name
        columns (list): List of column names
        values (list): List of values to insert
        
    Returns:
        int: Row ID of the inserted row, or -1 if failed
    """
    try:
        c = conn.cursor()
        placeholders = ", ".join(["?" for _ in values])
        columns_str = ", ".join(columns)
        sql = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
        c.execute(sql, values)
        conn.commit()
        logger.info(f"Data inserted successfully. Row ID: {c.lastrowid}")
        return c.lastrowid
    except sqlite3.Error as e:
        logger.error(f"Error inserting data: {e}")
        return -1

def query_data(conn, sql, params=()):
    """Query data from the database.
    
    Args:
        conn (Connection): Connection object
        sql (str): SQL query
        params (tuple): Parameters for the query
        
    Returns:
        list: Query results as a list of rows
    """
    try:
        c = conn.cursor()
        c.execute(sql, params)
        rows = c.fetchall()
        logger.info(f"Query executed successfully. Returned {len(rows)} rows.")
        return rows
    except sqlite3.Error as e:
        logger.error(f"Error querying data: {e}")
        return []

def close_connection(conn):
    """Close the database connection.
    
    Args:
        conn (Connection): Connection object
    """
    if conn:
        conn.close()
        logger.info("Database connection closed")
