import React from 'react';

const Home = () => {
  return (
    <>
      <h1 className="text-4xl font-bold text-nu-purple mb-4">Welcome to Xpert.ai</h1>
      <p className="text-muted mb-6">
        Ask a question and we’ll match it to real expert content — papers, blogs, interviews, and more.
      </p>
      <input
        type="text"
        placeholder="Enter your question"
        className="w-full p-3 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-nu-purple"
      />
      <button className="mt-4 bg-nu-purple hover:bg-nu-purple-hover text-white font-semibold py-2 px-6 rounded">
        Get Answer
      </button>
      <p className="mt-4 text-muted text-sm">Papers, Blogs, Interviews</p>
    </>
  );
};

export default Home;
