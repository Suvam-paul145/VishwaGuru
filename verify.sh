#!/bin/bash
python start-backend.py > backend.log 2>&1 &
BACKEND_PID=$!
cd frontend && npm run dev -- --port 5173 > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Waiting for servers to start..."
sleep 20
echo "Running verification..."
python verification/verify_new_detectors.py
echo "Verification complete. Stopping servers..."
kill $BACKEND_PID
kill $FRONTEND_PID
