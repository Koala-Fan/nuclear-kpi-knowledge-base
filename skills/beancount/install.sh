#!/bin/bash

# Install script for Beancount skill dependencies

echo "Installing Beancount for Clawdbot Beancount skill..."

# Check if pip is available
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "Error: pip is not installed. Please install pip first."
    exit 1
fi

# Try pip3 first (more common on newer systems)
if command -v pip3 &> /dev/null; then
    PIP_CMD=pip3
else
    PIP_CMD=pip
fi

echo "Using $PIP_CMD to install beancount..."

# Install beancount
$PIP_CMD install beancount

if [ $? -eq 0 ]; then
    echo "Beancount installed successfully!"
    echo "Verifying installation..."
    python3 -c "import beancount; print('Beancount version:', beancount.__version__)" 2>/dev/null || echo "Beancount installed but not accessible from Python"
    
    # Check if the command-line tools are available
    if command -v bean-check &> /dev/null; then
        echo "Beancount command-line tools are available:"
        bean-check --version
    else
        echo "Warning: Beancount command-line tools not found in PATH"
        echo "You may need to add the Python scripts directory to your PATH"
        echo "Common locations for the tools:"
        echo "  - ~/.local/bin"
        echo "  - /usr/local/bin"
        echo "  - $(python3 -m site --user-base)/bin"
    fi
else
    echo "Failed to install beancount"
    exit 1
fi

echo ""
echo "Installation complete! The Beancount skill should now work with Clawdbot."