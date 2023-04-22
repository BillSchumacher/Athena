// InputBox.js
import React from 'react';
import './InputBox.css';

const InputBox = ({ userInput, onUserInput, onKeyPress }) => {
  return (
    <div className="input-container">
      <input
        type="text"
        value={userInput}
        onChange={onUserInput}
        onKeyPress={onKeyPress}
        placeholder="Type your message here..."
      />
    </div>
  );
};

export default InputBox;