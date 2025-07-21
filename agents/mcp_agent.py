import json
from typing import List, Optional, Dict
from uagents import Agent, Context, Model
from pydantic import BaseModel, ValidationError

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend_api.llm_response import query_llama
from backend_api.agent_registry import AGENT_REGISTRY
from backend_api.models_shared import (
    BudgetReviewRequest, CreditQueryRequest, DeclineRequest, MediaRequest,
    PausePlanRequest, ProgressItem, ProgressRequest, SavingPlanRequest,
    ExpenseItem, ShareRequest, UserQuery, ReminderRequest
)

# ✅ Required fields per intent
REQUIRED_FIELDS = {
    "saving_plan": ["goal", "income"],
    "budget_review": ["income", "expenses"],
    "reminder_setup": ["day", "time", "user_name"],
    "pause_plan": ["reason", "user_name"],
    "decline": ["user_name"],
    "credit_query": ["credit_score", "query_type"],
    "progress_tracking": ["user_name", "goal", "goal_amount", "progress"],
    "media_request": ["user_name", "goal"],
    "share_request": ["user_name", "saved_amount", "weeks"]
}

# ✅ Intent → Agent name
intent_to_agent_name = {
    "saving_plan": "SavingAgent",
    "budget_review": "BudgetAgent",
    "reminder_setup": "ReminderAgent",
    "pause_plan": "PauseAgent",
    "decline": "DeclineAgent",
    "credit_query": "CreditAgent",
    "progress_tracking": "ProgressAgent",
    "media_request": "MediaAgent",
    "share_request": "ShareAgent"
}

# 📦 Parsed LLM response model
class LLMParsedOutput(BaseModel):
    intents: List[str]
    saving_plan: Optional[Dict] = None
    budget_review: Optional[Dict] = None
    credit_query: Optional[Dict] = None
    reminder_setup: Optional[Dict] = None
    pause_plan: Optional[Dict] = None
    decline: Optional[Dict] = None
    non_financial: Optional[Dict] = None
    progress_tracking: Optional[Dict] = None
    media_request: Optional[Dict] = None
    share_request: Optional[Dict] = None

    missing_fields: List[str]
    confidence: float
    message: str

# 💬 Simple outgoing message
class SimpleMessage(Model):
    message: str

# 🤖 MCP Agent definition
mcp_agent = Agent(
    name="MCPAgent",
    seed="mcp_agent",
    port=8001,
    endpoint=["http://localhost:8001/submit"]
)

# 🧠 Core handler
@mcp_agent.on_message(model=UserQuery)
async def handle_user_input(ctx: Context, sender: str, msg: UserQuery):
    ctx.logger.info("🧠 MCPAgent received a user message")

    try:
        # 🔹 Step 1: Build prompt
        prompt = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in msg.history])
        llama_response = query_llama(prompt)
        print(llama_response)
        # 🔹 Step 2: Parse LLM
        parsed = LLMParsedOutput(**json.loads(llama_response))
        ctx.logger.info(f"📌 LLM Intents Detected: {parsed.intents}")

        # 🔹 Step 3: Handle non-financial
        if "non_financial" in parsed.intents:
            await ctx.send(sender, SimpleMessage(message=parsed.message))
            return

        dispatched_intents = []

        # 🔹 Step 4: Intent Dispatch Loop
        for intent in parsed.intents:
            intent_data = getattr(parsed, intent, {})

            # ✅ Check for required fields
            missing = [f for f in REQUIRED_FIELDS.get(intent, []) if intent_data.get(f) in [None, "", [], {}]]
            if missing:
                ctx.logger.warning(f"⚠️ Required fields missing for `{intent}`: {', '.join(missing)}")
                ctx.logger.info(f"🔄 Skipping dispatch for `{intent}` due to incomplete info.")
                await ctx.send(sender, SimpleMessage(message=parsed.message))
                continue

            # 🧭 Route to agent
            agent_name = intent_to_agent_name.get(intent)
            agent_address = AGENT_REGISTRY.get(agent_name)
            if not agent_address:
                ctx.logger.warning(f"🚫 No registered agent for `{intent}`")
                continue

            # 📦 Dispatch request based on intent
            if intent == "saving_plan":
                request = SavingPlanRequest(
                    income=intent_data["income"],
                    goal=intent_data["goal"],
                    goal_cost=intent_data.get("goal_cost", 0),
                    expenses=[ExpenseItem(**e) for e in intent_data.get("expenses", [])]
                )
            elif intent == "budget_review":
                request = BudgetReviewRequest(
                    income=intent_data["income"],
                    expenses=[ExpenseItem(**e) for e in intent_data.get("expenses", [])]
                )
            elif intent == "reminder_setup":
                request = ReminderRequest(
                    day=intent_data["day"],
                    time=intent_data["time"],
                    user_name=intent_data["user_name"]
                )
            elif intent == "pause_plan":
                request = PausePlanRequest(
                    reason=intent_data["reason"],
                    user_name=intent_data["user_name"]
                )
            elif intent == "decline":
                request = DeclineRequest(
                    reason=intent_data.get("reason", "User declined"),
                    user_name=intent_data["user_name"]
                )
            elif intent == "credit_query":
                request = CreditQueryRequest(
                    credit_score=intent_data["credit_score"],
                    query_type=intent_data["query_type"]
                )
            elif intent == "progress_tracking":
                request = ProgressRequest(
                    user_name=intent_data["user_name"],
                    goal=intent_data["goal"],
                    goal_amount=intent_data["goal_amount"],
                    progress=[ProgressItem(**p) for p in intent_data["progress"]]
                )
            elif intent == "media_request":
                request = MediaRequest(
                    user_name=intent_data["user_name"],
                    goal=intent_data["goal"]
                )
            elif intent == "share_request":
                request = ShareRequest(
                    user_name=intent_data["user_name"],
                    saved_amount=intent_data["saved_amount"],
                    weeks=intent_data["weeks"]
                )
            else:
                ctx.logger.warning(f"⛔ Unsupported intent: {intent}")
                continue

            # 🚀 Send to agent
            await ctx.send(agent_address, request)
            dispatched_intents.append(intent)

        # 🔚 Step 5: Final user message
        if not dispatched_intents:
            await ctx.send(sender, SimpleMessage(message=parsed.message))
        else:
            await ctx.send(sender, SimpleMessage(message=parsed.message))

    except ValidationError as ve:
        ctx.logger.error(f"🔍 Validation Error: {ve}")
        await ctx.send(sender, SimpleMessage(message="❌ Sorry, response format was invalid. Try again."))
    except Exception as e:
        ctx.logger.error(f"🔥 MCP Error: {e}")
        await ctx.send(sender, SimpleMessage(message="🚨 Internal error occurred."))

# 🏃 Standalone mode
if __name__ == "__main__":
    mcp_agent.run()
