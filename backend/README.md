# Chat Application Backend

This is a Python Flask-based backend for a chat application with SQLite database.

## Folder Structure

```
backend/
├── Components/              # Reusable components
│   ├── gpt_tools/
│   │   └── gpt_tools.py    # AI/ML tools for processing messages
│   └── SQLlite/
│       └── sql_lite.py     # Database utilities and initialization
│
├── Monolithic/             # Main application logic
│   ├── db_ops/
│   │   └── db_ops.py       # Database CRUD operations
│   ├── utils/
│   │   └── utils.py        # Utility functions (login, signup, chat)
│   └── constants/
│       └── constants.py    # Application constants
│
├── server.py               # Flask server with API routes
├── requirements.txt        # Python dependencies
└── chat_app.db            # SQLite database (created on first run)
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    user_email TEXT UNIQUE NOT NULL,
    user_password TEXT NOT NULL,
    created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status INTEGER DEFAULT 1
)
```

### Chat Session Table
```sql
CREATE TABLE chat_session (
    chat_session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_name TEXT NOT NULL,
    session_description TEXT,
    session_created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_last_updated_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_user_id INTEGER NOT NULL,
    status INTEGER DEFAULT 1,
    FOREIGN KEY (created_user_id) REFERENCES users(user_id)
)
```

### Chat Messages Table
```sql
CREATE TABLE chat_messages (
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
```

## Setup Instructions

1. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```bash
   python server.py
   ```
   
   The server will start on `http://localhost:5000` and automatically initialize the database on first run.

## API Endpoints

### Authentication

#### POST `/api/auth/signup`
Register a new user
```json
Request:
{
    "user_name": "John Doe",
    "user_email": "user@example.com",
    "user_password": "password123"
}

Response:
{
    "success": true,
    "data": {
        "user_id": 1,
        "user_name": "John Doe",
        "user_email": "user@example.com",
        "message": "User registered successfully"
    }
}
```

#### POST `/api/auth/login`
Login user
```json
Request:
{
    "username": "user@example.com",
    "password": "password123"
}

Response:
{
    "success": true,
    "data": {
        "user_id": 1,
        "user_name": "John Doe",
        "user_email": "user@example.com",
        "status": 1
    },
    "message": "Login successful"
}
```

### User Management

#### GET `/api/user/<user_id>`
Get user information by ID

### Chat Sessions

#### POST `/api/chat/session/create`
Create a new chat session
```json
Request:
{
    "user_id": 1,
    "session_name": "My Chat Session",
    "session_description": "Description here"
}
```

#### GET `/api/chat/session/<session_id>`
Get chat session details

#### GET `/api/chat/sessions`
Get all available chat sessions

#### PUT `/api/chat/session/<session_id>`
Update chat session details

#### DELETE `/api/chat/session/<session_id>`
Archive (soft delete) a chat session

### Chat Messages

#### POST `/api/chat/message/send`
Send a chat message and get AI response
```json
Request:
{
    "session_id": 1,
    "message_text": "Hello, how are you?",
    "user_id": 1
}

Response:
{
    "success": true,
    "data": {
        "user_message_id": 1,
        "ai_message_id": 2,
        "response_text": "Processed response for: Hello, how are you?",
        "message": "Message processed successfully"
    }
}
```

#### GET `/api/chat/history/<session_id>`
Get chat history for a session

### Health Check

#### GET `/health`
Check if the server is running

## Database Operations

All database operations support:
- **Insert**: Create new records
- **Read**: Retrieve records by ID
- **Update**: Modify existing records
- **Archive**: Soft delete records (sets status to 2)

## Notes

- Passwords are hashed using SHA-256 before storage
- All timestamps are automatically managed by the database
- Status codes: 1 (Active), 0 (Inactive), 2 (Archived)
- Message IDs: 0 = System/AI, User ID = User message
- The AI processing function in `gpt_tools.py` is a placeholder and needs to be implemented

