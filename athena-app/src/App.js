import './App.css';
import React, { useState } from 'react';
import DarkModeToggle from './DarkModeToggle';
import Chat from './Chat';


function App() {

  const [darkMode, setDarkMode] = useState(false);
  const [userInput, setUserInput] = useState('');
  const [messages, setMessages] = useState([]);
  const handleUserInput = (e) => {
    setUserInput(e.target.value);
  };
  const sendMessage = async () => {
    // Append the user message to the message list
    const userMessage = { text: userInput, isAthena: false };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    // Fetch the response from Athena's API
    const response = await fetch('http://localhost:5000/api/v1/athena', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ input: userInput }),
    });
    const data = await response.json();


    const athenaMessage = { text: data.response, isAthena: true };
    setMessages((prevMessages) => [...prevMessages, athenaMessage]);
    setUserInput('');
  };
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };
  return (
      <div className={`App-chat-container${darkMode ? ' dark' : ''}`}> 
      <div><DarkModeToggle darkMode={darkMode} setDarkMode={setDarkMode} /></div>     <Chat
      userInput={userInput}
      messages={messages}
      onUserInput={handleUserInput}
      onKeyPress={handleKeyPress}
      darkMode={darkMode}
    />
      </div>
  );
}

export default App;
