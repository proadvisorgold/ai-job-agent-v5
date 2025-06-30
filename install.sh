#!/bin/bash

echo "📦 Starting AI Job Agent v5 installation..."

# Select directory
read -p "💾 Where would you like to install the agent? (Default: current directory) " install_dir
install_dir="${install_dir:-.}"

mkdir -p "$install_dir"
cd "$install_dir" || exit 1

echo "📁 Working in: $(pwd)"

# Set up virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📚 Installing required Python packages..."
pip install --upgrade pip
pip install streamlit beautifulsoup4 requests playwright

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install

# Done — Launch the app
echo "🚀 Launching AI Job Agent Dashboard..."
streamlit run streamlit_app/MainDashboard.py

