"""
SQLite Database Utilities
This module handles SQLite database connection and initialization
"""

import sqlite3
import os
from datetime import datetime

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'chat_app.db')


def get_db_connection():
    """
    Create and return a database connection
    
    Returns:
        sqlite3.Connection: Database connection object
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn


def init_database():
    """
    Initialize the database with required tables
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            user_email TEXT UNIQUE NOT NULL,
            user_password TEXT NOT NULL,
            created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_updated_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status INTEGER DEFAULT 1
        )
    """)
    
    # Create chat_session table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_session (
            chat_session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_name TEXT NOT NULL,
            session_description TEXT,
            session_created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            session_last_updated_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_user_id INTEGER NOT NULL,
            status INTEGER DEFAULT 1,
            FOREIGN KEY (created_user_id) REFERENCES users(user_id)
        )
    """)
    
    # Create chat_messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            chat_message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_session_id INTEGER NOT NULL,
            message_text TEXT NOT NULL,
            message_from_id INTEGER NOT NULL,
            message_to_id INTEGER NOT NULL,
            message_created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            message_created_user_id INTEGER NOT NULL,
            status INTEGER DEFAULT 1,
            FOREIGN KEY (chat_session_id) REFERENCES chat_session(chat_session_id),
            FOREIGN KEY (message_created_user_id) REFERENCES users(user_id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")


if __name__ == "__main__":
    init_database()

