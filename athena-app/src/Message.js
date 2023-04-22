// Message.js
import React from 'react';
import './Message.css';
import Avatar from './Avatar';
import MessageBubble from './MessageBubble';

const Message = ({ message, user }) => {
  const isUserMessage = message.sender === 'user' || !message.isAthena;

  return (
    <div className={`message ${isUserMessage ? 'user' : 'athena'}`}>
      {!isUserMessage && <Avatar user={{ name: 'Athena' }} />}
      <MessageBubble  sender={message.sender} text={message.text} isAthena={message.isAthena} />
      {isUserMessage && <Avatar user={user} />}
    </div>
  );
};

export default Message;