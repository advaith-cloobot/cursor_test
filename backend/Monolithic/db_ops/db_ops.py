"""
Database Operations Module
This module contains CRUD operations for all database tables
"""

import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from Components.SQLlite.sql_lite import get_db_connection
from Monolithic.constants.constants import STATUS_ACTIVE, STATUS_ARCHIVED


# ==================== USERS TABLE OPERATIONS ====================

def insert_user(user_name, user_email, user_password):
    """
    Insert a new user into the users table
    
    Args:
        user_name (str): User's name
        user_email (str): User's email
        user_password (str): User's password (should be hashed before calling)
    
    Returns:
        int: The user_id of the newly created user, or None if failed
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO users (user_name, user_email, user_password, created_timestamp, last_updated_timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_name, user_email, user_password, datetime.now(), datetime.now(), STATUS_ACTIVE))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id
    except Exception as e:
        print(f"Error inserting user: {e}")
        return None


def read_user(user_id):
    """
    Read a user by user_id
    
    Args:
        user_id (int): The user ID
    
    Returns:
        dict: User data or None if not found
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE user_id = ? AND status != ?", (user_id, STATUS_ARCHIVED))
        user = cursor.fetchone()
        conn.close()
        
        return dict(user) if user else None
    except Exception as e:
        print(f"Error reading user: {e}")
        return None


def read_user_by_email(user_email):
    """
    Read a user by email
    
    Args:
        user_email (str): The user email
    
    Returns:
        dict: User data or None if not found
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE user_email = ? AND status != ?", (user_email, STATUS_ARCHIVED))
        user = cursor.fetchone()
        conn.close()
        
        return dict(user) if user else None
    except Exception as e:
        print(f"Error reading user by email: {e}")
        return None


def update_user(user_id, user_name=None, user_email=None, user_password=None):
    """
    Update a user's information
    
    Args:
        user_id (int): The user ID
        user_name (str, optional): New user name
        user_email (str, optional): New user email
        user_password (str, optional): New user password
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if user_name is not None:
            updates.append("user_name = ?")
            params.append(user_name)
        if user_email is not None:
            updates.append("user_email = ?")
            params.append(user_email)
        if user_password is not None:
            updates.append("user_password = ?")
            params.append(user_password)
        
        if not updates:
            return False
        
        updates.append("last_updated_timestamp = ?")
        params.append(datetime.now())
        params.append(user_id)
        
        query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = ?"
        cursor.execute(query, params)
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating user: {e}")
        return False


def archive_user(user_id):
    """
    Archive a user (soft delete)
    
    Args:
        user_id (int): The user ID
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE users SET status = ?, last_updated_timestamp = ? WHERE user_id = ?
        """, (STATUS_ARCHIVED, datetime.now(), user_id))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error archiving user: {e}")
        return False


# ==================== CHAT_SESSION TABLE OPERATIONS ====================

def insert_chat_session(session_name, created_user_id, session_description=""):
    """
    Insert a new chat session
    
    Args:
        session_name (str): Session name
        created_user_id (int): User ID who created the session
        session_description (str, optional): Session description
    
    Returns:
        int: The chat_session_id of the newly created session, or None if failed
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO chat_session (session_name, session_description, session_created_timestamp, 
                                     session_last_updated_timestamp, created_user_id, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (session_name, session_description, datetime.now(), datetime.now(), created_user_id, STATUS_ACTIVE))
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return session_id
    except Exception as e:
        print(f"Error inserting chat session: {e}")
        return None


def read_chat_session(chat_session_id):
    """
    Read a chat session by chat_session_id
    
    Args:
        chat_session_id (int): The chat session ID
    
    Returns:
        dict: Chat session data or None if not found
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM chat_session WHERE chat_session_id = ? AND status != ?", 
                      (chat_session_id, STATUS_ARCHIVED))
        session = cursor.fetchone()
        conn.close()
        
        return dict(session) if session else None
    except Exception as e:
        print(f"Error reading chat session: {e}")
        return None


