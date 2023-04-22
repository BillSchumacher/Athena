// MessageList.js
import React, {useEffect, useRef} from 'react';
import './MessageList.css';
import Message from './Message';

const MessageList = ({ messages }) => {
    const messagesEndRef = useRef(null);
  
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
      };
    
      useEffect(() => {
        scrollToBottom();
      }, [messages]);
  return (
    <div className="message-list">
      {messages.map((message, index) => (
    <Message key={index} message={message} />
  ))}
  
  <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;