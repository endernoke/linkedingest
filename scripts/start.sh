cd backend
HOST="0.0.0.0"
PORT="${PORT:-10000}"
if [ -z "$PORT" ]; then
    echo "Starting FastAPI app on $HOST:10000"
    uvicorn app.main:app --host $HOST --port 10000
else
    echo "Starting FastAPI app on $HOST:$PORT"
    uvicorn app.main:app --host $HOST --port $PORT
fi