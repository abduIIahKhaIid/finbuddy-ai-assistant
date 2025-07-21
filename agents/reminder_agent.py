from uagents import Agent, Context

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend_api.models_shared import ReminderRequest, ReminderResponse

# Define the agent
reminder_agent = Agent(
    name="ReminderAgent",
    seed="reminder-agent-seed",
    port=8003,
    endpoint="http://localhost:8003/submit"
)

@reminder_agent.on_message(model=ReminderRequest)
async def handle_reminder_request(ctx: Context, sender: str, msg: ReminderRequest):
    ctx.logger.info(f"📥 Reminder request received for {msg.user_name}")

    response = ReminderResponse(
        message=f"✅ Reminder set! ⏰ Every {msg.day} at {msg.time} for {msg.user_name}."
    )

    await ctx.send(sender, response)

if __name__ == "__main__":
    reminder_agent.run()
