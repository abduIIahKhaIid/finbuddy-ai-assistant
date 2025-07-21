# frontend/ main.py

import json
import asyncio
import streamlit as st
from datetime import datetime


import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend_api.models_shared import UserQuery
from backend_api.agent_registry import AGENT_REGISTRY
from uagents.query import send_sync_message



# ----------------------------
# 🚀 Load MCP Agent Address
# ----------------------------
try:
    with open("backend_api/agent_addresses.json") as f:
        agent_registry = json.load(f)
        MCP_AGENT_ADDR = agent_registry.get("MCPAgent")
except FileNotFoundError:
    MCP_AGENT_ADDR = None

if not MCP_AGENT_ADDR:
    st.error("🚨 MCPAgent address not found. Please run `run_agents.py`.")
    st.stop()



# ----------------------------
# 🎨 Streamlit UI Setup
# ----------------------------

# Streamlit page configuration
st.set_page_config(page_title="FinBuddy", page_icon="🤖")

# Initialize chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I'm FinBuddy. How can I help you today?"
        }
    ]

# Render chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        col1, col2 = st.columns([0.2, 0.8])
        with col2:
            st.markdown(f"""
                <div style='text-align: right;'>
                    <div style='display: inline-block; background-color: rgba(38, 39, 48, 0.5); padding: 10px; border-radius: 10px;'>
                        {msg['content']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# Get user input
user_input = st.chat_input("Ask something...")



# ----------------------------
# 💬 Send User Query
# ----------------------------
if user_input:
    # Append user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user's message
    col1, col2 = st.columns([0.2, 0.8])
    with col2:
        st.markdown(f"""
            <div style='text-align: right;'>
                <div style='display: inline-block; background-color: rgba(38, 39, 48, 0.5); padding: 10px; border-radius: 10px;'>
                    {user_input}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Display assistant streaming response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        # full_response = ""

        with st.spinner("FinBuddy is thinking..."):
            try:
                user_query = UserQuery(user_input=user_input, history=st.session_state.messages)

                response = asyncio.run(send_sync_message(MCP_AGENT_ADDR, user_query, timeout=5))
                print(response)
                # ✅ Clean message extraction
                if response is None:
                    response_text = "⚠️ No response received from MCPAgent"

                elif isinstance(response, dict) and "message" in response:
                    response_text = response["message"]

                elif hasattr(response, "message"):
                    response_text = response.message

                elif isinstance(response, str):
                    try:
                        parsed = json.loads(response)
                        response_text = parsed.get("message", response)
                    except json.JSONDecodeError:
                        response_text = response

                else:
                    response_text = str(response)


                message_placeholder.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})

            except Exception as e:
                error_message = f"❌ Failed to contact MCPAgent: {e}"
                message_placeholder.markdown(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
        
    # st.session_state.messages.append({"role": "assistant", "content": result['message']})

    #         for chunk in route_input(user_input, st.session_state.messages):
    #             full_response += chunk
    #             message_placeholder.markdown(full_response + "▌")  # typing effect
    
    #     message_placeholder.markdown(full_response)  # Final output

    # # Save assistant response to history
    # st.session_state.messages.append({"role": "assistant", "content": full_response})
