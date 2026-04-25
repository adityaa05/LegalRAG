#!/bin/bash

# Get the project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( dirname "$SCRIPT_DIR" )"
cd "$PROJECT_ROOT"

echo "🚀 Starting LegalRAG System..."

# Start Backend in background
./scripts/run_backend.sh &
BACKEND_PID=$!

# Start Frontend in background
cd frontend && npm run dev &
FRONTEND_PID=$!

echo "✅ Backend started with PID $BACKEND_PID"
echo "✅ Frontend started with PID $FRONTEND_PID"
echo ""
echo "Backend: http://localhost:8001"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers."

# Trap SIGINT (Ctrl+C) to kill both processes
trap "kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT

# Keep script running
wait
