cd backend
HOST="0.0.0.0"
PORT="${PORT:-10000}"
if [ -z "$PORT" ]; then
    echo "Starting FastAPI app on $HOST:10000"
    python -m uvicorn app.main:app --host $HOST --port 10000
else
    echo "Starting FastAPI app on $HOST:$PORT"
    python -m uvicorn app.main:app --host $HOST --port $PORT
fi
