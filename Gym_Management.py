from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime

app = FastAPI(
    title="🏋️ Gym Management System",
    description=(
        "A complete FastAPI backend for managing gym members, trainers, "
        "equipment, and workout sessions.\n\n"
        "**Internship Final Project — Innomatics Research Labs**\n\n"
        "Covers Day 1–6: GET APIs · POST + Pydantic · Helper Functions · "
        "CRUD · Multi-Step Workflow · Search / Sort / Pagination."
    ),
    version="1.0.0",
)

# ─────────────────────────────────────────────────────────────────────────────
# IN-MEMORY DATA STORE
# ─────────────────────────────────────────────────────────────────────────────

members = [
    {"id": 1, "name": "Aarav Sharma",  "age": 25, "email": "aarav@gmail.com",  "plan": "monthly",   "active": True,  "joined": "2024-01-10"},
    {"id": 2, "name": "Priya Mehta",   "age": 30, "email": "priya@gmail.com",  "plan": "quarterly", "active": True,  "joined": "2024-02-15"},
    {"id": 3, "name": "Rohan Verma",   "age": 22, "email": "rohan@gmail.com",  "plan": "yearly",    "active": False, "joined": "2023-11-01"},
    {"id": 4, "name": "Sneha Patil",   "age": 28, "email": "sneha@gmail.com",  "plan": "monthly",   "active": True,  "joined": "2024-03-05"},
    {"id": 5, "name": "Karan Singh",   "age": 35, "email": "karan@gmail.com",  "plan": "yearly",    "active": True,  "joined": "2023-09-20"},
]

trainers = [
    {"id": 1, "name": "Vikram Joshi",  "specialty": "Strength Training",  "experience_years": 8, "available": True},
    {"id": 2, "name": "Nisha Kapoor",  "specialty": "Yoga & Flexibility", "experience_years": 5, "available": True},
    {"id": 3, "name": "Arjun Desai",   "specialty": "Cardio & HIIT",      "experience_years": 6, "available": False},
    {"id": 4, "name": "Meera Nair",    "specialty": "Zumba & Dance",      "experience_years": 4, "available": True},
]

equipment_list = [
    {"id": 1, "name": "Treadmill",      "category": "Cardio",    "quantity": 10, "status": "good"},
    {"id": 2, "name": "Bench Press",    "category": "Strength",  "quantity": 5,  "status": "good"},
    {"id": 3, "name": "Dumbbells Set",  "category": "Strength",  "quantity": 20, "status": "good"},
    {"id": 4, "name": "Cycling Bike",   "category": "Cardio",    "quantity": 8,  "status": "maintenance"},
    {"id": 5, "name": "Pull-up Bar",    "category": "Strength",  "quantity": 4,  "status": "good"},
    {"id": 6, "name": "Rowing Machine", "category": "Cardio",    "quantity": 3,  "status": "good"},
]

sessions = [
    {"id": 1, "member_id": 1, "trainer_id": 1, "date": "2025-07-01", "duration_minutes": 60, "type": "Strength Training", "status": "completed"},
    {"id": 2, "member_id": 2, "trainer_id": 2, "date": "2025-07-02", "duration_minutes": 45, "type": "Yoga",             "status": "completed"},
    {"id": 3, "member_id": 4, "trainer_id": 3, "date": "2025-07-03", "duration_minutes": 30, "type": "HIIT",             "status": "cancelled"},
]

member_id_counter    = 6
trainer_id_counter   = 5
equipment_id_counter = 7
session_id_counter   = 4


# ─────────────────────────────────────────────────────────────────────────────
# PYDANTIC MODELS
# ─────────────────────────────────────────────────────────────────────────────

