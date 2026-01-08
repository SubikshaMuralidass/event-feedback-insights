# Event Feedback Insights API

## 1️⃣ Problem Understanding & Assumptions

### 🔍 Problem Interpretation

The objective is to build a backend REST API that:

* Collects event feedback from attendees
* Stores feedback in a database
* Uses an external AI service (Gemini LLM) to generate a concise summary of feedback per event
* Exposes APIs to retrieve both raw feedback and AI-generated insights

This service acts as a bridge between a local database and a third-party AI API, demonstrating data flow handling, validation, and error resilience.

---

### 🎯 Use Case Chosen

**AI-Powered Event Feedback Summarizer**

Event organizers can quickly understand attendee sentiment without manually reading all comments.

---

### ⚠️ Assumptions

The following assumptions were made due to ambiguous or open-ended requirements:

* Feedback is text-only and written in English.
* Events already exist before feedback is submitted.
* No user authentication is required (API is internal/admin-facing).
* External AI API may be:
  * Rate-limited
  * Temporarily unavailable
* AI summaries are best-effort and not mission-critical.
* Feedback volume per event is moderate (no large-scale streaming).
* Database consistency is preferred over eventual consistency.

---

## 2️⃣ Design Decisions

### 🗄️ Database Schema

**Tables**

* `events`
* `event_feedback`
* `event_summary`

**Why this design**

* Separation of raw feedback and generated insights
* Enables regeneration of summaries without re-submitting feedback
* Indexed `event_id` for fast aggregation

**Indexing**

* `event_feedback.event_id` indexed for efficient lookups

---

### 📁 Project Structure

```
app/
├── config.py
├── crud.py
├── main.py              # FastAPI entry point
├── routes.py            # API routes
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── services/
│   └── llm.py           # Gemini integration
├── database.py          # DB session & engine
tests/
├── test_feedback.py     # pytest unit tests
├── readme.md
├── requirement.txt
├── .env.example
```

**Architecture**

* Layered architecture
* Clear separation between:

  * API layer
  * Business logic
  * External services

---

### ✅ Validation Logic

Beyond Pydantic type validation:

* Empty feedback lists are blocked early
* Invalid `event_id` returns HTTP 404
* Gemini is never called if no feedback exists
* LLM responses are sanitized before returning

---

### 🌐 External API Handling

* API key stored securely using environment variables
* Rate-limit and quota errors handled gracefully
* AI calls isolated in a service layer
* External failures do not crash the application

---

## 3️⃣ Solution Approach (Data Flow)

1. Client submits feedback for an event
2. Feedback is validated and stored in PostgreSQL
3. coordinator requests event summary
4. Backend:
   * Fetches feedback from DB
   * Sends request to Gemini API
5. AI summary returned and sent to client

---

## 4️⃣ Error Handling Strategy

### 🧯 Database Errors

* Wrapped using FastAPI exception handling
* Returns appropriate HTTP status codes

### 🤖 External API Failures

Handled scenarios:

* Rate limiting (HTTP 429)
* API downtime
* Invalid model access
* Quota exhaustion

**Strategy**

* Catch and log errors
* Return meaningful fallback responses
* Avoid retry storms

### 🛡️ Global Exception Handling

* Centralized error handling using FastAPI
* Prevents unhandled crashes
* Ensures consistent API responses

---

## 5️⃣ How to Run the Project

### 🧪 Prerequisites

* Python 3.11+
* Virtual environment
* Gemini API Key

---

### ⚙️ Setup Instructions

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### 🔐 Environment Variables

Create `.env` file:

```
DATABASE_URL=postgresql://user:password@localhost:5432/events_db
GEMINI_API_KEY=your_api_key_here
```

Example provided in `.env.example`.

---

### ▶️ Run the Server

```bash
uvicorn app.main:app --reload
```

Access Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

### 📬 Example API Calls

**Create feedback**

```bash
POST /events/{event_id}/feedback
```

**Generate summary**

```bash
POST /events/{event_id}/summary
```

---

### 🧪 Run Tests

```bash
pytest -v
```

Tests mock external AI calls to ensure deterministic results.

---
