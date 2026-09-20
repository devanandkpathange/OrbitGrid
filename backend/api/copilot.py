"""
Orbit Grid SETU — Supply-chain Evaluation & Tactical Unit API Router.
Accepts user questions about supply chain siting, co-serving corridors,
cost trade-offs, and disruptions, and answers using SETU's autonomous reasoning engine
or your team's fine-tuned model endpoint.
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from ..services.ai_copilot import answer_supply_chain_question

router = APIRouter(prefix="/api/copilot", tags=["Orbit Grid SETU Intelligence Core"])


class CopilotQueryRequest(BaseModel):
    question: str = Field(..., description="User's logistics, routing, or siting question")
    custom_llm_url: Optional[str] = Field(None, description="Optional custom/local trained LLM endpoint URL")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Active network telemetry & solution state")


class CopilotQueryResponse(BaseModel):
    answer: str
    source: str
    key_takeaways: List[str] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)


@router.post("/chat", response_model=CopilotQueryResponse)
async def ask_copilot(request: CopilotQueryRequest):
    """
    Queries Orbit Grid SETU Supply Chain Advisor with active network context.
    Runs 100% offline at ₹0 cost or connects to custom trained model endpoint.
    """
    result = await answer_supply_chain_question(
        question=request.question,
        custom_llm_url=request.custom_llm_url,
        context=request.context
    )
    return result
