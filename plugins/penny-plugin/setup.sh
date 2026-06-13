#!/bin/bash
# Penny QBO Plugin Setup
# Run this once to install dependencies and store your QBO credentials securely.

set -e

echo ""
echo "🪙  Penny QBO Plugin Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. Install Python dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r "$(dirname "$0")/mcp-server/requirements.txt" --break-system-packages --quiet
echo "   ✅ Dependencies installed"

# 2. Create secure credentials directory
CONFIG_DIR="$HOME/.penny-qbo"
mkdir -p "$CONFIG_DIR"
chmod 700 "$CONFIG_DIR"

# 3. Store credentials
CONFIG_FILE="$CONFIG_DIR/config.json"

echo ""
echo "🔑 Enter your Intuit Developer credentials:"
echo "   (Find these at developer.intuit.com → your app → Keys & OAuth)"
echo ""
read -p "   Client ID:     " CLIENT_ID
read -s -p "   Client Secret: " CLIENT_SECRET
echo ""

cat > "$CONFIG_FILE" <<EOF
{
  "client_id": "$CLIENT_ID",
  "client_secret": "$CLIENT_SECRET"
}
EOF
chmod 600 "$CONFIG_FILE"
echo "   ✅ Credentials stored at $CONFIG_FILE (private, owner-read-only)"

# 4. Print MCP config snippet
SERVER_PATH="$(cd "$(dirname "$0")/mcp-server" && pwd)/server.py"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅  Setup complete!"
echo ""
echo "📋 Add this to your Claude MCP config"
echo "   (claude_desktop_config.json or Cowork plugin config):"
echo ""
echo '   "penny-qbo": {'
echo '     "command": "python3",'
echo "     \"args\": [\"$SERVER_PATH\"]"
echo '   }'
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "▶️  After adding to MCP config, restart Cowork, then ask"
echo "   Penny to run qbo_authenticate to connect to QuickBooks."
echo ""
