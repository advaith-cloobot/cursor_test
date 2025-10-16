"""
Utility Functions Module
This module contains utility functions for login, signup, and chat processing
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from Components.gpt_tools.gpt_tools import process_message
from Monolithic.db_ops.db_ops import (
    insert_user, read_user_by_email, insert_chat_session, 
    insert_chat_message, read_session_messages, update_chat_session
)
from Monolithic.constants.constants import (
    STATUS_ACTIVE, MESSAGE_FROM_USER, MESSAGE_FROM_SYSTEM,
    DEFAULT_SESSION_NAME, DEFAULT_SESSION_DESCRIPTION
)


def validate_login(username, password):
    """
    Validate user login credentials
    
    Args:
        username (str): User's email or username
        password (str): User's password
    
    Returns:
        tuple: (bool, dict/str) - (success status, user data or error message)
    """
    try:
        # Read user by email (using email as username)
        user = read_user_by_email(username)
        
        if not user:
            return False, "User not found"
        
        # Check if user is active
        if user['status'] != STATUS_ACTIVE:
            return False, "User account is inactive"
        
        # Compare plain text passwords
        if user['user_password'] == password:
            # Remove password from returned user data
            user_data = {k: v for k, v in user.items() if k != 'user_password'}
            return True, user_data
        else:
            return False, "Invalid password"
    except Exception as e:
        print(f"Error validating login: {e}")
        return False, "Login validation failed"


def signup_user(user_name, user_email, user_password):
    """
    Sign up a new user
    
    Args:
        user_name (str): User's name
        user_email (str): User's email
        user_password (str): User's password
    
    Returns:
        tuple: (bool, dict/str) - (success status, user data or error message)
    """
    try:
        # Check if user already exists
        existing_user = read_user_by_email(user_email)
        if existing_user:
            return False, "User with this email already exists"
        
        # Insert new user with plain text password
        user_id = insert_user(user_name, user_email, user_password)
        
        if user_id:
            return True, {
                "user_id": user_id,
                "user_name": user_name,
                "user_email": user_email,
                "message": "User registered successfully"
            }
        else:
            return False, "Failed to create user"
    except Exception as e:
        print(f"Error signing up user: {e}")
        return False, "User registration failed"


def save_system_response(session_id, response_text):
    """
    Save system response to the database
    
    Args:
        session_id (int): The chat session ID
        response_text (str): The system response text
    
    Returns:
        tuple: (bool, dict/str) - (success status, message data or error message)
    """
    try:
        from Monolithic.db_ops.db_ops import insert_chat_message
        
        # Insert system message (message_from_id = 0 for system)
        message_id = insert_chat_message(
            chat_session_id=session_id,
            message_text=response_text,
            message_from_id=0,  # System message
            message_to_id=0,  # System to user
            message_created_user_id=0  # System user
        )
        
        if message_id:
            return True, {
                "message_id": message_id,
                "message_text": response_text,
                "message_from_id": 0
            }
        else:
            return False, "Failed to save system response"
    except Exception as e:
        print(f"Error saving system response: {e}")
        return False, "Failed to save system response"


def create_new_chat_session(user_id, session_name=None, session_description=None):
    """
    Create a new chat session
    
    Args:
        user_id (int): User ID who is creating the session
        session_name (str, optional): Name of the session
        session_description (str, optional): Description of the session
    
    Returns:
        tuple: (bool, dict/str) - (success status, session data or error message)
    """
    try:
        if not session_name:
            session_name = DEFAULT_SESSION_NAME
        if not session_description:
            session_description = DEFAULT_SESSION_DESCRIPTION
        
        session_id = insert_chat_session(session_name, user_id, session_description)
        
        if session_id:
            return True, {
                "chat_session_id": session_id,
                "session_name": session_name,
                "session_description": session_description,
                "message": "Chat session created successfully"
            }
        else:
            return False, "Failed to create chat session"
    except Exception as e:
        print(f"Error creating chat session: {e}")
        return False, "Chat session creation failed"


def process_chat_message(session_id, message_text, user_id):
    """
    Process a chat message, insert it into the database, get AI response,
    and insert the response into the database
    
    Args:
        session_id (int): The chat session ID
        message_text (str): The message text from the user
        user_id (int): The user ID who sent the message
    
    Returns:
        tuple: (bool, dict/str) - (success status, response data or error message)
    """
    try:
        # Insert the incoming user message into the database
        # message_from_id = user_id (user sending message)
        # message_to_id = 0 (system/AI)
        user_message_id = insert_chat_message(
            chat_session_id=session_id,
            message_text=message_text,
            message_from_id=user_id,
            message_to_id=MESSAGE_FROM_SYSTEM,
            message_created_user_id=user_id
        )
        
        if not user_message_id:
            return False, "Failed to insert user message"
        
        # Process the message using AI/ML tools
        response_text = process_message(session_id, message_text)
        
        # Insert the AI response into the database
        # message_from_id = 0 (system/AI sending response)
        # message_to_id = user_id (responding to user)
        ai_message_id = insert_chat_message(
            chat_session_id=session_id,
            message_text=response_text,
            message_from_id=MESSAGE_FROM_SYSTEM,
            message_to_id=user_id,
            message_created_user_id=user_id
        )
        
        if not ai_message_id:
            return False, "Failed to insert AI response"
        
        # Update the session's last updated timestamp
        update_chat_session(session_id)
        
        return True, {
            "user_message_id": user_message_id,
            "ai_message_id": ai_message_id,
            "response_text": response_text,
            "message": "Message processed successfully"
        }
    except Exception as e:
        print(f"Error processing chat message: {e}")
        return False, "Message processing failed"


def get_chat_history(session_id):
    """
    Fetch all messages for a given chat session
    
    Args:
        session_id (int): The chat session ID
    
    Returns:
        tuple: (bool, list/str) - (success status, list of messages or error message)
    """
    try:
        messages = read_session_messages(session_id)
        
        if messages is not None:
            return True, messages
        else:
            return False, "Failed to fetch chat history"
    except Exception as e:
        print(f"Error fetching chat history: {e}")
        return False, "Failed to fetch chat history"

