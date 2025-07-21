#backend_api/agent_registry.py

import json
import os

AGENT_REGISTRY = {}

# 🌍 Correct path to the agent address file
AGENT_REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "agent_addresses.json")

# 🧠 Load the agent addresses if the file exists
if os.path.exists(AGENT_REGISTRY_PATH):
    try:
        with open(AGENT_REGISTRY_PATH, "r") as file:
            AGENT_REGISTRY = json.load(file)
    except Exception as e:
        print(f"❌ Failed to load agent registry: {e}")
else:
    print("⚠️ agent_addresses.json not found. Run `run_agents.py` first.")
