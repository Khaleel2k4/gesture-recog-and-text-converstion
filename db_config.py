import mysql.connector
from mysql.connector import Error

class DatabaseConfig:
    """Database configuration for MySQL connection"""
    
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.user = 'root'
        self.password = 'Khaleel@2004'
        self.database = 'gesture_recognition'
    
    def get_connection(self):
        """Create and return a MySQL database connection"""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def create_database_if_not_exists(self):
        """Create the database if it doesn't exist"""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password
            )
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            connection.commit()
            cursor.close()
            connection.close()
            print(f"Database '{self.database}' created or already exists")
        except Error as e:
            print(f"Error creating database: {e}")

# Global database config instance
db_config = DatabaseConfig()
