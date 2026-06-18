"""
Utility Functions: Database Connection and Management
Handles MySQL database operations with connection pooling
"""
import pymysql
from pymysql import Error
import logging
from config.config import get_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseConnection:
    """
    Manages MySQL database connections
    Implements connection pooling and error handling
    """
    
    _connections = {}
    
    @staticmethod
    def get_connection(config=None):
        """
        Get database connection
        
        Args:
            config: Configuration object
            
        Returns:
            Database connection object
        """
        if config is None:
            config = get_config()
        
        try:
            connection = pymysql.connect(
                host=config.MYSQL_HOST,
                port=config.MYSQL_PORT,
                user=config.MYSQL_USER,
                password=config.MYSQL_PASSWORD,
                database=config.MYSQL_DB,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            logger.info("Database connection successful")
            return connection
        except Error as e:
            logger.error(f"Database connection error: {str(e)}")
            raise
    
    @staticmethod
    def execute_query(query, params=None, fetch_one=False):
        """
        Execute a database query
        
        Args:
            query: SQL query string
            params: Query parameters
            fetch_one: If True, return single record; if False, return all
            
        Returns:
            Query results or None
        """
        connection = None
        try:
            connection = DatabaseConnection.get_connection()
            cursor = connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            connection.commit()
            
            if 'SELECT' in query.upper():
                if fetch_one:
                    return cursor.fetchone()
                else:
                    return cursor.fetchall()
            
            return cursor.rowcount
            
        except Error as e:
            logger.error(f"Query execution error: {str(e)}")
            if connection:
                connection.rollback()
            raise
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()
    
    @staticmethod
    def insert_record(table, data):
        """
        Insert a record into the database
        
        Args:
            table: Table name
            data: Dictionary with column: value pairs
            
        Returns:
            Last inserted ID
        """
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        
        connection = None
        try:
            connection = DatabaseConnection.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, list(data.values()))
            connection.commit()
            logger.info(f"Record inserted into {table}")
            return cursor.lastrowid
        except Error as e:
            logger.error(f"Insert error: {str(e)}")
            if connection:
                connection.rollback()
            raise
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()
    
    @staticmethod
    def update_record(table, data, where_clause, where_values):
        """
        Update a record in the database
        
        Args:
            table: Table name
            data: Dictionary with column: value pairs
            where_clause: WHERE condition
            where_values: WHERE values
            
        Returns:
            Number of affected rows
        """
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        values = list(data.values()) + where_values
        
        return DatabaseConnection.execute_query(query, values)
    
    @staticmethod
    def delete_record(table, where_clause, where_values):
        """
        Delete a record from the database
        
        Args:
            table: Table name
            where_clause: WHERE condition
            where_values: WHERE values
            
        Returns:
            Number of affected rows
        """
        query = f"DELETE FROM {table} WHERE {where_clause}"
        return DatabaseConnection.execute_query(query, where_values)
