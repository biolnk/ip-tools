#!/bin/bash

echo "Installing IP Tools Requirements..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )\d+\.\d+')
if (( $(echo "$python_version < 3.7" | bc -l) )); then
    echo "Error: Python 3.7+ required. Found $python_version"
    exit 1
fi

# Install pip requirements
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Install system dependencies (Linux only)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y whois
    elif command -v yum &> /dev/null; then
        sudo yum install -y whois
    fi
fi

echo "Installation complete!"
