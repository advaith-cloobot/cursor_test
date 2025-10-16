import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
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
  const navigate = useNavigate();

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
    
    const messageText = newMessage.trim();
    setNewMessage('');
    setLoading(true);
    
    // Add user message to local state immediately so it's visible
    const tempUserMessage = {
      chat_message_id: `temp_${Date.now()}`, // Temporary ID
      message_text: messageText,
      message_from_id: user.user_id,
      message_created_timestamp: new Date().toISOString(),
      isTemporary: true
    };
    setMessages(prevMessages => [...prevMessages, tempUserMessage]);
    
    try {
      // Process the message with GPT (this handles both saving user message and generating AI response)
      const response = await httpClient.post('/api/chat/message/process', {
        session_id: currentSession.chat_session_id,
        message_text: messageText,
        user_id: user.user_id
      }, {
        timeout: 60000 // 60 second timeout for GPT processing
      });
      
      if (response.data.success) {
        // Refresh messages to show both user message and AI response
        await fetchMessages(currentSession.chat_session_id);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      // Remove the temporary message on error
      setMessages(prevMessages => prevMessages.filter(msg => !msg.isTemporary));
      // Show error message to user
      alert('Failed to send message. Please try again.');
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

  const handleLogout = () => {
    // Clear user data from localStorage
    localStorage.removeItem('user');
    // Dispatch custom event to notify App component of auth change
    window.dispatchEvent(new Event('authChange'));
    // Navigate to login page
    navigate('/login');
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

        <button className="logout-btn" onClick={handleLogout}>
          <span className="logout-icon">🚪</span>
          Logout
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
                    <div className="message-text">
                      {message.message_from_id === 0 ? (
                        <ReactMarkdown>{message.message_text}</ReactMarkdown>
                      ) : (
                        message.message_text
                      )}
                    </div>
                    <div className="message-time">
                      {formatTimestamp(message.message_created_timestamp)}
                    </div>
                  </div>
                </div>
              ))}
              
              {/* Loading indicator when processing response */}
              {loading && (
                <div className="message ai-message loading-message">
                  <div className="message-content">
                    <div className="message-text">
                      <span className="loading-dots">Processing response</span>
                      <span className="loading-animation">...</span>
                    </div>
                  </div>
                </div>
              )}
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
