import React, { useState } from 'react';

const Home = () => {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);

  const handleSendPrompt = async () => {
    try {
      // send api request to backend
      console.log("Button clicked!");

      // sample response placeholding for the model's generated response. ChatGPT used this format which seems pretty solid
      const mockResponse = {
        answer: "Sustainable architecture focuses on energy efficiency, material reuse, and minimizing environmental impact.",
        sources: [
          {
            title: "Green Design by Lisa Smith",
            url: "https://example.com/green-design",
            type: "academic paper"
          }
        ],
        experts: [
          {
            name: "Lisa Smith",
            affiliation: "MIT",
            expertise: ["Sustainability", "Architecture"]
          }
        ]
      }

      setResponse(mockResponse);

      // switch router to response page? not sure about this yet, maybe it will output the text on the same UI
    } catch(err) {
      console.error("Error processing user prompt:", err);
    }
  }
  return (
    <div className="text-center">
      <h1 className="text-4xl font-bold text-nu-purple mb-4">Welcome to Xpert.ai</h1>
      <p className="text-muted mb-6">
        Ask a question and we’ll match it to real expert content — papers, blogs, interviews, and more.
      </p>
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target_value)}
        placeholder="Enter your question"
        className="w-full p-3 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-nu-purple"
      />
      <button
        onClick={handleSendPrompt}
        className="mt-4 bg-nu-purple hover:bg-nu-purple-hover text-white font-semibold py-2 px-6 rounded"
      >
        Get Answer
      </button>
      <p className="mt-4 text-muted text-sm">Papers, Blogs, Interviews</p>

      {response && (
        <div className="mt-8 text-left max-w-2xl mx-auto bg-white shadow rounded p-6">
          <h2 className="text-2xl font-bold text-nu-purple mb-2">Answer</h2>
          <p className="mb-4">{response.answer}</p>

          <h3 className="font-semibold mb-1">Sources</h3>
          <ul className="list-disc list-inside text-sm mb-4">
            {response.sources.map((src, idx) => (
              <li key={idx}>
                <a href={src.url} className="text-nu-purple hover:underline" target="_blank" rel="noreferrer">
                  {src.title} ({src.type})
                </a>
              </li>
            ))}
          </ul>

          <h3>Experts</h3>
          <ul className="list-disc list-inside text-sm">
            {response.experts.map((exp, idx) => (
              <li key={idx}>
                {exp.name} – {exp.affiliation} ({exp.expertise.join(", ")})
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Home;
