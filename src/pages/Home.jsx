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

      setResponse(data);
      console.log("Received response:", data);

      // scroll to response
      document.getElementById("results")?.scrollIntoView({ behavior: "smooth" });
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
        <div className="mt-8 text-left mx-auto max-w-screen-xl px-4">
          <h2 className="text-2xl font-bold text-nu-purple mb-2">Matched Experts</h2>
          <p className="text-sm italic mb-6">Here are some experts that may be relevant to your query. Scroll to see each expert's publications, sample viewpoint on the topic, and contact info.</p>

          
          {response.error && (
            <div className="mt-4 text-red-600 font-medium">
              {response.error}
            </div>
          )}

          <div id="results" className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-x-6 gap-y-8">
            {response.experts.map((expert, idx) => (
              <div key={idx} className="bg-white shadow-md rounded p-6 border border-gray-200">
                <h3 className="text-xl font-semibold text-nu-purple mb-1">
                  <a href={expert.url} target="_blank" rel="noreferrer" className="hover:underline">
                    {expert.name}
                  </a>
                </h3>
                <p className="text-sm text-gray-600 mb-2">
                  Field{expert.expertise?.length > 1 || expert.expertise[0] == "No explicit fields of expertise found." ? 's' : ''}: {expert.expertise?.length ? expert.expertise.join(', ') : 'Not available'}
                </p>

                <p className="text-sm mb-4">H-Index: {expert.hIndex}</p>

                <p className="text-sm font-medium mb-1">Affiliations:</p>
                <ul className="list-disc list-inside text-sm mb-4">
                  {expert.affiliations.map((affiliation, j) => (
                    <li key={j}>{affiliation}</li>
                  ))}
                </ul>

                <p className="text-sm text-gray-800 mb-2 italic">Sample Perspective:</p>
                <p className="text-sm mb-4">{expert.answer}</p>

                <p className="text-sm font-medium mb-1">Key Publications:</p>
                <ul className="list-disc list-inside text-sm mb-4">
                  {expert.papers.map((paper, j) => (
                    <li key={j}>
                      <a href={paper.url} target="_blank" rel="noreferrer" className="text-nu-purple hover:underline">
                        {paper.title} ({paper.venue || 'unknown venue'}, {paper.year}, {paper.citationCount} citations)
                      </a>
                    </li>
                  ))}
                </ul>

                <p className="text-sm font-medium mb-1">Contact Info:</p>
                {expert.contact && (
                  <div className="text-sm text-gray-700 space-y-1">
                    {expert.contact.emails?.length > 0 && (
                      <div>
                        <span className="font-semibold">Emails:</span>{' '}
                        {expert.contact.emails.map((email, i) => (
                          <span key={i} className="block text-blue-700 underline">{email}</span>
                        ))}
                      </div>
                    )}
                    {expert.contact["researcher-urls"]?.length > 0 && (
                      <div>
                        <span className="font-semibold">Websites:</span>
                        {expert.contact["researcher-urls"].map((site, i) => (
                          <a key={i} href={site.url} target="_blank" rel="noreferrer" className="block text-blue-700 underline">
                            {site.name || site.url}
                          </a>
                        ))}
                      </div>
                    )}
                    {expert.contact["external-identifiers"]?.length > 0 && (
                      <div>
                        <span className="font-semibold">Profiles:</span>
                        {expert.contact["external-identifiers"].map((id, i) => (
                          <a key={i} href={id.url} target="_blank" rel="noreferrer" className="block text-blue-700 underline">
                            {id.name || id.url}
                          </a>
                        ))}
                      </div>
                    )}
                    {(!expert.contact.emails?.length && !expert.contact["researcher-urls"]?.length && !expert.contact["external-identifiers"]?.length) && (
                      <p className="italic text-gray-500">No contact info available.</p>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;
