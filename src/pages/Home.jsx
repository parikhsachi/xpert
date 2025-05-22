import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const Home = () => {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeExpert, setActiveExpert] = useState(null);

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

      setResponse(data);
      console.log("Received response:", data);

      // scroll to response
      setTimeout(() => {
        document.getElementById("results")?.scrollIntoView({ behavior: "smooth" });
      }, 400); // matches transition duration
    } catch(err) {
      console.error("Error sending user prompt:", err);
      setError(err.message || "Something went wrong.")
    }
    setLoading(false);
  }
  return (
    <div className="w-full text-center p-8">
      <h1 className="text-4xl font-bold text-nu-purple mb-4">Welcome to Xpert.ai</h1>
      <p className="text-muted mb-6">
        Ask a question and we’ll match it to real expert insight — backed by research, publications, and profiles.
      </p>
      <div className="w-full mx-auto max-w-4xl">
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
        <p className="mt-4 text-muted text-sm">Credible. Cited. Concise.</p>

        {error && (
          <div className="mt-4 text-red-600 font-medium">
            {error}
          </div>
        )}
      </div>

      <AnimatePresence>
        {response && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            transition={{ duration: 0.4 }}
            className="bg-white mt-8 text-left mx-auto px-6 py-8 shadow-md hover:shadow-lg border border-gray-300 rounded"
          >
            <div className="text-center">
              <h2 className="text-2xl font-bold text-nu-purple mb-2">Matched Experts</h2>
              <p className="text-sm italic mb-6">Here are some experts that may be relevant to your query. Scroll to see each expert's publications, sample viewpoint on the topic, and contact info.</p>
              {response.error && (
                <div className="mt-4 text-red-600 font-medium">
                  {response.error}
                </div>
              )}
            </div>

            <div id="results" className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-x-6 gap-y-8">
              {response.experts.map((expert, idx) => (
                <div
                  key={idx}
                  className="bg-white shadow-md rounded p-6 border border-gray-300 cursor-pointer hover:shadow-xl transition"
                  onClick={() => setActiveExpert(expert)}
                >
                  <h3 className="text-xl font-semibold text-nu-purple mb-1">{expert.name}</h3>
                  <p className="text-sm text-gray-600 mb-2">
                    Fields: {expert.expertise?.length ? expert.expertise.join(', ') : 'Not available'}
                  </p>
                  <p className="text-sm mb-4">H-Index: {expert.hIndex}</p>
                  <p className="text-sm text-gray-600 mb-2">Click to expand...</p>
                </div>
              ))}
            </div>
            {activeExpert && (
              <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                <div className="bg-white max-w-lg sm:max-w-xl md:max-w-2xl lg:max-w-4xl xl:max-w-6xl w-full p-6 rounded shadow-lg relative overflow-y-auto max-h-[90vh]">
                  <button
                    onClick={() => setActiveExpert(null)}
                    className="absolute top-3 right-3 text-gray-600 hover:text-gray-800 text-xl"
                  >
                    ×
                  </button>
                  <h3 className="text-2xl font-semibold text-nu-purple mb-1">
                    <a href={activeExpert.url} target="_blank" rel="noreferrer" className="hover:underline">
                      {activeExpert.name}
                    </a>
                  </h3>
                  <p className="text-sm text-gray-600 mb-2">
                    Fields: {activeExpert.expertise?.length ? activeExpert.expertise.join(', ') : 'Not available'}
                  </p>
                  <p className="text-sm mb-4">H-Index: {activeExpert.hIndex}</p>

                  <p className="text-sm font-medium mb-1">Affiliations:</p>
                  <ul className="list-disc list-inside text-sm mb-4">
                    {activeExpert.affiliations.map((affiliation, j) => (
                      <li key={j}>{affiliation}</li>
                    ))}
                  </ul>

                  <p className="text-sm text-gray-800 mb-2 italic">Sample Perspective:</p>
                  <p className="text-sm mb-4">{activeExpert.answer}</p>

                  <p className="text-sm font-medium mb-1">Key Publications:</p>
                  <ul className="list-disc list-inside text-sm mb-4">
                    {activeExpert.papers.map((paper, j) => (
                      <li key={j}>
                        <a href={paper.url} target="_blank" rel="noreferrer" className="text-nu-purple hover:underline">
                          {paper.title} ({paper.venue || 'unknown venue'}, {paper.year}, {paper.citationCount} citations)
                        </a>
                      </li>
                    ))}
                  </ul>

                  <p className="text-sm font-medium mb-1">Contact Info:</p>
                  <div className="text-sm text-gray-700 space-y-1">
                    {activeExpert.contact.emails?.length > 0 && (
                      <div>
                        <span className="font-semibold">Emails:</span>{' '}
                        {activeExpert.contact.emails.map((email, i) => (
                          <span key={i} className="block text-blue-700 underline">{email}</span>
                        ))}
                      </div>
                    )}
                    {activeExpert.contact["researcher-urls"]?.length > 0 && (
                      <div>
                        <span className="font-semibold">Websites:</span>
                        {activeExpert.contact["researcher-urls"].map((site, i) => (
                          <a key={i} href={site.url} target="_blank" rel="noreferrer" className="block text-blue-700 underline">
                            {site.name || site.url}
                          </a>
                        ))}
                      </div>
                    )}
                    {activeExpert.contact["external-identifiers"]?.length > 0 && (
                      <div>
                        <span className="font-semibold">Profiles:</span>
                        {activeExpert.contact["external-identifiers"].map((id, i) => (
                          <a key={i} href={id.url} target="_blank" rel="noreferrer" className="block text-blue-700 underline">
                            {id.name || id.url}
                          </a>
                        ))}
                      </div>
                    )}
                    {(!activeExpert.contact.emails?.length && !activeExpert.contact["researcher-urls"]?.length && !activeExpert.contact["external-identifiers"]?.length) && (
                      <p className="italic text-gray-500">No contact info available.</p>
                    )}
                  </div>
                </div>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default Home;