class MemberCreate(BaseModel):
    name:  str = Field(..., min_length=2, max_length=50, description="Full name")
    age:   int = Field(..., ge=15, le=80,                description="Age between 15 and 80")
    email: str = Field(...,                              description="Valid email address")
    plan:  str = Field(...,                              description="monthly | quarterly | yearly")

    @field_validator("plan")
    @classmethod
    def validate_plan(cls, v):
        allowed = ["monthly", "quarterly", "yearly"]
        if v.lower() not in allowed:
            raise ValueError(f"Plan must be one of: {allowed}")
        return v.lower()

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if "@" not in v or "." not in v:
            raise ValueError("Invalid email format")
        return v.lower()


class MemberUpdate(BaseModel):
    name:   Optional[str]  = Field(None, min_length=2, max_length=50)
    age:    Optional[int]  = Field(None, ge=15, le=80)
    email:  Optional[str]  = None
    plan:   Optional[str]  = None
    active: Optional[bool] = None


class TrainerCreate(BaseModel):
    name:             str = Field(..., min_length=2, max_length=50)
    specialty:        str = Field(..., description="E.g. Yoga, Cardio, Strength Training")
    experience_years: int = Field(..., ge=1, le=40)


class EquipmentCreate(BaseModel):
    name:     str = Field(..., min_length=2)
    category: str = Field(..., description="Cardio or Strength")
    quantity: int = Field(..., ge=1)
    status:   str = Field(default="good", description="good or maintenance")

    @field_validator("category")
    @classmethod
    def validate_category(cls, v):
        allowed = ["cardio", "strength"]
        if v.lower() not in allowed:
            raise ValueError(f"Category must be one of {allowed}")
        return v.capitalize()


class SessionCreate(BaseModel):
    member_id:        int = Field(..., ge=1)
    trainer_id:       int = Field(..., ge=1)
    date:             str = Field(..., description="Date in YYYY-MM-DD format")
    duration_minutes: int = Field(..., ge=15, le=180)
    type:             str = Field(..., description="Workout type e.g. Yoga, HIIT, Strength")


# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def find_member(member_id: int):
    return next((m for m in members if m["id"] == member_id), None)

def find_trainer(trainer_id: int):
    return next((t for t in trainers if t["id"] == trainer_id), None)

def find_equipment(equipment_id: int):
    return next((e for e in equipment_list if e["id"] == equipment_id), None)

def find_session(session_id: int):
    return next((s for s in sessions if s["id"] == session_id), None)

def calculate_plan_price(plan: str) -> float:
    prices = {"monthly": 999.0, "quarterly": 2699.0, "yearly": 8999.0}
    return prices.get(plan.lower(), 0.0)

def filter_members(
    keyword: Optional[str]  = None,
    plan:    Optional[str]  = None,
    active:  Optional[bool] = None,
) -> list:
    result = members[:]
    if keyword is not None:
        kw = keyword.lower()
        result = [m for m in result if kw in m["name"].lower() or kw in m["email"].lower()]
    if plan is not None:
        result = [m for m in result if m["plan"] == plan.lower()]
    if active is not None:
        result = [m for m in result if m["active"] == active]
    return result


# =============================================================================
#  ⚠️  ROUTE ORDERING RULE (Very Important in FastAPI)
#
#  FastAPI matches routes TOP TO BOTTOM.
#  Fixed routes like /members/search  must come BEFORE
#  variable routes like /members/{member_id}
#
#  Correct order for /members:
#    1. GET  /members                 ← list all
#    2. GET  /members/summary/stats   ← fixed
#    3. GET  /members/search          ← fixed
#    4. GET  /members/sort            ← fixed
#    5. GET  /members/paginate        ← fixed
#    6. GET  /members/browse          ← fixed
#    7. GET  /members/{member_id}     ← variable (LAST)
#    8. PUT  /members/{member_id}
#    9. DELETE /members/{member_id}
# =============================================================================


# ─────────────────────────────────────────────────────────────────────────────
#  DAY 1 — GET APIs
# ─────────────────────────────────────────────────────────────────────────────

