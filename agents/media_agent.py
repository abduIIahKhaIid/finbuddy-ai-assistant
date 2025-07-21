
from uagents import Agent, Context
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend_api.models_shared import MediaRequest, MediaResponse



media_agent = Agent(
    name="MediaAgent",
    seed="media-agent-seed",
    port=8009,
    endpoint="http://localhost:8009/submit"
)

@media_agent.on_message(model=MediaRequest)
async def handle_media(ctx: Context, sender: str, msg: MediaRequest):
    message = (
        f"🎬 {msg.user_name} ka motivational video ready hai for goal '{msg.goal}'!\n"
        f"Dekhein apni mehnat ka safar 💪"
    )
    # Placeholder video URL
    media_url = "https://example.com/fake-progress-video.mp4"

    await ctx.send(sender, MediaResponse(message=message, media_url=media_url))

if __name__ == "__main__":
    media_agent.run()