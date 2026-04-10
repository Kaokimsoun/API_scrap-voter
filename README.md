# 🗳️ Voter NID Lookup API

## 📖 Description

The **Voter NID Lookup API** is a backend service built with FastAPI that allows users to search Cambodian voter information using a National ID (NID).

The system is designed with a **cache-first architecture**, meaning it first checks a local SQLite database for existing records. If the requested NID is not found, the system automatically retrieves the data from the official NEC voter website using Selenium, then stores it locally for faster future access.

This approach improves performance, reduces repeated web scraping, and ensures efficient data retrieval.

---

## 🚀 Technologies Used

* SQLite (local database storage)
* Selenium (web scraping automation)
* FastAPI (REST API framework)
* Pydantic (data validation)

---

## ✨ Features

* Search single or multiple NIDs
* Automatic database caching (faster repeated queries)
* Web scraping fallback using Selenium
* Store and reuse data locally
* CLI support for testing without API
* Structured JSON response

---

## 📁 Project Structure

```
project/
│
├── main.py              # FastAPI application
├── db.py                # Database logic (SQLite)
├── test_and_scrap.py    # CLI testing script
├── schema.sql           # Database schema
├── voters.db            # SQLite database (generated)
├── requirements.txt     # Dependencies
└── README.md            # Documentation
```

---

## ⚙️ Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

**Windows**

```bash
.venv\Scripts\activate
```

**Mac/Linux**

```bash
source .venv/bin/activate
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Setup Database

```bash
sqlite3 voters.db
.read schema.sql
```

OR:

```sql
.open voters.db
.read schema.sql
```

---

### 4. Run API Server

```bash
uvicorn main:app --reload
```

Open in browser:

```
http://127.0.0.1:8000/docs
```

---

## 📡 API Endpoints

### ✅ Health Check

```
GET /
```

Response:

```json
{
  "message": "✅ Voter NID API is running",
  "endpoint": "/api/search-nid"
}
```

---

### 🔍 Search Multiple NIDs

```
POST /api/search-nid
```

Request:

```json
{
  "nids": ["051491501", "123456789"]
}
```

---

### 🔍 Search Single NID

```
POST /search
```

Request:

```json
{
  "nid": "051491501"
}
```

---

## 🧪 CLI Testing

Run without API:

```bash
python test_and_scrap.py
```

Example:

```
Enter NID(s), separated by commas: 051491501
```

---

## 🔄 How It Works

1. User sends NID(s)
2. System checks SQLite database (cache)
3. If found → return immediately
4. If not found → Selenium scrapes NEC website
5. Store new data into database
6. Return combined results

---

## 🧱 Architecture

```
┌─────────────────┐
│   API Request   │
│ (Client / CLI)  │
└────────┬────────┘
         │
    ┌────▼─────┐
    │ FastAPI  │
    └────┬─────┘
         │
    ┌────▼──────────────┐
    │ Check Database    │
    │ (SQLite Cache)    │
    └────┬───────┬──────┘
         │       │
   Cache Hit   Cache Miss
         │       │
         │       ▼
         │  ┌───────────────┐
         │  │ run_selenium  │
         │  │ (Scraper)     │
         │  └──────┬────────┘
         │         │
         │         ▼
         │  ┌───────────────┐
         │  │ NEC Website   │
         │  │ (External)    │
         │  └──────┬────────┘
         │         │
         │         ▼
         │  ┌───────────────┐
         │  │ Parsed Data   │
         │  └──────┬────────┘
         │         │
         │         ▼
         │  ┌───────────────┐
         │  │ Save to DB    │
         │  │ (insert_to_db)│
         │  └──────┬────────┘
         │         │
         └─────────┴──────────────┐
                                  ▼
                        ┌────────────────┐
                        │ Return Response│
                        │ (JSON Output)  │
                        └────────────────┘
```

---

## ⚠️ Notes

* Requires Google Chrome installed
* ChromeDriver must match your Chrome version
* You can enable headless mode in `main.py` for better performance

---
