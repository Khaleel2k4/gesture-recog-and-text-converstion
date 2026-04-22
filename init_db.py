"""
Database initialization script for gesture recognition system
Run this script to create the database schema
"""

from db_config import db_config
from mysql.connector import Error

def create_tables():
    """Create all necessary tables for the gesture recognition system"""
    
    # First, ensure the database exists
    db_config.create_database_if_not_exists()
    
    # Get connection to the database
    connection = db_config.get_connection()
    
    if not connection:
        print("Failed to connect to database")
        return False
    
    try:
        cursor = connection.cursor()
        
        # Create users table
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP NULL
        )
        """
        cursor.execute(users_table)
        print("Users table created successfully")
        
        # Create gestures table to store recognized gestures
        gestures_table = """
        CREATE TABLE IF NOT EXISTS gestures (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            gesture_label VARCHAR(10) NOT NULL,
            confidence FLOAT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
        cursor.execute(gestures_table)
        print("Gestures table created successfully")
        
        # Create sessions table to store recognition sessions
        sessions_table = """
        CREATE TABLE IF NOT EXISTS recognition_sessions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            session_end TIMESTAMP NULL,
            total_gestures INT DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
        cursor.execute(sessions_table)
        print("Recognition sessions table created successfully")
        
        # Create gesture statistics table
        stats_table = """
        CREATE TABLE IF NOT EXISTS gesture_statistics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            gesture_label VARCHAR(10) NOT NULL,
            recognition_count INT DEFAULT 0,
            last_recognized TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE KEY unique_user_gesture (user_id, gesture_label)
        )
        """
        cursor.execute(stats_table)
        print("Gesture statistics table created successfully")
        
        # Insert default user (can be changed later)
        insert_user = """
        INSERT IGNORE INTO users (email, password) 
        VALUES ('nagamjyothi691@gmail.com', 'sign@2026')
        """
        cursor.execute(insert_user)
        print("Default user inserted (if not exists)")
        
        connection.commit()
        print("\nDatabase initialization completed successfully!")
        return True
        
    except Error as e:
        print(f"Error creating tables: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    print("Initializing gesture recognition database...")
    print("=" * 50)
    create_tables()
