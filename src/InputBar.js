import React from 'react';
import './InputBar.css'; // Define your styles for input bar here

const InputBar = ({ userInput, onInputChange, onSubmit }) => {
  return (
    <form className="inputBar" onSubmit={onSubmit}>
      <input
        type="text"
        value={userInput}
        onChange={onInputChange}
        placeholder="Type your message here..."
      />
      <button type="submit">Send</button>
    </form>
  );
};

export default InputBar;
