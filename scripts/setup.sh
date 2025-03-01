PYTHON="python3"
PIP="$PYTHON -m pip"
NPM="npm"
VENV_DIR="venv"

# Create a virtual environment
echo "Creating virtual environment in $VENV_DIR..."
$PYTHON -m venv $VENV_DIR
if [ $? -ne 0 ]; then
  echo "Failed to create virtual environment. Ensure Python 3 is properly installed."
  exit 1
fi
echo "Virtual environment created successfully."

# Activate the virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Install backend dependencies
$PIP install -r backend/requirements.txt
cd frontend

# Install frontend dependencies
$NPM install

# Build the frontend
$NPM run build

# Move to root directory
cd ..

echo "Setup complete."