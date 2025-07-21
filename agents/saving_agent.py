# agents/saving_agent.py

from uagents import Agent, Context

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend_api.models_shared import SavingPlanRequest, SavingPlanResponse


# ----------------------
# 🤖 Define Agent
# ----------------------
saving_agent = Agent(
    name="SavingAgent",
    seed="saving-agent-seed",
    port=8002,
    endpoint="http://localhost:8002/submit"
)


# ----------------------
# 📬 Handle Incoming Request
# ----------------------
@saving_agent.on_message(model=SavingPlanRequest)
async def handle_saving_plan(ctx: Context, sender: str, msg: SavingPlanRequest):
    ctx.logger.info(f"📥 Received saving plan request from {sender}")
    
    total_expenses = sum(e.amount for e in msg.expenses)
    available = msg.income - total_expenses

    if available <= 0:
        response = SavingPlanResponse(
            message="😟 Aapka kharch income se zyada hai. Saving possible nahi hai.",
            monthly_saving=0,
            suggestions=["Track spending with an app", "Avoid impulse purchases"]
        )
        await ctx.send(sender, response)
        return

    if msg.goal_cost:
        months = max(1, msg.goal_cost // available)
        monthly_saving = min(available, msg.goal_cost // months)
        message = f"🎯 Goal '{msg.goal}' ke liye {monthly_saving} PKR/month save karein — approx {months} months mein goal poora ho sakta hai."
    else:
        monthly_saving = int(available * 0.25)
        message = f"💡 Aap {monthly_saving} PKR/month save kar sakte hain based on your budget."

    response = SavingPlanResponse(
        message=message,
        monthly_saving=monthly_saving,
        suggestions=["Use cash envelope method", "Review budget weekly"]
    )

    await ctx.send(sender, response)

# ----------------------
# 🏁 Run the Agent
# ----------------------
if __name__ == "__main__":
    saving_agent.run()
