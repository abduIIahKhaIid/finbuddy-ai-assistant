from uagents import Agent, Context
from pydantic import BaseModel
from uagents.setup import fund_agent_if_low

class MissingDataRequest(BaseModel):
    missing_fields: list
    user_name: str

class MissingDataResponse(BaseModel):
    message: str

filler_agent = Agent(name="DataFillerAgent", seed="filler-agent-seed")
fund_agent_if_low(filler_agent.wallet.address())

@filler_agent.on_message(model=MissingDataRequest)
async def handle_filler(ctx: Context, sender: str, msg: MissingDataRequest):
    fields = ", ".join(msg.missing_fields)
    response = f"👋 {msg.user_name}, to continue, I need: {fields}. Could you please share that?"

    await ctx.send(sender, MissingDataResponse(message=response))

if __name__ == "__main__":
    filler_agent.run()
