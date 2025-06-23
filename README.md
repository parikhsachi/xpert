# 🧠 Xpert.ai

Xpert.ai is an AI-powered expert discovery tool built to help **journalists**, **lawyers**, and **researchers** find credible subject-matter experts in seconds. By aggregating academic data and combining it with AI-generated insight, Xpert.ai delivers a ranked list of experts tailored to your query.

---

## 🚀 Features

- 🔍 **Semantic Scholar integration** for paper and author search
- 🧮 **Heuristic author selection** based on paper relevance, citation count, and author contributions
- 📊 **Author ranking algorithm** using h-index, recency, field match, and total impact
- 🏛️ **ORCID integration** for affiliation and contact details
- 🧠 **OpenAI-powered insight generator** that simulates expert perspectives
- ⚡ **FastAPI backend** and **React frontend** for seamless performance

---

## 🧱 Architecture Overview

### 🔧 Backend

The backend consists of multiple stages:

1. **Paper Search (Semantic Scholar)** – Based on the user's query, we fetch top papers.
2. **Heuristic Author Selection** – Authors of those papers are gathered and filtered using criteria like author position and number of papers.
3. **Basic Author Lookup (Semantic Scholar)** – Additional author metadata is retrieved.
4. **Affiliation Lookup (ORCID API)** – Augments profiles with institutions and contact info.
5. **Author Ranking** – Experts are scored and ranked by relevance and authority.
6. **AI Perspective (OpenAI API)** – GPT generates a plausible answer from each expert based on their research corpus.

### 🎨 Frontend

- Built in **React**, the frontend collects user input and displays interactive expert cards.
- Cards include expert name, affiliation, top publications, contact info, and an AI-generated summary.

---

## ⚙️ Tech Stack

| Layer      | Technology          |
|------------|---------------------|
| Frontend   | React, Tailwind CSS |
| Backend    | Python, FastAPI     |
| APIs       | Semantic Scholar, ORCID, OpenAI |
| Hosting    | _Insert if applicable_ |
| Deployment | Docker (optional)   |

---

## 📥 Setup & Installation

### Frontend
```bash
git clone https://github.com/parikhsachi/xpert
npm install
npm run dev
```

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### API Keys
- Create a .env file and populate it with the following
```
OPENAI_API_KEY=your_key
S2_API_KEY=your_key
```

---

## 📡 API Endpoints
| Endpoint     | Description                        |
| ------------ | ---------------------------------- |
| `/search`    | Main query route for expert search |
| `/rank`      | Applies ranking heuristic          |
| `/summarize` | Generates AI-based insight summary |

---

## 📈 Sample Output
For a query like "deepfakes in political campaigns":
| Expert          | Affiliation   | h-index | AI Perspective                                                       |
| --------------- | ------------- | ------- | -------------------------------------------------------------------- |
| Dr. Jane Doe    | MIT Media Lab | 47      | “Based on her 2023 paper on misinformation detection...”             |
| Prof. Arvind K. | Stanford HAI  | 52      | “This technology raises urgent regulatory and ethical challenges...” |

---

## 🧠 Execution Flow
1. User inputs a question or topic
2. Semantic Scholar returns top matching papers
3. Authors are selected and filtered heuristically
4. Author data is enriched via ORCID
5. Experts are ranked and scored
6. GPT generates a perspective for each expert
7. Results are rendered as expert cards in the frontend

---

## 🧑‍💻 Team
- Ian Slater – Full-stack developer, backend architecture
- Sachi Parikh – UX/UI and research
- Rahib Taher – Systems integration, ranking algorithm