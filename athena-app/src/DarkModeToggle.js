import React from 'react';
import './DarkModeToggle.css';
const DarkModeToggle = ({ darkMode, setDarkMode }) => {
  return (
    <label className="switch">
      <input
        type="checkbox"
        checked={darkMode}
        onChange={() => setDarkMode(!darkMode)}
      />
      <span className="slider"></span>
    </label>
  );
};

export default DarkModeToggle;