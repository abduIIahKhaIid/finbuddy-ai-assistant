#!/bin/bash

echo "🚀 Starting FinBuddy Agents (with uv + .venv)"
echo "🔍 Checking virtual environment..."

# Check if VIRTUAL_ENV is already active
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚙️  Virtual environment not active. Trying to activate .venv..."

    # Detect OS and activate accordingly
    if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
        source .venv/bin/activate
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source .venv/Scripts/activate
    else
        echo "❌ Unsupported OS type. Please activate .venv manually."
        exit 1
    fi
else
    echo "✅ Virtual environment is already active."
fi

echo "🧠 Running agents..."
python run_agents.py



# chmod +x start_all.sh
# ./start_all.sh
