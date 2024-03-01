// Message.js
import React from 'react';
import ReactMarkdown from 'react-markdown';
import './Message.css'; // Ensure you have this CSS file with the styles for .message-user and .message-ai

const Message = ({ text, author }) => {
  const messageClass = author === 'user' ? 'message-user' : 'message-ai';

  return (
    <div className={`message ${messageClass}`}>
      <ReactMarkdown>{text}</ReactMarkdown>
    </div>
  );
};

export default Message;
