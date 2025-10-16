# SQL Database Schemas

This document contains the CREATE TABLE queries for all database tables.

## Table: users

```sql
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    user_email TEXT UNIQUE NOT NULL,
    user_password TEXT NOT NULL,
    created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status INTEGER DEFAULT 1
);
```

**Schema Details:**
- `user_id`: Primary key, auto-increment
- `user_name`: User's display name (text)
- `user_email`: User's email address (text, unique)
- `user_password`: Hashed password (text)
- `created_timestamp`: Timestamp when user was created
- `last_updated_timestamp`: Timestamp when user was last updated
- `status`: User status (integer) - 1=Active, 0=Inactive, 2=Archived

---

## Table: chat_session

```sql
CREATE TABLE IF NOT EXISTS chat_session (
    chat_session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_name TEXT NOT NULL,
    session_description TEXT,
    session_created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_last_updated_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_user_id INTEGER NOT NULL,
    status INTEGER DEFAULT 1,
    FOREIGN KEY (created_user_id) REFERENCES users(user_id)
);
```

**Schema Details:**
- `chat_session_id`: Primary key, auto-increment
- `session_name`: Name of the chat session (text)
- `session_description`: Description of the chat session (text)
- `session_created_timestamp`: Timestamp when session was created
- `session_last_updated_timestamp`: Timestamp when session was last updated
- `created_user_id`: Foreign key referencing users table (integer)
- `status`: Session status (integer) - 1=Active, 0=Inactive, 2=Archived

---

## Table: chat_messages

```sql
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
);
```

**Schema Details:**
- `chat_message_id`: Primary key, auto-increment
- `chat_session_id`: Foreign key referencing chat_session table (integer)
- `message_text`: The actual message content (text)
- `message_from_id`: ID of the message sender (integer) - 0=System/AI, User ID=User
- `message_to_id`: ID of the message receiver (integer) - 0=System/AI, User ID=User
- `message_created_timestamp`: Timestamp when message was created
- `message_created_user_id`: Foreign key referencing the user who created the message (integer)
- `status`: Message status (integer) - 1=Active, 0=Inactive, 2=Archived

---

## Database Operations Available

For each table, the following operations are implemented in `Monolithic/db_ops/db_ops.py`:

### Users Table
- `insert_user(user_name, user_email, user_password)` - Create new user
- `read_user(user_id)` - Read user by ID
- `read_user_by_email(user_email)` - Read user by email
- `update_user(user_id, user_name, user_email, user_password)` - Update user
- `archive_user(user_id)` - Archive (soft delete) user

### Chat Session Table
- `insert_chat_session(session_name, created_user_id, session_description)` - Create new session
- `read_chat_session(chat_session_id)` - Read session by ID
- `read_user_chat_sessions(user_id)` - Read all sessions for a user
- `update_chat_session(chat_session_id, session_name, session_description)` - Update session
- `archive_chat_session(chat_session_id)` - Archive (soft delete) session

### Chat Messages Table
- `insert_chat_message(chat_session_id, message_text, message_from_id, message_to_id, message_created_user_id)` - Create new message
- `read_chat_message(chat_message_id)` - Read message by ID
- `read_session_messages(chat_session_id)` - Read all messages for a session
- `update_chat_message(chat_message_id, message_text)` - Update message
- `archive_chat_message(chat_message_id)` - Archive (soft delete) message

