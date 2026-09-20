"""
Orbit Grid — Database & Persistence Engine
Manages enterprise users, authentication sessions, and persistent supply chain / warehouse analysis.
Uses SQLite for zero-config, ACID-compliant, reliable local persistence,
with extensible hooks for Supabase cloud sync when configured.
"""

import os
import sqlite3
import hashlib
import secrets
import json
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, Tuple

DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "orbit_grid.db")

from contextlib import contextmanager

# Optional Supabase credentials from environment
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """
    Initializes database tables for users, sessions, and warehouse analysis state.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Users Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 2. Authentication Sessions Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # 3. Persistent User Warehouse Analysis Scenarios Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_scenarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                scenario_name TEXT NOT NULL,
                region TEXT DEFAULT 'pan_india',
                business_description TEXT,
                warehouse_count INTEGER DEFAULT 2,
                snap_to_hubs INTEGER DEFAULT 1,
                demand_points_json TEXT,
                optimized_result_json TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        conn.commit()


# Initialize schema on module import
init_db()


def _hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    if not salt:
        salt = secrets.token_hex(16)
    # Salted SHA-256
    hash_obj = hashlib.sha256((salt + password).encode("utf-8"))
    return hash_obj.hexdigest(), salt


def register_user(company_name: str, username: str, password: str) -> Dict[str, Any]:
    """
    Registers a new company account.
    """
    company_name = company_name.strip()
    username = username.strip().lower()
    
    if not company_name:
        raise ValueError("Company name is required.")
    if not username or len(username) < 3:
        raise ValueError("Username must be at least 3 characters.")
    if not password or len(password) < 4:
        raise ValueError("Password must be at least 4 characters.")
        
    pwd_hash, salt = _hash_password(password)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (company_name, username, password_hash, salt, created_at, last_login)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """, (company_name, username, pwd_hash, salt))
            user_id = cursor.lastrowid
            conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError(f"Username '{username}' is already registered. Please sign in.")
            
    token = create_session(user_id)
    return {
        "user_id": user_id,
        "company_name": company_name,
        "username": username,
        "token": token
    }


def authenticate_user(username: str, password: str) -> Dict[str, Any]:
    """
    Authenticates username and password against the database.
    """
    username = username.strip().lower()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        
        if not row:
            raise ValueError("Invalid username or password.")
            
        pwd_hash, _ = _hash_password(password, row["salt"])
        if pwd_hash != row["password_hash"]:
            raise ValueError("Invalid username or password.")
            
        # Update last login
        cursor.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?", (row["id"],))
        conn.commit()
        
        user_id = row["id"]
        company_name = row["company_name"]

    token = create_session(user_id)
    saved_scenario = get_user_analysis(user_id)
    
    return {
        "user_id": user_id,
        "company_name": company_name,
        "username": username,
        "token": token,
        "saved_scenario": saved_scenario
    }


def create_session(user_id: int) -> str:
    """
    Creates a new 30-day authentication session token.
    """
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(days=30)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sessions (token, user_id, expires_at)
            VALUES (?, ?, ?)
        """, (token, user_id, expires_at.isoformat()))
        conn.commit()
        
    return token


def verify_session(token: str) -> Optional[Dict[str, Any]]:
    """
    Verifies a session token and returns the authenticated user details.
    """
    if not token:
        return None
        
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id, u.company_name, u.username, s.expires_at
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.token = ?
        """, (token,))
        row = cursor.fetchone()
        
        if not row:
            return None
            
        expires_at = datetime.fromisoformat(row["expires_at"])
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) > expires_at:
            cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
            conn.commit()
            return None
            
        return {
            "user_id": row["id"],
            "company_name": row["company_name"],
            "username": row["username"]
        }


def destroy_session(token: str):
    """
    Invalidates a session token (log out).
    """
    if not token:
        return
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
        conn.commit()


def save_user_analysis(
    user_id: int,
    region: str,
    business_description: str,
    warehouse_count: int,
    snap_to_hubs: bool,
    demand_points: list,
    optimized_result: Optional[dict] = None,
    scenario_name: str = "Primary Active Network"
) -> Dict[str, Any]:
    """
    Saves or updates the user's active warehouse optimization network and demand data.
    """
    demand_json = json.dumps(demand_points or [])
    result_json = json.dumps(optimized_result or {})
    snap_int = 1 if snap_to_hubs else 0
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM user_scenarios WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute("""
                UPDATE user_scenarios
                SET scenario_name = ?, region = ?, business_description = ?,
                    warehouse_count = ?, snap_to_hubs = ?, demand_points_json = ?,
                    optimized_result_json = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (scenario_name, region, business_description, warehouse_count, snap_int, demand_json, result_json, existing["id"]))
            scenario_id = existing["id"]
        else:
            cursor.execute("""
                INSERT INTO user_scenarios (user_id, scenario_name, region, business_description, warehouse_count, snap_to_hubs, demand_points_json, optimized_result_json, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (user_id, scenario_name, region, business_description, warehouse_count, snap_int, demand_json, result_json))
            scenario_id = cursor.lastrowid
            
        conn.commit()
        
    return {
        "status": "success",
        "scenario_id": scenario_id,
        "demand_points_count": len(demand_points or []),
        "warehouse_count": warehouse_count,
        "region": region
    }


def get_user_analysis(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieves the user's latest saved warehouse network analysis.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM user_scenarios
            WHERE user_id = ?
            ORDER BY updated_at DESC LIMIT 1
        """, (user_id,))
        row = cursor.fetchone()
        
        if not row:
            return None
            
        demand_points = []
        if row["demand_points_json"]:
            try:
                demand_points = json.loads(row["demand_points_json"])
            except Exception:
                pass
                
        optimized_result = None
        if row["optimized_result_json"]:
            try:
                optimized_result = json.loads(row["optimized_result_json"])
            except Exception:
                pass
                
        return {
            "id": row["id"],
            "scenario_name": row["scenario_name"],
            "region": row["region"],
            "business_description": row["business_description"],
            "warehouse_count": row["warehouse_count"],
            "snap_to_hubs": bool(row["snap_to_hubs"]),
            "demand_points": demand_points,
            "optimized_result": optimized_result,
            "updated_at": row["updated_at"]
        }


def get_or_create_evaluator_account() -> Dict[str, Any]:
    """
    Creates or returns a pre-configured account for 1-click evaluator / hackathon judge demo.
    """
    username = "evaluator"
    password = "judge_access_2026"
    company_name = "National Logistics & Supply Chain Corp"
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        
    if not row:
        return register_user(company_name, username, password)
    else:
        return authenticate_user(username, password)
