// Chat.js
import React from 'react';
import './Chat.css';
import MessageList from './MessageList';
import InputBox from './InputBox';

const Chat = ({ userInput, messages, onUserInput, onKeyPress, darkMode }) => {
  return (
    <div className={`chat-container${darkMode ? ' dark' : ''}`}>
      <MessageList messages={messages} />
      <InputBox
        userInput={userInput}
        onUserInput={onUserInput}
        onKeyPress={onKeyPress}
      />
    </div>
  );
};

export default Chat;