# Q1 — Home Route
@app.get("/", tags=["Day 1 - GET APIs"])
def home():
    """Welcome route — overview of all available endpoints."""
    return {
        "message": "🏋️ Welcome to the Gym Management System API",
        "version": "1.0.0",
        "swagger_docs": "http://127.0.0.1:8000/docs",
        "endpoints": {
            "members":   "/members",
            "trainers":  "/trainers",
            "equipment": "/equipment",
            "sessions":  "/sessions",
        },
    }


# Q2 — List All Members
@app.get("/members", tags=["Day 1 - GET APIs"])
def get_all_members():
    """Return the full list of gym members."""
    return {"total": len(members), "members": members}


# Q3 — List All Trainers
@app.get("/trainers", tags=["Day 1 - GET APIs"])
def get_all_trainers(
    available: Optional[bool] = Query(None, description="true=available only"),
):
    """Return all trainers. Optional availability filter."""
    result = trainers if available is None else [t for t in trainers if t["available"] == available]
    return {"total": len(result), "trainers": result}


# Q4 — Member Summary Stats
# ✅ FIXED ROUTE — declared before /members/{member_id}
@app.get("/members/summary/stats", tags=["Day 1 - GET APIs"])
def member_summary():
    """Summary: total, active/inactive counts, plan breakdown and pricing."""
    total        = len(members)
    active_count = sum(1 for m in members if m["active"])
    plans: dict  = {}
    for m in members:
        plans[m["plan"]] = plans.get(m["plan"], 0) + 1
    return {
        "total_members":    total,
        "active_members":   active_count,
        "inactive_members": total - active_count,
        "plan_breakdown":   plans,
        "plan_prices_inr":  {"monthly": 999, "quarterly": 2699, "yearly": 8999},
    }


# ─────────────────────────────────────────────────────────────────────────────
#  DAY 2 — POST + Pydantic Validation
# ─────────────────────────────────────────────────────────────────────────────

# Q5 — Register New Member
@app.post("/members", status_code=201, tags=["Day 2 - POST + Pydantic"])
def register_member(member: MemberCreate):
    """
    Register a new gym member with full Pydantic validation.
    - name: 2–50 chars | age: 15–80 | email: unique + valid | plan: monthly/quarterly/yearly
    """
    global member_id_counter
    if any(m["email"] == member.email for m in members):
        raise HTTPException(status_code=400, detail="Email already registered")
    new_member = {
        "id":     member_id_counter,
        "name":   member.name,
        "age":    member.age,
        "email":  member.email,
        "plan":   member.plan,
        "active": True,
        "joined": str(date.today()),
    }
    members.append(new_member)
    member_id_counter += 1
    return {
        "message":        "✅ Member registered successfully",
        "member":         new_member,
        "plan_price_inr": calculate_plan_price(member.plan),
    }


# Q6 — Add New Trainer
@app.post("/trainers", status_code=201, tags=["Day 2 - POST + Pydantic"])
def add_trainer(trainer: TrainerCreate):
    """Add a new trainer. name: 2–50 chars | experience_years: 1–40"""
    global trainer_id_counter
    new_trainer = {
        "id":               trainer_id_counter,
        "name":             trainer.name,
        "specialty":        trainer.specialty,
        "experience_years": trainer.experience_years,
        "available":        True,
    }
    trainers.append(new_trainer)
    trainer_id_counter += 1
    return {"message": "✅ Trainer added successfully", "trainer": new_trainer}


# ─────────────────────────────────────────────────────────────────────────────
#  DAY 3 — Helper Functions + Query Parameters
# ─────────────────────────────────────────────────────────────────────────────

# Q7 — Get All Equipment (with Query filters)
@app.get("/equipment", tags=["Day 3 - Helper Functions"])
def get_all_equipment(
    category: Optional[str] = Query(None, description="Cardio or Strength"),
    status:   Optional[str] = Query(None, description="good or maintenance"),
):
    """Return all equipment. Uses is not None Query() filter checks."""
    result = equipment_list[:]
    if category is not None:
        result = [e for e in result if e["category"].lower() == category.lower()]
    if status is not None:
        result = [e for e in result if e["status"].lower() == status.lower()]
    return {"total": len(result), "equipment": result}


