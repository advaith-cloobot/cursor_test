import React, { useState, useEffect } from 'react';
import httpClient from '../httpClient';
import './AIChat.css';

const AIChat = () => {
  const [sessions, setSessions] = useState([]);
  const [currentSession, setCurrentSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionsLoading, setSessionsLoading] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Get user from localStorage
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));
    }
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    setSessionsLoading(true);
    try {
      const response = await httpClient.get('/api/chat/sessions');
      if (response.data.success) {
        setSessions(response.data.data);
      }
    } catch (error) {
      console.error('Error fetching sessions:', error);
    } finally {
      setSessionsLoading(false);
    }
  };

  const fetchMessages = async (sessionId) => {
    try {
      const response = await httpClient.get(`/api/chat/history/${sessionId}`);
      if (response.data.success) {
        setMessages(response.data.data);
      }
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  const createNewSession = async () => {
    if (!user) return;
    
    try {
      const response = await httpClient.post('/api/chat/session/create', {
        user_id: user.user_id,
        session_name: 'New Chat Session',
        session_description: 'A new chat session'
      });
      
      if (response.data.success) {
        const newSession = response.data.data;
        setSessions([newSession, ...sessions]);
        setCurrentSession(newSession);
        setMessages([]);
      }
    } catch (error) {
      console.error('Error creating session:', error);
    }
  };

  const selectSession = (session) => {
    setCurrentSession(session);
    fetchMessages(session.chat_session_id);
  };

  const sendMessage = async () => {
    if (!newMessage.trim() || !currentSession || !user) return;
    
    setLoading(true);
    try {
      const response = await httpClient.post('/api/chat/message/send', {
        session_id: currentSession.chat_session_id,
        message_text: newMessage,
        user_id: user.user_id
      });
      
      if (response.data.success) {
        setNewMessage('');
        // Refresh messages to show the new ones
        fetchMessages(currentSession.chat_session_id);
      }
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="ai-chat-container">
      {/* Left Sidebar */}
      <div className="sidebar">
        <div className="sidebar-header">
          <div className="search-container">
            <input
              type="text"
              placeholder="Q Search chats"
              className="search-input"
            />
            <span className="search-icon">🔍</span>
          </div>
        </div>

        <div className="history-section">
          <div className="history-header">
            <span className="history-icon">🕐</span>
            <span className="history-label">History</span>
            <span className="history-arrow">⌄</span>
          </div>
          
          <div className="sessions-list">
            <div className="session-group">
              <div className="group-header">
                <span className="group-title">TODAY</span>
                <span className="group-arrow">⌄</span>
              </div>
              
              {sessionsLoading ? (
                <div className="loading-sessions">Loading sessions...</div>
              ) : (
                sessions.map((session) => (
                  <div
                    key={session.chat_session_id}
                    className={`session-item ${
                      currentSession?.chat_session_id === session.chat_session_id ? 'active' : ''
                    }`}
                    onClick={() => selectSession(session)}
                  >
                    <span className="session-icon">💬</span>
                    <span className="session-name">{session.session_name}</span>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        <button className="new-session-btn" onClick={createNewSession}>
          <span className="plus-icon">+</span>
          New Chat
        </button>
      </div>

      {/* Main Chat Area */}
      <div className="main-content">
        {currentSession ? (
          <>
            {/* Messages Area */}
            <div className="messages-container">
              {messages.map((message) => (
                <div
                  key={message.chat_message_id}
                  className={`message ${
                    message.message_from_id === 0 ? 'ai-message' : 'user-message'
                  }`}
                >
                  <div className="message-content">
                    <div className="message-text">{message.message_text}</div>
                    <div className="message-time">
                      {formatTimestamp(message.message_created_timestamp)}
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Message Input */}
            <div className="message-input-container">
              <div className="input-actions">
                <button className="action-btn" title="Voice input">
                  🎤
                </button>
                <button className="action-btn" title="Attach file">
                  📎
                </button>
              </div>
              <input
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type a message..."
                className="message-input"
                disabled={loading}
              />
              <button
                onClick={sendMessage}
                disabled={loading || !newMessage.trim()}
                className="send-button"
              >
                {loading ? '⏳' : '✈️'}
              </button>
            </div>
          </>
        ) : (
          <div className="no-session">
            <h2>Select a chat session to start</h2>
            <p>Choose a session from the left panel or create a new one</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default AIChat;
