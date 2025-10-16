"""
Flask Server with API Routes
Main server file that handles all API endpoints for the chat application
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add directories to path for imports
sys.path.append(os.path.dirname(__file__))

from Components.SQLlite.sql_lite import init_database
from Monolithic.utils.utils import (
    validate_login, signup_user, create_new_chat_session,
    process_chat_message, get_chat_history
)
from Monolithic.db_ops.db_ops import (
    read_user, read_all_chat_sessions, read_chat_session,
    update_chat_session, archive_chat_session
)
from Monolithic.constants.constants import (
    SUCCESS, CREATED, BAD_REQUEST, UNAUTHORIZED, 
    NOT_FOUND, INTERNAL_SERVER_ERROR
)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize database on startup
init_database()


# ==================== HEALTH CHECK ====================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Server is running"
    }), SUCCESS


# ==================== USER AUTHENTICATION ROUTES ====================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """
    Login endpoint
    
    Request body:
        {
            "username": "user@example.com",
            "password": "password123"
        }
    
    Returns:
        User data if successful, error message otherwise
    """
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({
                "success": False,
                "message": "Username and password are required"
            }), BAD_REQUEST
        
        username = data['username']
        password = data['password']
        
        success, result = validate_login(username, password)
        
        if success:
            return jsonify({
                "success": True,
                "data": result,
                "message": "Login successful"
            }), SUCCESS
        else:
            return jsonify({
                "success": False,
                "message": result
            }), UNAUTHORIZED
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({
            "success": False,
            "message": "Internal server error"
        }), INTERNAL_SERVER_ERROR


@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """
    Signup endpoint
    
    Request body:
        {
            "user_name": "John Doe",
            "user_email": "user@example.com",
            "user_password": "password123"
        }
    
    Returns:
        User data if successful, error message otherwise
    """
    try:
        data = request.get_json()
        
        if not data or 'user_name' not in data or 'user_email' not in data or 'user_password' not in data:
            return jsonify({
                "success": False,
                "message": "Name, email, and password are required"
            }), BAD_REQUEST
        
        user_name = data['user_name']
        user_email = data['user_email']
        user_password = data['user_password']
        
        success, result = signup_user(user_name, user_email, user_password)
        
        if success:
            return jsonify({
                "success": True,
                "data": result,
                "message": "User registered successfully"
            }), CREATED
        else:
            return jsonify({
                "success": False,
                "message": result
            }), BAD_REQUEST
    except Exception as e:
        print(f"Signup error: {e}")
        return jsonify({
            "success": False,
            "message": "Internal server error"
        }), INTERNAL_SERVER_ERROR


# ==================== USER ROUTES ====================

@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get user information by user_id
    """
    try:
        user = read_user(user_id)
        
        if user:
            # Remove password from response
            user_data = {k: v for k, v in user.items() if k != 'user_password'}
            return jsonify({
                "success": True,
                "data": user_data
            }), SUCCESS
        else:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), NOT_FOUND
    except Exception as e:
        print(f"Get user error: {e}")
        return jsonify({
            "success": False,
            "message": "Internal server error"
        }), INTERNAL_SERVER_ERROR


# ==================== CHAT SESSION ROUTES ====================

@app.route('/api/chat/session/create', methods=['POST'])
def create_session():
    """
    Create a new chat session
    
    Request body:
        {
            "user_id": 1,
            "session_name": "My Chat Session",
            "session_description": "Description here"
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'user_id' not in data:
            return jsonify({
                "success": False,
                "message": "User ID is required"
            }), BAD_REQUEST
        
        user_id = data['user_id']
        session_name = data.get('session_name')
        session_description = data.get('session_description')
        
        success, result = create_new_chat_session(user_id, session_name, session_description)
        
        if success:
            return jsonify({
                "success": True,
                "data": result,
                "message": "Chat session created successfully"
            }), CREATED
        else:
            return jsonify({
                "success": False,
                "message": result
            }), BAD_REQUEST
    except Exception as e:
        print(f"Create session error: {e}")
        return jsonify({
            "success": False,
            "message": "Internal server error"
        }), INTERNAL_SERVER_ERROR


@app.route('/api/chat/session/<int:session_id>', methods=['GET'])
def get_session(session_id):
    """
    Get chat session details by session_id
    """
    try:
        session = read_chat_session(session_id)
        
        if session:
            return jsonify({
                "success": True,
                "data": session
            }), SUCCESS
        else:
            return jsonify({
                "success": False,
                "message": "Chat session not found"
            }), NOT_FOUND
    except Exception as e:
        print(f"Get session error: {e}")
        return jsonify({
            "success": False,
            "message": "Internal server error"
        }), INTERNAL_SERVER_ERROR


@app.route('/api/chat/sessions', methods=['GET'])
def get_all_sessions():
    """
    Get all available chat sessions
    """
    try:
        sessions = read_all_chat_sessions()
        
        return jsonify({
            "success": True,
            "data": sessions,
            "count": len(sessions)
        }), SUCCESS
    except Exception as e:
        print(f"Get all sessions error: {e}")
        return jsonify({
            "success": False,
            "message": "Internal server error"
        }), INTERNAL_SERVER_ERROR


@app.route('/api/chat/session/<int:session_id>', methods=['PUT'])
def update_session(session_id):
    """
    Update chat session details
    
    Request body:
        {
            "session_name": "Updated Name",
            "session_description": "Updated Description"
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "message": "No data provided"
            }), BAD_REQUEST
        
        session_name = data.get('session_name')
        session_description = data.get('session_description')
        
        success = update_chat_session(session_id, session_name, session_description)
        
        if success:
            return jsonify({
                "success": True,
                "message": "Chat session updated successfully"
            }), SUCCESS
        else:
            return jsonify({
                "success": False,
                "message": "Failed to update chat session"
            }), BAD_REQUEST
    except Exception as e:
        print(f"Update session error: {e}")
        return jsonify({
            "success": False,
            "message": "Internal server error"
        }), INTERNAL_SERVER_ERROR