def read_all_chat_sessions():
    """
    Read all available chat sessions
    
    Returns:
        list: List of all chat sessions
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM chat_session 
            WHERE status != ?
            ORDER BY session_last_updated_timestamp DESC
        """, (STATUS_ARCHIVED,))
        
        sessions = cursor.fetchall()
        conn.close()
        
        return [dict(session) for session in sessions]
    except Exception as e:
        print(f"Error reading all chat sessions: {e}")
        return []


def update_chat_session(chat_session_id, session_name=None, session_description=None):
    """
    Update a chat session's information
    
    Args:
        chat_session_id (int): The chat session ID
        session_name (str, optional): New session name
        session_description (str, optional): New session description
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if session_name is not None:
            updates.append("session_name = ?")
            params.append(session_name)
        if session_description is not None:
            updates.append("session_description = ?")
            params.append(session_description)
        
        if not updates:
            return False
        
        updates.append("session_last_updated_timestamp = ?")
        params.append(datetime.now())
        params.append(chat_session_id)
        
        query = f"UPDATE chat_session SET {', '.join(updates)} WHERE chat_session_id = ?"
        cursor.execute(query, params)
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating chat session: {e}")
        return False


def archive_chat_session(chat_session_id):
    """
    Archive a chat session (soft delete)
    
    Args:
        chat_session_id (int): The chat session ID
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE chat_session SET status = ?, session_last_updated_timestamp = ? 
            WHERE chat_session_id = ?
        """, (STATUS_ARCHIVED, datetime.now(), chat_session_id))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error archiving chat session: {e}")
        return False


# ==================== CHAT_MESSAGES TABLE OPERATIONS ====================

def insert_chat_message(chat_session_id, message_text, message_from_id, 
                       message_to_id, message_created_user_id):
    """
    Insert a new chat message
    
    Args:
        chat_session_id (int): The chat session ID
        message_text (str): The message text
        message_from_id (int): ID of the sender
        message_to_id (int): ID of the receiver
        message_created_user_id (int): User ID who created the message
    
    Returns:
        int: The chat_message_id of the newly created message, or None if failed
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO chat_messages (chat_session_id, message_text, message_from_id, 
                                      message_to_id, message_created_timestamp, 
                                      message_created_user_id, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (chat_session_id, message_text, message_from_id, message_to_id, 
              datetime.now(), message_created_user_id, STATUS_ACTIVE))
        
        message_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return message_id
    except Exception as e:
        print(f"Error inserting chat message: {e}")
        return None


def read_chat_message(chat_message_id):
    """
    Read a chat message by chat_message_id
    
    Args:
        chat_message_id (int): The chat message ID
    
    Returns:
        dict: Chat message data or None if not found
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM chat_messages WHERE chat_message_id = ? AND status != ?", 
                      (chat_message_id, STATUS_ARCHIVED))
        message = cursor.fetchone()
        conn.close()
        
        return dict(message) if message else None
    except Exception as e:
        print(f"Error reading chat message: {e}")
        return None


def read_session_messages(chat_session_id):
    """
    Read all messages for a chat session
    
    Args:
        chat_session_id (int): The chat session ID
    
    Returns:
        list: List of chat messages
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM chat_messages 
            WHERE chat_session_id = ? AND status != ?
            ORDER BY message_created_timestamp ASC
        """, (chat_session_id, STATUS_ARCHIVED))
        
        messages = cursor.fetchall()
        conn.close()
        
        return [dict(message) for message in messages]
    except Exception as e:
        print(f"Error reading session messages: {e}")
        return []


def update_chat_message(chat_message_id, message_text=None):
    """
    Update a chat message's text
    
    Args:
        chat_message_id (int): The chat message ID
        message_text (str, optional): New message text
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if message_text is None:
            return False
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE chat_messages SET message_text = ? WHERE chat_message_id = ?
        """, (message_text, chat_message_id))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating chat message: {e}")
        return False


def archive_chat_message(chat_message_id):
    """
    Archive a chat message (soft delete)
    
    Args:
        chat_message_id (int): The chat message ID
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE chat_messages SET status = ? WHERE chat_message_id = ?
        """, (STATUS_ARCHIVED, chat_message_id))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error archiving chat message: {e}")
        return False

