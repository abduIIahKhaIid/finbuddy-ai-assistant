from uagents import Agent, Context
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend_api.models_shared import ShareRequest, ShareResponse



share_agent = Agent(
    name="ShareAgent",
    seed="share-agent-seed",
    port=8010,
    endpoint="http://localhost:8010/submit"
)

@share_agent.on_message(model=ShareRequest)
async def handle_share(ctx: Context, sender: str, msg: ShareRequest):
    tweet = (
        f"Thanks to #FinBuddy, {msg.user_name} saved {msg.saved_amount} PKR in {msg.weeks} weeks 💚\n"
        f"Planning made simple with AI + agents. #RAISEYourHack"
    )
    message = "📤 Tweet ready to post!"
    await ctx.send(sender, ShareResponse(message=message, tweet_text=tweet))

if __name__ == "__main__":
    share_agent.run()