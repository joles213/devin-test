from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime
import psycopg
from . import db
from .models.models import User, EmotionalCheckIn, FocusModeSession, Streak, UserRole, EmotionType

app = FastAPI()

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/api/login")
async def login(username: str, password: str):
    user = db.get_user_by_username(username)
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"user_id": user.id, "username": user.username, "role": user.role, "name": user.name}

@app.get("/api/users")
async def get_users():
    return db.get_users()

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/api/check-ins")
async def create_check_in(user_id: int, emotion: EmotionType, notes: Optional[str] = None):
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    check_in = db.create_check_in(user_id, emotion, notes)
    
    if emotion in [EmotionType.VERY_SAD, EmotionType.NEED_HELP]:
        return {"check_in": check_in, "alert": True, "message": f"Alert: Student {user.name} needs attention"}
    
    return {"check_in": check_in, "alert": False}

@app.get("/api/check-ins/user/{user_id}")
async def get_user_check_ins(user_id: int):
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return db.get_check_ins_by_user(user_id)

@app.post("/api/focus-mode/start")
async def start_focus_mode(user_id: int):
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    active_session = db.get_active_focus_mode(user_id)
    if active_session:
        return active_session
    
    return db.start_focus_mode(user_id)

@app.post("/api/focus-mode/end/{session_id}")
async def end_focus_mode(session_id: int):
    session = db.end_focus_mode(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or already ended")
    return session

@app.get("/api/focus-mode/active/{user_id}")
async def get_active_focus_mode(user_id: int):
    session = db.get_active_focus_mode(user_id)
    if not session:
        return {"is_active": False}
    return {"is_active": True, "session": session}

@app.get("/api/streaks/{user_id}")
async def get_user_streak(user_id: int):
    streak = db.get_streak(user_id)
    if not streak:
        return {"streak": 0, "longest_streak": 0}
    return streak
