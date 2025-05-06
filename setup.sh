#!/bin/bash
# Setup script for OpenAI Image Generator

# Print colored text
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}===== OpenAI Image Generator Setup =====${NC}"
echo

# Check for Python installation
echo -e "${YELLOW}Checking for Python...${NC}"
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
    echo "Python 3 found."
elif command -v python &>/dev/null; then
    PYTHON_CMD=python
    echo "Python found."
else
    echo -e "${RED}Python not found. Please install Python 3.6+ to continue.${NC}"
    exit 1
fi

# Check for tkinter
echo -e "${YELLOW}Checking for tkinter...${NC}"
if $PYTHON_CMD -c "import tkinter; print('Tkinter is installed.')" 2>/dev/null; then
    echo "tkinter is installed."
else
    echo -e "${RED}tkinter is not installed or not properly configured.${NC}"
    echo "Please install tkinter before continuing:"
    echo "  - On Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  - On Fedora: sudo dnf install python3-tkinter"
    echo "  - On macOS (using Homebrew): brew install python-tk"
    echo "  - On Windows: tkinter should be included with standard Python installations"
    echo
    read -p "Do you want to continue anyway? (y/n): " continue_anyway
    if [[ "$continue_anyway" != "y" && "$continue_anyway" != "Y" ]]; then
        echo "Setup aborted. Please install tkinter and run the script again."
        exit 1
    fi
    echo "Continuing without tkinter. The application may not work properly."
fi

# Check for virtual environment tool
echo -e "${YELLOW}Setting up virtual environment...${NC}"
if command -v uv &>/dev/null; then
    echo "Using uv to create virtual environment..."
    uv venv
    ACTIVATE_CMD="source .venv/bin/activate"
else
    echo "Using python venv to create virtual environment..."
    $PYTHON_CMD -m venv .venv
    ACTIVATE_CMD="source .venv/bin/activate"
fi

# Activate virtual environment
echo "Activating virtual environment..."
eval "$ACTIVATE_CMD"

# Install dependencies
echo -e "${YELLOW}Installing required packages...${NC}"
if command -v uv &>/dev/null; then
    uv pip install -r requirements.txt
else
    $PYTHON_CMD -m pip install -r requirements.txt
fi

# Check for .env file and create if it doesn't exist
echo -e "${YELLOW}Checking for .env file...${NC}"
if [ ! -f .env ]; then
    echo ".env file not found. Let's create one."
    echo -n "Enter your OpenAI API key: "
    read -r API_KEY
    echo "OPENAI_API_KEY=$API_KEY" > .env
    echo ".env file created with your API key."
else
    echo ".env file already exists."
fi

echo -e "${GREEN}Setup complete!${NC}"
echo
echo "To start using the image generator:"
echo "1. Make sure you're in the virtual environment:"
echo "   $ACTIVATE_CMD"
echo "2. Run the script:"
echo "   $PYTHON_CMD openai_image_generator.py"
echo
echo "Enjoy generating images with DALL-E!"
