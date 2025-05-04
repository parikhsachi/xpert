// api.js
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: import.meta.env.VITE_OPENAI_API_KEY 
});

export const callOpenAi = async ({ prompt, systemPrompt }) => {
  try {
    const defaultSystemPrompt = `You are an expert knowledge assistant. For the following question, provide:
    1. A concise answer
    2. Relevant sources (academic papers, articles, etc.) with proper URLs 
    3. Experts in the field with affiliations
    Format the response as JSON with this structure:
    {
      "answer": "string",
      "sources": [{"title": "string", "url": "string", "type": "string"}],
      "experts": [{"name": "string", "affiliation": "string", "expertise": ["string"]}]
    }`;

    const response = await openai.chat.completions.create({
      model: "gpt-4",
      messages: [
        { role: "system", content: systemPrompt || defaultSystemPrompt },
        { role: "user", content: prompt }
      ],
      temperature: 0.7,
      response_format: { type: "json_object" }
    });

    return JSON.parse(response.choices[0].message.content);
  } catch (error) {
    console.error('OpenAI API Error:', error);
    throw error;
  }
};