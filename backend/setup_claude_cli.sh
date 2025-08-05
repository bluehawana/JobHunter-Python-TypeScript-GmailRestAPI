#!/bin/bash
"""
Setup Claude CLI for third-party API
"""

echo "🚀 Setting up Claude CLI for JobHunter"
echo "=================================="

# Export environment variables
export ANTHROPIC_AUTH_TOKEN=REMOVED_SECRET
export ANTHROPIC_BASE_URL=https://anyrouter.top

echo "✅ Environment variables set:"
echo "   ANTHROPIC_AUTH_TOKEN: ${ANTHROPIC_AUTH_TOKEN:0:20}..."
echo "   ANTHROPIC_BASE_URL: $ANTHROPIC_BASE_URL"
echo ""

echo "🤖 Starting Claude CLI setup..."
echo "Please follow these steps:"
echo "1. Choose your preferred theme + Enter"
echo "2. Confirm security notice + Enter" 
echo "3. Use default Terminal configuration + Enter"
echo "4. Trust working directory + Enter"
echo ""

# Start Claude CLI
claude