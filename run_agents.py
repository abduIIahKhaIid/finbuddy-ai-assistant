# run_agents.py

import os
import json
import subprocess
import time
from importlib import import_module

# 🗂️ Active agents (add new ones here as needed)
ACTIVE_AGENTS = [
    "agents.mcp_agent",
    "agents.saving_agent",
    "agents.reminder_agent",
    "agents.budget_agent",
    "agents.pause_agent",
    "agents.decline_agent",
    "agents.credit_agent",
    "agents.progress_agent",
    "agents.media_agent",
    "agents.share_agent"
]


def launch_agents():
    processes = []

    print("🚀 Launching all FinBuddy agents via subprocess...\n")

    for agent_module in ACTIVE_AGENTS:
        try:
            print(f"🔹 Starting agent from: {agent_module}")

            # 🧠 Dynamically import the agent module
            module = import_module(agent_module)
            agent = getattr(module, [attr for attr in dir(module) if attr.endswith("_agent")][0])

            # 🗂️ Save name & address
            agent_info[agent.name] = agent.address

            # 🏃 Start agent subprocess
            file_path = agent_module.replace(".", "/") + ".py"
            p = subprocess.Popen(["python", file_path])
            processes.append(p)

        except Exception as e:
            print(f"❌ Failed to start agent from {agent_module}: {e}")

    return processes


if __name__ == "__main__":
    # 🛠️ Setup
    os.makedirs("backend_api", exist_ok=True)
    agent_info = {}

    # ▶️ Start all agents
    processes = launch_agents()

    # 💾 Save agent addresses
    with open("backend_api/agent_addresses.json", "w") as f:
        json.dump(agent_info, f, indent=4)
        print("\n✅ Agent addresses saved to backend_api/agent_addresses.json")

    print("\n🟢 All agents are running. Press Ctrl+C to stop.\n")

    try:
        # Keep script alive while agents run
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping all agents...")
        for p in processes:
            p.terminate()
        print("✅ All agents stopped.")
