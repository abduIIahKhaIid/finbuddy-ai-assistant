# backend_api/models

from uagents import Model
from pydantic import BaseModel
from typing import List, Optional

class ExpenseItem(BaseModel):
    category: str
    amount: int

class SavingPlanRequest(BaseModel):
    income: int
    goal: str
    goal_cost: Optional[int] = None
    expenses: List[ExpenseItem]


class SavingPlanResponse(BaseModel):
    message: str
    monthly_saving: int
    suggestions: Optional[List[str]] = []

class UserQuery(Model):
    user_input: str
    history: List[dict]



class ReminderRequest(BaseModel):
    day: str  # "Friday"
    time: str  # "10:00"
    user_name: str

class ReminderResponse(BaseModel):
    message: str


class BudgetReviewRequest(BaseModel):
    income: int
    expenses: List[ExpenseItem]

class BudgetReviewResponse(BaseModel):
    message: str
    risk_level: Optional[str] = None  # e.g., "high", "moderate", "low"
    suggestions: Optional[List[str]] = []


class PausePlanRequest(BaseModel):
    reason: Optional[str] = None
    user_name: Optional[str] = None

class PausePlanResponse(BaseModel):
    message: str


class DeclineRequest(BaseModel):
    reason: Optional[str] = None
    user_name: Optional[str] = None

class DeclineResponse(BaseModel):
    message: str


class CreditQueryRequest(BaseModel):
    credit_score: Optional[int] = None
    query_type: Optional[str] = None  # e.g., "loan_eligibility", "how_to_check"

class CreditQueryResponse(BaseModel):
    message: str



class ProgressItem(BaseModel):
    week: int
    amount_saved: int

class ProgressRequest(BaseModel):
    user_name: str
    goal: str
    goal_amount: int
    progress: List[ProgressItem]

class ProgressResponse(BaseModel):
    message: str


class MediaRequest(BaseModel):
    user_name: str
    goal: str

class MediaResponse(BaseModel):
    message: str
    media_url: str


class ShareRequest(BaseModel):
    user_name: str
    saved_amount: int
    weeks: int

class ShareResponse(BaseModel):
    message: str
    tweet_text: str