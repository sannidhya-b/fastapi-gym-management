# 🏋️ Gym Management System — FastAPI Backend

A complete real-world FastAPI backend project built as part of the
**Innomatics Research Labs FastAPI Internship**.

## 🚀 Tech Stack
- FastAPI
- Pydantic
- Uvicorn
- Python 3.10+

## ⚙️ Setup & Run

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn Gym_Management:app --reload

# Open Swagger UI
http://127.0.0.1:8000/docs

## 📋 All 20 API Endpoints

### Day 1 - GET APIs
- GET /  → Home route
- GET /members → Get all members
- GET /trainers → Get all trainers
- GET /members/summary/stats → Member statistics

### Day 2 - POST + Pydantic
- POST /members → Register new member
- POST /trainers → Add new trainer

### Day 3 - Helper Functions
- GET /equipment → Get all equipment
- POST /equipment → Add equipment
- GET /trainers/{trainer_id} → Get trainer by ID

### Day 4 - CRUD Operations
- GET /members/{member_id} → Get member by ID
- PUT /members/{member_id} → Update member
- DELETE /members/{member_id} → Delete member

### Day 5 - Multi-Step Workflow
- POST /sessions/book → Step 1 Book session
- POST /sessions/{id}/checkin → Step 2 Check in
- POST /sessions/{id}/complete → Step 3 Complete session

### Day 6 - Search, Sort, Paginate
- GET /members/search → Search members
- GET /members/sort → Sort members
- GET /members/paginate → Paginate members
- GET /sessions → Get all sessions
- GET /members/browse → Combined search+sort+paginate

## ✅ Concepts Implemented
- GET APIs with path and query parameters
- POST APIs with Pydantic validation
- Field constraints and custom validators
- Helper functions
- Full CRUD operations
- Multi-step workflow
- Keyword search, sorting, pagination
- Combined browse endpoint

## 👨‍💻 Author
Built by Sannidhya as part of Innomatics Research Labs FastAPI Internship.

#FastAPI #Python #BackendDevelopment #InnomaticsResearchLabs