# Q8 — Add New Equipment
@app.post("/equipment", status_code=201, tags=["Day 3 - Helper Functions"])
def add_equipment(item: EquipmentCreate):
    """Add new gym equipment. Category validated (Cardio/Strength)."""
    global equipment_id_counter
    new_item = {
        "id":       equipment_id_counter,
        "name":     item.name,
        "category": item.category,
        "quantity": item.quantity,
        "status":   item.status,
    }
    equipment_list.append(new_item)
    equipment_id_counter += 1
    return {"message": "✅ Equipment added successfully", "equipment": new_item}


# Q9 — Get Trainer by ID (uses find_trainer() helper)
@app.get("/trainers/{trainer_id}", tags=["Day 3 - Helper Functions"])
def get_trainer_by_id(trainer_id: int):
    """Find trainer by ID using find_trainer() helper. Returns 404 if not found."""
    trainer = find_trainer(trainer_id)
    if not trainer:
        raise HTTPException(status_code=404, detail=f"Trainer ID {trainer_id} not found")
    return trainer


# ─────────────────────────────────────────────────────────────────────────────
#  DAY 6 — Advanced: Search · Sort · Paginate · Browse
#  ✅ ALL FIXED ROUTES — must be declared BEFORE /members/{member_id}
# ─────────────────────────────────────────────────────────────────────────────

# Q16 — Search Members
# ✅ FIXED ROUTE — declared before /members/{member_id}
@app.get("/members/search", tags=["Day 6 - Search, Sort, Paginate"])
def search_members(
    keyword: str            = Query(..., min_length=1, description="Search by name or email"),
    plan:    Optional[str]  = Query(None,              description="Filter by plan"),
    active:  Optional[bool] = Query(None,              description="Filter by active status"),
):
    """Search members by keyword. Uses filter_members() helper with is not None checks."""
    result = filter_members(keyword=keyword, plan=plan, active=active)
    if not result:
        raise HTTPException(status_code=404, detail=f"No members found matching '{keyword}'")
    return {"total": len(result), "members": result}


# Q17 — Sort Members
# ✅ FIXED ROUTE — declared before /members/{member_id}
@app.get("/members/sort", tags=["Day 6 - Search, Sort, Paginate"])
def sort_members(
    sort_by: str = Query("name", description="Sort field: name | age | plan | joined"),
    order:   str = Query("asc",  description="asc or desc"),
):
    """Sort all members by a chosen field in ascending or descending order."""
    valid_fields = ["name", "age", "plan", "joined"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"sort_by must be one of {valid_fields}")
    if order.lower() not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="order must be 'asc' or 'desc'")
    sorted_members = sorted(members, key=lambda m: m[sort_by], reverse=(order.lower() == "desc"))
    return {
        "sorted_by": sort_by,
        "order":     order,
        "total":     len(sorted_members),
        "members":   sorted_members,
    }


