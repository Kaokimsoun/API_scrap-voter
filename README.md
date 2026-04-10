# 🗳️ Voter NID Lookup API

This project is a FastAPI-based service that allows users to search Cambodian voter information by NID (National ID).  
It uses:

- SQLite database (local storage)
- Selenium (web scraping from NEC website)
- FastAPI (API service)

---

## Features

- Search single or multiple NIDs
- Automatically checks local database first
- If not found → scrape from website using Selenium
- Save scraped data into SQLite database
- Reuse stored data for faster future queries

---

## Project Structure

project/
│
├── main.py # FastAPI application
├── db.py # Database logic (SQLite)
├── test_and_scrap.py # CLI testing script
├── schema.sql # Database schema
├── voters.db # SQLite database (generated)
├── requirements.txt # Python dependencies
└── README.md # Documentation


---

## ⚙️ Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv .venv

- Window:

.venv\Scripts\activate

- Mac/Linux:

source .venv/bin/activate

2. Install Dependencies

pip install -r requirements.txt

3. Setup Database

Run SQLite and execute schema:
sqlite3 voters.db
.read schema.sql

OR inside SQLite:
.open voters.db
.read schema.sql

4. Run API Server
uvicorn main:app --reload
Open browser:

http://127.0.0.1:8000/docs
📡 API Endpoints
✅ Health Check
GET /

Response:

{
  "message": "✅ Voter NID API is running",
  "endpoint": "/api/search-nid"
}
🔍 Search Multiple NIDs
POST /api/search-nid

Request:

{
  "nids": ["051491501", "123456789"]
}
🔍 Search Single NID
POST /search

Request:

{
  "nid": "051491501"
}
🧪 Run CLI Test (Without API)
python test_and_scrap.py

Input:

Enter NID(s), separated by commas: 051491501
🔄 How It Works
User sends NID(s)
System checks SQLite database
If found → return immediately
If not found → Selenium scrapes from website
Save new data into database
Return combined results

Architecture

┌─────────────────┐
│   API Request   │
│ (Client / CLI)  │
└────────┬────────┘
         │
    ┌────▼─────┐
    │ FastAPI  │
    │ (main.py)│
    └────┬─────┘
         │
    ┌────▼──────────────┐
    │ Check Database    │
    │ (db.py - SQLite)  │
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
