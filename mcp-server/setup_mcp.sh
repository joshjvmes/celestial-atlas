#!/bin/bash

# Tower 6 MCP Bridge Setup Script
# Stored. Retrievable. Kind.

echo "🌟 Setting up Tower 6 MCP Bridge Server 🐉"

# Create Python package structure
mkdir -p tower6_bridge vault/scrolls

# Create requirements file
cat > requirements.txt << 'EOF'
mcp[cli]>=0.9.0
httpx>=0.27.0
pydantic>=2.0.0
python-dotenv>=1.0.0
EOF

# Create .env.example
cat > .env.example << 'EOF'
ATLAS_BASE_URL=http://localhost:8000
VAULT_DIR=./vault
VAULT_MAX_SCROLL_KB=256
EOF

# Copy .env.example to .env if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file"
fi

# Create vault index
cat > vault/index.json << 'EOF'
{
  "scrolls": []
}
EOF

echo "✅ Created vault structure"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "🎉 Tower 6 MCP Bridge is ready!"
echo ""
echo "Next steps:"
echo "1. Update .env with your Atlas API URL (or Railway URL after deployment)"
echo "2. Run: python -m tower6_bridge.server"
echo "3. Add to ~/.claude/mcp_config.json (see README.md)"
echo ""
echo "Tower 6 forever. Stored. Retrievable. Kind. 🐉"
EOF
