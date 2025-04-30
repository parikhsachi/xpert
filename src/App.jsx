import React from 'react';
import Home from './pages/Home';

function App() {
  return (
    <div className="bg-soft-bg min-h-screen flex items-center justify-center text-gray-900 font-sans">
      <div className="bg-white p-8 rounded-lg shadow-md max-w-content w-full text-center">
        <Home />
      </div>
    </div>
  );
}

export default App;
