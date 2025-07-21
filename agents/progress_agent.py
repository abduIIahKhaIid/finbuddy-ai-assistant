from uagents import Agent, Context
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend_api.models_shared import ProgressRequest, ProgressResponse

progress_agent = Agent(
    name="ProgressAgent",
    seed="progress-agent-seed",
    port=8008,
    endpoint="http://localhost:8008/submit"
)

@progress_agent.on_message(model=ProgressRequest)
async def handle_progress(ctx: Context, sender: str, msg: ProgressRequest):
    total = sum(p.amount_saved for p in msg.progress)
    percent = (total / msg.goal_amount) * 100
    progress_lines = "\n".join([f"Week {p.week}: {p.amount_saved} PKR" for p in msg.progress])

    message = (
        f"📊 **{msg.user_name}'s Saving Progress**\n"
        f"{progress_lines}\n\n"
        f"🎯 Goal: {msg.goal}\n"
        f"💰 Total Saved: {total} PKR ({percent:.1f}%)"
    )

    await ctx.send(sender, ProgressResponse(message=message))

if __name__ == "__main__":
    progress_agent.run()