from uagents import Agent, Context
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend_api.models_shared import CreditQueryRequest, CreditQueryResponse

credit_agent = Agent(
    name="CreditAgent",
    seed="credit-agent-seed",
    port=8007,
    endpoint="http://localhost:8007/submit"
)

@credit_agent.on_message(model=CreditQueryRequest)
async def handle_credit_query(ctx: Context, sender: str, msg: CreditQueryRequest):
    ctx.logger.info(f"📊 Credit query received: {msg.query_type}")

    if msg.query_type == "loan_eligibility":
        if msg.credit_score and msg.credit_score >= 700:
            message = "👍 Aapka credit score strong hai — loan lena asaan ho sakta hai!"
        elif msg.credit_score:
            message = "📉 Score thoda low hai. Loan milega lekin shayad zyada markup par."
        else:
            message = "💡 Pehle apna credit score check karen — apps like CreditFix ya Karandaaz help karte hain."

    elif msg.query_type == "how_to_check":
        message = "📲 Credit score check karne ke liye: Try apps like CreditFix, Easypaisa, ya apna bank portal."

    else:
        message = "❓ Specific query type unclear. Bataiye aap kis cheez ke liye pooch rahe hain?"

    response = CreditQueryResponse(message=message)
    await ctx.send(sender, response)

if __name__ == "__main__":
    credit_agent.run()
