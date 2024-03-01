import React, { useState } from 'react';

import { sendMessage } from './apiService'; // Importing the API service
import Message from './Message'; // Assuming you have a Message component
import InputBar from './InputBar'; // Assuming you have an InputBar component
import './ChatApp.css'; // Make sure you create this CSS file and define styles

function ChatApp() {
  const [messages, setMessages] = useState([]);
  const [isAiTyping, setIsAiTyping] = useState(false);
  const [userInput, setUserInput] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('en-US'); // default voice messages in English
  const messagesEndRef = React.useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({behavior: "smooth" });
  }

  React.useEffect(scrollToBottom, [messages]);
  const handleInputChange = (event) => {
    setUserInput(event.target.value);
  };

  const handleLanguageChange = (event) => {
    setSelectedLanguage(event.target.value);
  }

  const handleSubmit = async (input) => {
    let inputText = userInput;
    if (input && input.preventDefault) {
      input.preventDefault();
    } else if (typeof input === "string") {
      inputText = input;
    }
    if (!inputText.trim()) return;

    const userMessage = {
      text: inputText,
      author: 'user'
    };

    setMessages(messages => [...messages, userMessage]); // Add user message to chat
    setUserInput(''); // Clearing the input field
    setIsAiTyping(true);

    try {
      const aiResponse = await sendMessage(inputText); // Sending message to API
      const aiMessage = {
        text: aiResponse.reply, // Get AI response
        author: 'ai'
      };
      setMessages(messages => [...messages, aiMessage]); // Add AI response to chat
    } catch (error) {
      console.error('Error sending message:', error);
    }
    setIsAiTyping(false); // AI stops typing after response or error
  };

  const startVoiceRecognition = () => {
    const recognition = new window.webkitSpeechRecognition() || new window.SpeechRecognition();
    // fi-FI for Finnish, en-Us for English
    recognition.lang = selectedLanguage;
    recognition.start();

    recognition.onresult = function(event) {
      const transcript = event.results[0][0].transcript;
      handleSubmit(transcript); // use transcript as input and submit
    };

    recognition.onerror = function(event) {
      console.error('Speech recognition error', event.error);
    }
  }

  return (
    <div className="ChatApp">
      <div className="messages">
        {messages.map((message, index) => (
          <Message key={index} text={message.text} author={message.author} />
        ))}
        <div ref={messagesEndRef} />
        {isAiTyping && <div className="ai-typing">AI is typing...</div>}
      </div>
      <InputBar 
        userInput={userInput} 
        onInputChange={handleInputChange} 
        onSubmit={(event) => handleSubmit(event)}
      />
      <select onChange={handleLanguageChange} value={selectedLanguage}>
        <option value="en-US">English</option>
        <option value="fi-FI">Finnish</option>
      </select>
      <button onClick={startVoiceRecognition} className="voice-command-button">🎙 Speak</button>
    </div>
  );
}

export default ChatApp;
