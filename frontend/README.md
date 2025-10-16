# Chat Application Frontend

A React-based frontend for the chat application with dark theme design based on Google Material Design 3.

## Features

### Authentication
- **Login Page**: Email and password input with login functionality
- **Signup Page**: Full name, email, and password with registration
- **Protected Routes**: Automatic redirection based on authentication status

### Chat Interface
- **Session Management**: Create new chat sessions with plus icon
- **Session List**: Left sidebar showing all available sessions
- **Message Display**: Chat history with user and AI message differentiation
- **Real-time Messaging**: Send messages and receive AI responses
- **Search Functionality**: Search through chat sessions

## Design System

### Colors
- **Background**: #0D0D0D (darkest)
- **Panels**: #1A1A1A (secondary dark)
- **Buttons**: #262626 (default), #333333 (hover), #404040 (active)
- **Accent**: #C82FFF (magenta)
- **Gradient**: Linear gradient from #C82FFF to #00AAFF
- **Text**: #FFFFFF (primary), #A8A8A8 (secondary)
- **Borders**: #A8A8A8 (placeholder color)

### Typography
- **Font Family**: Montserrat (Google Fonts)
- **Weights**: Regular (400), Medium (500), Semi-bold (600)
- **Sizes**: 14px (body), 16px (buttons), 28px (headings)

### Components
- **Buttons**: Rounded corners, gradient for primary actions
- **Inputs**: Rounded corners (2-4px radius), dark backgrounds
- **Cards**: Subtle borders, dark backgrounds
- **Messages**: Different styling for user vs AI messages

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Login.js & Login.css
│   │   ├── Signup.js & Signup.css
│   │   └── AIChat.js & AIChat.css
│   ├── httpClient.js
│   ├── App.js & App.css
│   └── index.js
├── package.json
└── README.md
```

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm start
   ```

3. **Build for Production**:
   ```bash
   npm run build
   ```

## API Integration

### Authentication Endpoints
- `POST /api/auth/login` - User login
- `POST /api/auth/signup` - User registration

### Chat Endpoints
- `GET /api/chat/sessions` - Get all chat sessions
- `POST /api/chat/session/create` - Create new session
- `GET /api/chat/history/<session_id>` - Get chat history
- `POST /api/chat/message/send` - Send message

### HTTP Client Configuration
The `httpClient.js` file is configured to connect to the backend server at `http://192.168.0.135:5000`.

## Features Implementation

### Login Component
- Email and password input fields
- Form validation and error handling
- API integration with backend login endpoint
- Navigation to signup page
- Automatic redirection to chat on successful login

### Signup Component
- Full name, email, and password fields
- Form validation and error handling
- API integration with backend signup endpoint
- Navigation to login page
- Automatic redirection to chat on successful registration

### AI Chat Component
- **Left Sidebar**:
  - Search functionality for sessions
  - Session list with grouping (Today, Yesterday)
  - Plus icon for creating new sessions
  - Active session highlighting
- **Main Chat Area**:
  - Message display with user/AI differentiation
  - Message input with voice and file attachment icons
  - Send button with gradient styling
  - Real-time message updates

### Responsive Design
- Mobile-friendly layout
- Flexible sidebar and main content areas
- Touch-friendly button sizes
- Optimized for various screen sizes

## Usage

1. **Start the application**: `npm start`
2. **Navigate to login**: Default route redirects to login
3. **Create account**: Click "Sign Up" to register
4. **Login**: Enter credentials to access chat
5. **Create session**: Click "+" to create new chat session
6. **Send messages**: Type and send messages to AI
7. **View history**: Click on sessions to view chat history

## Dependencies

- **React**: ^18.2.0
- **React Router DOM**: ^6.8.0
- **Axios**: ^1.6.0
- **React Scripts**: ^5.0.1

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)