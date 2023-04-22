import React from 'react';
import './MessageBubble.css';

const MessageBubble = ({ sender, text, isAthena }) => {
  const isUser = sender === 'user';
  const bubbleClass = isUser || !isAthena ? 'user-message' : 'athena-message';

  return (
    <div className={`message-bubble ${bubbleClass}`}>
      <p>{text}</p>
    </div>
  );
};

export default MessageBubble;