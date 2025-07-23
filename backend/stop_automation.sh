#!/bin/bash

# JobHunter Automation Stop Script
echo "🛑 Stopping JobHunter Automation System..."

# Stop Celery worker
echo "🔄 Stopping Celery worker..."
pkill -f "celery.*worker"

# Stop Celery Beat
echo "⏰ Stopping Celery Beat..."
pkill -f "celery.*beat"

# Stop FastAPI server
echo "🌐 Stopping FastAPI server..."
pkill -f "uvicorn.*app.main:app"

# Optionally stop Redis and MongoDB (uncomment if you want to stop them)
# echo "🔴 Stopping Redis..."
# pkill redis-server

# echo "🔴 Stopping MongoDB..."
# pkill mongod

echo "✅ JobHunter Automation System stopped"