from uagents import Agent, Context
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend_api.models_shared import DeclineRequest, DeclineResponse

decline_agent = Agent(
    name="DeclineAgent",
    seed="decline-agent-seed",
    port=8006,
    endpoint="http://localhost:8006/submit"
)

@decline_agent.on_message(model=DeclineRequest)
async def handle_decline(ctx: Context, sender: str, msg: DeclineRequest):
    ctx.logger.info(f"❌ User declined for now: {msg.reason}")

    response = DeclineResponse(
        message=f"Koi masla nahi {msg.user_name or 'dost'} 😊 Jab mood ho, main yahin hoon!"
    )

    await ctx.send(sender, response)

if __name__ == "__main__":
    decline_agent.run()