@app.route('/api/chat/session/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    """
    Archive (soft delete) a chat session
    """
    try:
        success = archive_chat_session(session_id)
        
        if success:
            return jsonify({
                "success": True,
                "message": "Chat session archived successfully"
            }), SUCCESS
        else:
            return jsonify({
                "success": False,
                "message": "Failed to archive chat session"
            }), BAD_REQUEST
    except Exception as e:
        print(f"Delete session error: {e}")
        return jsonify({
            "success": False,
            "message": "Internal server error"
        }), INTERNAL_SERVER_ERROR


# ==================== CHAT MESSAGE ROUTES ====================

@app.route('/api/chat/message/send', methods=['POST'])
def send_message():
    """
    Send a chat message and get AI response
    
    Request body:
        {
            "session_id": 1,
            "message_text": "Hello, how are you?",
            "user_id": 1
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'session_id' not in data or 'message_text' not in data or 'user_id' not in data:
            return jsonify({
                "success": False,
                "message": "Session ID, message text, and user ID are required"
            }), BAD_REQUEST
        
        session_id = data['session_id']
        message_text = data['message_text']
        user_id = data['user_id']
        
        success, result = process_chat_message(session_id, message_text, user_id)
        
        if success:
            return jsonify({
                "success": True,
                "data": result,
                "message": "Message sent successfully"
            }), CREATED
        else:
            return jsonify({
                "success": False,
                "message": result
            }), BAD_REQUEST
    except Exception as e:
        print(f"Send message error: {e}")
        return jsonify({
            "success": False,
            "message": "Internal server error"
        }), INTERNAL_SERVER_ERROR


@app.route('/api/chat/message/process', methods=['POST'])
def process_message():
    """
    Process a chat message with GPT and get AI response
    
    Request body:
        {
            "session_id": 1,
            "message_text": "Hello, how are you?",
            "user_id": 1
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'session_id' not in data or 'message_text' not in data or 'user_id' not in data:
            return jsonify({
                "success": False,
                "message": "Session ID, message text, and user ID are required"
            }), BAD_REQUEST
        
        session_id = data['session_id']
        message_text = data['message_text']
        user_id = data['user_id']
        
        # Save the user message first
        from Monolithic.db_ops.db_ops import insert_chat_message
        from Monolithic.constants.constants import MESSAGE_FROM_SYSTEM
        
        user_message_id = insert_chat_message(
            chat_session_id=session_id,
            message_text=message_text,
            message_from_id=user_id,
            message_to_id=MESSAGE_FROM_SYSTEM,
            message_created_user_id=user_id
        )
        
        if not user_message_id:
            return jsonify({
                "success": False,
                "message": "Failed to save user message"
            }), BAD_REQUEST
        
        # Process message with GPT
        from Components.gpt_tools.gpt_tools import process_message as gpt_process_message
        gpt_response = gpt_process_message(session_id, message_text)
        
        # Save the GPT response as a system message
        from Monolithic.utils.utils import save_system_response
        success, result = save_system_response(session_id, gpt_response)
        
        if success:
            return jsonify({
                "success": True,
                "data": result,
                "message": "Message processed successfully"
            }), CREATED
        else:
            return jsonify({
                "success": False,
                "message": result
            }), BAD_REQUEST
    except Exception as e:
        print(f"Process message error: {e}")
        return jsonify({
            "success": False,
            "message": "Internal server error"
        }), INTERNAL_SERVER_ERROR


@app.route('/api/chat/history/<int:session_id>', methods=['GET'])
def get_history(session_id):
    """
    Get chat history for a session
    """
    try:
        success, result = get_chat_history(session_id)
        
        if success:
            return jsonify({
                "success": True,
                "data": result,
                "count": len(result)
            }), SUCCESS
        else:
            return jsonify({
                "success": False,
                "message": result
            }), BAD_REQUEST
    except Exception as e:
        print(f"Get history error: {e}")
        return jsonify({
            "success": False,
            "message": "Internal server error"
        }), INTERNAL_SERVER_ERROR


# ==================== MAIN ====================

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Database initialized and ready")
    app.run(debug=True, host='0.0.0.0', port=5000)

