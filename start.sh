#!/bin/bash

# COPILOT PRO V - AI Master Tool Startup Script
# Copyright (c) 2025 Yadullah

echo "======================================"
echo "COPILOT PRO V - AI Master Tool"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
if ! pip install --upgrade pip; then
    echo "Error: Failed to upgrade pip"
    exit 1
fi

if ! pip install -r requirements.txt; then
    echo "Error: Failed to install dependencies from requirements.txt"
    exit 1
fi
echo "✓ Dependencies installed successfully"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "Please edit .env file with your API keys before running the server."
    echo ""
fi

# Determine which version to run
VERSION=${1:-"v2"}

if [ "$VERSION" == "v1" ]; then
    echo "Starting COPILOT PRO V (Version 1)..."
    uvicorn backend_main:app --reload --host 0.0.0.0 --port 8000
elif [ "$VERSION" == "v2" ]; then
    echo "Starting COPILOT PRO V (Version 2 - Enhanced)..."
    uvicorn backend_main_Version2:app --reload --host 0.0.0.0 --port 8000
else
    echo "Error: Invalid version. Use 'v1' or 'v2'"
    exit 1
fi
