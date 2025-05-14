import React, { useState } from 'react';

const Home = () => {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSendPrompt = async () => {
    setLoading(true);
    try {
      setError(null);
      // send api request to backend
      console.log("Button clicked!");
      const res = await fetch("http://localhost:8000/api/v1/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({question: question})
      });

      if(!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || "Unknown error occurred")
      }

      const data = await res.json();

      // // sample response placeholding for the model's generated response. ChatGPT used this format which seems pretty solid
      // const mockResponse = {
      //   answer: "Sustainable architecture focuses on energy efficiency, material reuse, and minimizing environmental impact.",
      //   sources: [
      //     {
      //       title: "Green Design by Lisa Smith",
      //       url: "https://example.com/green-design",
      //       type: "academic paper"
      //     }
      //   ],
      //   experts: [
      //     {
      //       name: "Lisa Smith",
      //       affiliation: "MIT",
      //       expertise: ["Sustainability", "Architecture"]
      //     }
      //   ]
      // }

      setResponse(data);
      console.log("Received response:", data);

      // switch router to response page? not sure about this yet, maybe it will output the text on the same UI
    } catch(err) {
      console.error("Error sending user prompt:", err);
      setError(err.message || "Something went wrong.")
    }
    setLoading(false);
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
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Enter your question"
        className="w-full p-3 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-nu-purple"
      />
      {!loading && (
        <button
          onClick={handleSendPrompt}
          className="mt-4 bg-nu-purple hover:bg-nu-purple-80 text-white font-semibold py-2 px-6 rounded"
        >
          Get Answer
        </button>
      )}
      {loading && (
        <button
          className="mt-4 bg-nu-purple-60 hover:bg-nu-purple-80 text-white font-semibold py-2 px-6 rounded"
        >
          Loading...
        </button>
      )}
      <p className="mt-4 text-muted text-sm">Papers, Blogs, Interviews</p>

      {error && (
        <div className="mt-4 text-red-600 font-medium">
          {error}
        </div>
      )}

      {response && (
        <div className="mt-8 text-left max-w-2xl mx-auto bg-white shadow rounded p-6">

          <h2 className="text-2xl font-bold text-nu-purple">Experts</h2>
          <p className="text-sm italic mb-2">These are the experts that I believe have the most relevant knowledge for your question.</p>
          <ul className="list-disc list-inside text-sm mb-4">
            {response.experts.map((exp, idx) => (
              <li key={idx}>
                {exp.name} – {exp.affiliation} ({exp.expertise.join(", ")})
              </li>
            ))}
          </ul>

          <h3 className="font-semibold">Answer</h3>
          <p className="text-sm italic mb-1">Here is a sample response based on existing literature online.</p>
          <p className="mb-4">{response.answer}</p>

          <h3 className="font-semibold mb-1">Sources and Further Reading</h3>
          <ul className="list-disc list-inside text-sm mb-4">
            {response.sources.map((src, idx) => (
              <li key={idx}>
                <a href={src.url} className="text-nu-purple hover:underline" target="_blank" rel="noreferrer">
                  {src.title} ({src.type})
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Home;
