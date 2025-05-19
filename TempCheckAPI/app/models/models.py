from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"
    PARENT = "parent"

class User(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole
    name: str
    password: str  # In a real app, this would be hashed

class EmotionType(str, Enum):
    VERY_HAPPY = "very_happy"
    HAPPY = "happy"
    NEUTRAL = "neutral"
    SAD = "sad"
    VERY_SAD = "very_sad"
    NEED_HELP = "need_help"

class EmotionalCheckIn(BaseModel):
    id: int
    user_id: int
    emotion: EmotionType
    timestamp: datetime
    notes: Optional[str] = None

class FocusModeSession(BaseModel):
    id: int
    user_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    is_active: bool = True

class Streak(BaseModel):
    id: int
    user_id: int
    current_streak: int
    longest_streak: int
    last_check_in: datetime
