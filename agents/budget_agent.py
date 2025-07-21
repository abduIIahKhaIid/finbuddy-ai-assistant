from uagents import Agent, Context
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend_api.models_shared import BudgetReviewRequest, BudgetReviewResponse

budget_agent = Agent(
    name="BudgetAgent",
    seed="budget-agent-seed",
    port=8004,
    endpoint="http://localhost:8004/submit"
)

@budget_agent.on_message(model=BudgetReviewRequest)
async def handle_budget_review(ctx: Context, sender: str, msg: BudgetReviewRequest):
    ctx.logger.info(f"📊 Budget Review Request received from {sender}")

    total_expenses = sum(e.amount for e in msg.expenses)
    savings = msg.income - total_expenses

    suggestions = []
    if savings <= 0:
        suggestions.append("Aapka kharcha income se zyada hai — consider reducing non-essential spending.")
    else:
        suggestions.append(f"Aap around {savings} PKR save kar sakte hain har month agar ye pattern follow ho.")

    top_spends = sorted(msg.expenses, key=lambda e: e.amount, reverse=True)[:2]
    for item in top_spends:
        suggestions.append(f"💸 {item.category} main zyada kharch hai — isay review karein.")

    response = BudgetReviewResponse(
        message=f"📊 Budget analysis complete. You have {savings} PKR left after expenses.",
        insights=suggestions
    )

    await ctx.send(sender, response)

if __name__ == "__main__":
    budget_agent.run()
