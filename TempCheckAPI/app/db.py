from datetime import datetime
from typing import Dict, List, Optional
from .models.models import User, EmotionalCheckIn, FocusModeSession, Streak, UserRole, EmotionType

users: Dict[int, User] = {}
emotional_check_ins: Dict[int, EmotionalCheckIn] = {}
focus_mode_sessions: Dict[int, FocusModeSession] = {}
streaks: Dict[int, Streak] = {}

user_id_counter = 1
check_in_id_counter = 1
session_id_counter = 1
streak_id_counter = 1

def seed_data():
    global user_id_counter, check_in_id_counter, session_id_counter, streak_id_counter
    
    create_user("student1", "student1@example.com", UserRole.STUDENT, "Student One", "password")
    create_user("teacher1", "teacher1@example.com", UserRole.TEACHER, "Teacher One", "password")
    
def create_user(username: str, email: str, role: UserRole, name: str, password: str) -> User:
    global user_id_counter
    user = User(
        id=user_id_counter,
        username=username,
        email=email,
        role=role,
        name=name,
        password=password  # In a real app, this would be hashed
    )
    users[user_id_counter] = user
    user_id_counter += 1
    return user

def get_user(user_id: int) -> Optional[User]:
    return users.get(user_id)

def get_users() -> List[User]:
    return list(users.values())

def get_user_by_username(username: str) -> Optional[User]:
    for user in users.values():
        if user.username == username:
            return user
    return None

def create_check_in(user_id: int, emotion: EmotionType, notes: Optional[str] = None) -> EmotionalCheckIn:
    global check_in_id_counter
    check_in = EmotionalCheckIn(
        id=check_in_id_counter,
        user_id=user_id,
        emotion=emotion,
        timestamp=datetime.now(),
        notes=notes
    )
    emotional_check_ins[check_in_id_counter] = check_in
    check_in_id_counter += 1
    
    update_streak(user_id)
    
    return check_in

def get_check_ins_by_user(user_id: int) -> List[EmotionalCheckIn]:
    return [ci for ci in emotional_check_ins.values() if ci.user_id == user_id]

def get_check_ins() -> List[EmotionalCheckIn]:
    return list(emotional_check_ins.values())

def start_focus_mode(user_id: int) -> FocusModeSession:
    global session_id_counter
    session = FocusModeSession(
        id=session_id_counter,
        user_id=user_id,
        start_time=datetime.now(),
        is_active=True
    )
    focus_mode_sessions[session_id_counter] = session
    session_id_counter += 1
    return session

def end_focus_mode(session_id: int) -> Optional[FocusModeSession]:
    session = focus_mode_sessions.get(session_id)
    if session and session.is_active:
        session.end_time = datetime.now()
        session.is_active = False
        focus_mode_sessions[session_id] = session
    return session

def get_active_focus_mode(user_id: int) -> Optional[FocusModeSession]:
    for session in focus_mode_sessions.values():
        if session.user_id == user_id and session.is_active:
            return session
    return None

def create_streak(user_id: int) -> Streak:
    global streak_id_counter
    streak = Streak(
        id=streak_id_counter,
        user_id=user_id,
        current_streak=0,
        longest_streak=0,
        last_check_in=datetime.now()
    )
    streaks[streak_id_counter] = streak
    streak_id_counter += 1
    return streak

def update_streak(user_id: int) -> Streak:
    user_streak = None
    for streak in streaks.values():
        if streak.user_id == user_id:
            user_streak = streak
            break
    
    if not user_streak:
        user_streak = create_streak(user_id)
    
    today = datetime.now().date()
    last_check_in_date = user_streak.last_check_in.date()
    
    if (today - last_check_in_date).days == 1:
        user_streak.current_streak += 1
        if user_streak.current_streak > user_streak.longest_streak:
            user_streak.longest_streak = user_streak.current_streak
    elif (today - last_check_in_date).days > 1:
        user_streak.current_streak = 1
    
    user_streak.last_check_in = datetime.now()
    return user_streak

def get_streak(user_id: int) -> Optional[Streak]:
    for streak in streaks.values():
        if streak.user_id == user_id:
            return streak
    return None

seed_data()
