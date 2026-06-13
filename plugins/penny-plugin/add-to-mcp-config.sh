#!/bin/bash
# Add Penny QBO MCP Server to Claude's configuration
# Run this script once to register the server, then restart Cowork.

set -e

SERVER_PATH="/Users/tars/QBO/penny-plugin/mcp-server/server.py"
PYTHON_PATH=$(which python3)

# Locate the Claude config file
CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

if [ ! -f "$CLAUDE_CONFIG" ]; then
  echo "Creating new Claude config..."
  mkdir -p "$(dirname "$CLAUDE_CONFIG")"
  echo '{"mcpServers": {}}' > "$CLAUDE_CONFIG"
fi

# Back it up
cp "$CLAUDE_CONFIG" "$CLAUDE_CONFIG.backup"
echo "✅ Backed up existing config to claude_desktop_config.json.backup"

# Use Python to safely merge in the new server entry
python3 - <<EOF
import json

config_path = "$CLAUDE_CONFIG"
with open(config_path) as f:
    config = json.load(f)

if "mcpServers" not in config:
    config["mcpServers"] = {}

config["mcpServers"]["penny-qbo"] = {
    "command": "$PYTHON_PATH",
    "args": ["$SERVER_PATH"]
}

with open(config_path, "w") as f:
    json.dump(config, f, indent=2)

print("✅ penny-qbo server added to Claude MCP config")
print(f"   Config: $CLAUDE_CONFIG")
print(f"   Server: $SERVER_PATH")
EOF

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Done! Next steps:"
echo ""
echo "1. Restart Cowork completely (quit and reopen)"
echo "2. Ask Penny to run: qbo_authenticate"
echo "   This opens a browser window to connect to QuickBooks."
echo "   You only need to do this once."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
