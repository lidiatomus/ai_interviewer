# AI Interviewer

An AI-powered full-stack web application that generates interview questions based on a chosen topic, collects user responses, and produces an intelligent summary with sentiment and keywords.

---

## Features

- Generate interview questions using OpenAI
- Interactive question-by-question interview flow
- Store interview data in PostgreSQL
- AI-generated summary of responses
- Sentiment analysis and keyword extraction
- Export interview results as JSON
- Full Docker Compose setup for easy deployment

---

## Tech Stack

### Backend
- FastAPI
- PostgreSQL
- OpenAI API

### Frontend
- React (Vite)
- JavaScript (JSX)

### DevOps
- Docker
- Docker Compose

---

## Project Structure

```

ai_interviewer/
│
├── backend/
│   ├── app/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md

```

---

## Environment Variables

Create a file:

```

backend/.env

```

Based on:

```

DATABASE_URL=postgresql://postgres:postgres@db:5432/ai_interviewer
OPENAI_API_KEY=your_openai_api_key_here

````

---

## Run with Docker (Recommended)

### 1. Make sure Docker is installed and running

### 2. From project root:

```bash
docker compose up --build
````

### 3. Open the app:

* Frontend → [http://localhost:5173](http://localhost:5173)
* Backend docs → [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Run Locally (without Docker)

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## How It Works

1. User selects a topic
2. Backend generates interview questions using OpenAI
3. User answers questions step-by-step
4. Responses are stored in PostgreSQL
5. After completion:

   * AI generates summary
   * Sentiment is analyzed
   * Keywords are extracted
6. Results are displayed and exported as JSON

---

## 📌 Notes

* The OpenAI API key is required to generate questions and summaries
* The `.env` file is not committed for security reasons
* Docker Compose ensures the app runs consistently across environments

---

## 👩‍💻 Author

Lidia Tomus

