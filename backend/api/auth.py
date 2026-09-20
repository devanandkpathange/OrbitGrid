"""
Authentication and User State Persistence Router for Orbit Grid.
Provides registration, login, evaluator demo access, session validation,
and saving/loading persistent warehouse analysis states.
"""

from fastapi import APIRouter, HTTPException, Header, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from ..db.database import (
    register_user,
    authenticate_user,
    verify_session,
    destroy_session,
    save_user_analysis,
    get_user_analysis,
    get_or_create_evaluator_account
)

router = APIRouter(prefix="/api", tags=["Authentication & User Management"])


class RegisterRequest(BaseModel):
    company_name: str
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class SaveAnalysisRequest(BaseModel):
    region: Optional[str] = "pan_india"
    business_description: Optional[str] = "General Supply Chain"
    warehouse_count: Optional[int] = 2
    snap_to_hubs: Optional[bool] = True
    demand_points: Optional[List[Dict[str, Any]]] = []
    optimized_result: Optional[Dict[str, Any]] = None
    scenario_name: Optional[str] = "Primary Active Network"


def _extract_token(authorization: Optional[str], token: Optional[str]) -> str:
    if authorization and authorization.startswith("Bearer "):
        return authorization.split("Bearer ")[1].strip()
    if token:
        return token.strip()
    return ""


@router.post("/auth/register")
async def api_register(payload: RegisterRequest):
    try:
        res = register_user(payload.company_name, payload.username, payload.password)
        return {
            "status": "success",
            "message": "Company registered successfully.",
            "token": res["token"],
            "user": {
                "company_name": res["company_name"],
                "username": res["username"]
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/auth/login")
async def api_login(payload: LoginRequest):
    try:
        res = authenticate_user(payload.username, payload.password)
        return {
            "status": "success",
            "message": "Welcome back!",
            "token": res["token"],
            "user": {
                "company_name": res["company_name"],
                "username": res["username"]
            },
            "saved_scenario": res["saved_scenario"]
        }
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")


@router.post("/auth/evaluator-demo")
async def api_evaluator_demo():
    """
    1-Click Evaluator access for judges. Pre-configures a clean corporate environment.
    """
    try:
        res = get_or_create_evaluator_account()
        return {
            "status": "success",
            "message": "Evaluator Demo Access Granted.",
            "token": res["token"],
            "user": {
                "company_name": res["company_name"],
                "username": res["username"]
            },
            "saved_scenario": res.get("saved_scenario")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demo access failed: {str(e)}")


@router.get("/auth/me")
async def api_get_me(
    authorization: Optional[str] = Header(None),
    token: Optional[str] = Query(None)
):
    tok = _extract_token(authorization, token)
    user = verify_session(tok)
    if not user:
        raise HTTPException(status_code=401, detail="Session expired or invalid.")
        
    saved_scenario = get_user_analysis(user["user_id"])
    return {
        "status": "success",
        "user": {
            "company_name": user["company_name"],
            "username": user["username"]
        },
        "saved_scenario": saved_scenario
    }


@router.post("/auth/logout")
async def api_logout(
    authorization: Optional[str] = Header(None),
    token: Optional[str] = Query(None)
):
    tok = _extract_token(authorization, token)
    if tok:
        destroy_session(tok)
    return {"status": "success", "message": "Logged out successfully."}


@router.post("/user/save-analysis")
async def api_save_analysis(
    payload: SaveAnalysisRequest,
    authorization: Optional[str] = Header(None),
    token: Optional[str] = Query(None)
):
    tok = _extract_token(authorization, token)
    user = verify_session(tok)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required to save analysis.")
        
    res = save_user_analysis(
        user_id=user["user_id"],
        region=payload.region or "pan_india",
        business_description=payload.business_description or "General Supply Chain",
        warehouse_count=payload.warehouse_count or 2,
        snap_to_hubs=payload.snap_to_hubs if payload.snap_to_hubs is not None else True,
        demand_points=payload.demand_points or [],
        optimized_result=payload.optimized_result,
        scenario_name=payload.scenario_name or "Primary Active Network"
    )
    return {
        "status": "success",
        "message": f"Successfully saved {res['demand_points_count']} demand nodes & warehouse analysis to database.",
        "details": res
    }


@router.get("/user/my-analysis")
async def api_get_my_analysis(
    authorization: Optional[str] = Header(None),
    token: Optional[str] = Query(None)
):
    tok = _extract_token(authorization, token)
    user = verify_session(tok)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required.")
        
    saved = get_user_analysis(user["user_id"])
    return {
        "status": "success",
        "has_saved_analysis": bool(saved),
        "analysis": saved
    }
