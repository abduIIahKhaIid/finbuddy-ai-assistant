from uagents import Agent, Context
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend_api.models_shared import PausePlanRequest, PausePlanResponse

pause_agent = Agent(
    name="PauseAgent",
    seed="pause-agent-seed",
    port=8005,
    endpoint="http://localhost:8005/submit"
)

@pause_agent.on_message(model=PausePlanRequest)
async def handle_pause(ctx: Context, sender: str, msg: PausePlanRequest):
    ctx.logger.info(f"⏸️ Pause request from {sender}")

    friendly_msg = f"😌 No worries {msg.user_name or 'friend'} — it's totally okay to take a break. Jab tayar ho, main yahin hoon ❤️"
    
    await ctx.send(sender, PausePlanResponse(message=friendly_msg))

if __name__ == "__main__":
    pause_agent.run()