# Q18 — Paginate Members
# ✅ FIXED ROUTE — declared before /members/{member_id}
@app.get("/members/paginate", tags=["Day 6 - Search, Sort, Paginate"])
def paginate_members(
    page:     int = Query(1, ge=1,        description="Page number (starts at 1)"),
    per_page: int = Query(2, ge=1, le=20, description="Records per page (max 20)"),
):
    """Paginate the members list."""
    total       = len(members)
    total_pages = max(1, (total + per_page - 1) // per_page)
    start       = (page - 1) * per_page
    paginated   = members[start: start + per_page]
    if not paginated:
        raise HTTPException(status_code=404, detail=f"Page {page} has no data")
    return {
        "page":        page,
        "per_page":    per_page,
        "total":       total,
        "total_pages": total_pages,
        "members":     paginated,
    }


# Q20 — Combined Browse (Search + Sort + Paginate)
# ✅ FIXED ROUTE — declared before /members/{member_id}
@app.get("/members/browse", tags=["Day 6 - Search, Sort, Paginate"])
def browse_members(
    keyword:  Optional[str]  = Query(None,  description="Search keyword (name or email)"),
    plan:     Optional[str]  = Query(None,  description="Filter by plan"),
    active:   Optional[bool] = Query(None,  description="Filter by active status"),
    sort_by:  str  = Query("name", description="Sort field: name | age | plan | joined"),
    order:    str  = Query("asc",  description="asc or desc"),
    page:     int  = Query(1,  ge=1,        description="Page number"),
    per_page: int  = Query(2,  ge=1, le=20, description="Records per page"),
):
    """Combined endpoint — Search + Sort + Paginate in one call."""
    # Step 1 — Filter
    result = filter_members(keyword=keyword, plan=plan, active=active)
    # Step 2 — Sort
    valid_fields = ["name", "age", "plan", "joined"]
    if sort_by in valid_fields:
        result = sorted(result, key=lambda m: m[sort_by], reverse=(order.lower() == "desc"))
    # Step 3 — Paginate
    total       = len(result)
    total_pages = max(1, (total + per_page - 1) // per_page)
    start       = (page - 1) * per_page
    paginated   = result[start: start + per_page]
    return {
        "filters":    {"keyword": keyword, "plan": plan, "active": active},
        "sorting":    {"sort_by": sort_by, "order": order},
        "pagination": {"page": page, "per_page": per_page, "total": total, "total_pages": total_pages},
        "members":    paginated,
    }


# ─────────────────────────────────────────────────────────────────────────────
#  DAY 4 — CRUD Operations
#  ✅ VARIABLE ROUTES — declared AFTER all fixed /members/* routes above
# ─────────────────────────────────────────────────────────────────────────────

# Q3b — Get Member by ID
# ✅ VARIABLE ROUTE — placed after all fixed routes
@app.get("/members/{member_id}", tags=["Day 1 - GET APIs"])
def get_member_by_id(member_id: int):
    """Get a single member by ID. Returns 404 if not found."""
    member = find_member(member_id)
    if not member:
        raise HTTPException(status_code=404, detail=f"Member ID {member_id} not found")
    return member


# Q10 — Update Member
@app.put("/members/{member_id}", tags=["Day 4 - CRUD Operations"])
def update_member(member_id: int, updates: MemberUpdate):
    """Update member fields. Only provided fields are changed. Returns 404 if not found."""
    member = find_member(member_id)
    if not member:
        raise HTTPException(status_code=404, detail=f"Member ID {member_id} not found")
    if updates.name   is not None: member["name"]   = updates.name
    if updates.age    is not None: member["age"]     = updates.age
    if updates.email  is not None: member["email"]   = updates.email.lower()
    if updates.plan   is not None: member["plan"]    = updates.plan.lower()
    if updates.active is not None: member["active"]  = updates.active
    return {"message": "✅ Member updated successfully", "member": member}


# Q11 — Delete Member
@app.delete("/members/{member_id}", tags=["Day 4 - CRUD Operations"])
def delete_member(member_id: int):
    """Delete a gym member by ID. Returns 404 if not found."""
    member = find_member(member_id)
    if not member:
        raise HTTPException(status_code=404, detail=f"Member ID {member_id} not found")
    members.remove(member)
    return {"message": f"🗑️ Member '{member['name']}' (ID {member_id}) deleted successfully"}


# Q12 — Delete Equipment
@app.delete("/equipment/{equipment_id}", tags=["Day 4 - CRUD Operations"])
def delete_equipment(equipment_id: int):
    """Delete gym equipment by ID. Returns 404 if not found."""
    item = find_equipment(equipment_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Equipment ID {equipment_id} not found")
    equipment_list.remove(item)
    return {"message": f"🗑️ Equipment '{item['name']}' deleted successfully"}


# ─────────────────────────────────────────────────────────────────────────────
#  DAY 5 — Multi-Step Workflow: Book ➜ Check-In ➜ Complete
# ─────────────────────────────────────────────────────────────────────────────

# Q13 — STEP 1: Book a Session
# ✅ FIXED ROUTE /sessions/book — declared before /sessions/{session_id}/*
@app.post("/sessions/book", status_code=201, tags=["Day 5 - Multi-Step Workflow"])
def book_session(session: SessionCreate):
    """
    STEP 1 of 3 — Book a gym session.
    Checks member is active and trainer is available.
    Status → booked | Next: POST /sessions/{id}/checkin
    """
    global session_id_counter
    member  = find_member(session.member_id)
    trainer = find_trainer(session.trainer_id)
    if not member:
        raise HTTPException(status_code=404, detail=f"Member ID {session.member_id} not found")
    if not member["active"]:
        raise HTTPException(status_code=400, detail="Member is inactive. Please renew membership.")
    if not trainer:
        raise HTTPException(status_code=404, detail=f"Trainer ID {session.trainer_id} not found")
    if not trainer["available"]:
        raise HTTPException(status_code=400, detail=f"Trainer '{trainer['name']}' is unavailable")
    new_session = {
        "id":               session_id_counter,
        "member_id":        session.member_id,
        "trainer_id":       session.trainer_id,
        "date":             session.date,
        "duration_minutes": session.duration_minutes,
        "type":             session.type,
        "status":           "booked",
    }
    sessions.append(new_session)
    session_id_counter += 1
    return {
        "message":   "✅ Session booked successfully",
        "session":   new_session,
        "member":    member["name"],
        "trainer":   trainer["name"],
        "next_step": f"POST /sessions/{new_session['id']}/checkin",
    }


# Q14 — STEP 2: Check-In
@app.post("/sessions/{session_id}/checkin", tags=["Day 5 - Multi-Step Workflow"])
def checkin_session(session_id: int):
    """
    STEP 2 of 3 — Check in for a booked session.
    Status must be booked → changes to in_progress.
    Next: POST /sessions/{id}/complete
    """
    session = find_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session ID {session_id} not found")
    if session["status"] != "booked":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot check in. Status is '{session['status']}'. Must be 'booked'.",
        )
    session["status"]       = "in_progress"
    session["checkin_time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return {
        "message":   "✅ Check-in successful! Session is now in progress 💪",
        "session":   session,
        "next_step": f"POST /sessions/{session_id}/complete",
    }


# Q15 — STEP 3: Complete Session
@app.post("/sessions/{session_id}/complete", tags=["Day 5 - Multi-Step Workflow"])
def complete_session(session_id: int):
    """
    STEP 3 of 3 — Mark session as completed.
    Status must be in_progress → changes to completed.
    """
    session = find_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session ID {session_id} not found")
    if session["status"] != "in_progress":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot complete. Status is '{session['status']}'. Must be 'in_progress'.",
        )
    session["status"]        = "completed"
    session["checkout_time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return {
        "message":          "🎉 Session completed! Great workout!",
        "session":          session,
        "duration_minutes": session["duration_minutes"],
    }


# Q19 — Get All Sessions (enriched)
@app.get("/sessions", tags=["Day 6 - Search, Sort, Paginate"])
def get_all_sessions(
    status: Optional[str] = Query(None, description="booked | in_progress | completed | cancelled"),
):
    """Return all sessions enriched with member and trainer names. Filter by status."""
    result = sessions if status is None else [s for s in sessions if s["status"] == status.lower()]
    enriched = []
    for s in result:
        m = find_member(s["member_id"])
        t = find_trainer(s["trainer_id"])
        enriched.append({
            **s,
            "member_name":  m["name"] if m else "Unknown",
            "trainer_name": t["name"] if t else "Unknown",
        })
    return {"total": len(enriched), "sessions": enriched} 