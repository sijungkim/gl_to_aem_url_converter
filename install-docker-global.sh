#!/bin/bash

# AEM URL Converter - Global Docker Command Installer
# Creates a global command that can run the Docker version from anywhere

set -e

# Configuration
GLOBAL_COMMAND_NAME="aem-docker"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GLOBAL_SCRIPT_DIR="$HOME/.local/bin"
GLOBAL_SCRIPT_PATH="$GLOBAL_SCRIPT_DIR/$GLOBAL_COMMAND_NAME"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}Installing AEM URL Converter global Docker command...${NC}"

# Create ~/.local/bin if it doesn't exist
mkdir -p "$GLOBAL_SCRIPT_DIR"

# Create the global launcher script
cat > "$GLOBAL_SCRIPT_PATH" << EOF
#!/bin/bash

# AEM URL Converter - Global Docker Launcher
# This script can be run from anywhere and will find/run the Docker version

PROJECT_SCRIPT="$PROJECT_DIR/docker-run.sh"

# Check if project Docker script exists
if [[ ! -f "\$PROJECT_SCRIPT" ]]; then
    echo "Error: Docker runner script not found at \$PROJECT_SCRIPT"
    echo "Please check the installation or reinstall the global command."
    exit 1
fi

# Make sure the script is executable
chmod +x "\$PROJECT_SCRIPT"

# Run the Docker script with all arguments passed through
"\$PROJECT_SCRIPT" "\$@"
EOF

# Make the global script executable
chmod +x "$GLOBAL_SCRIPT_PATH"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo -e "${YELLOW}Adding ~/.local/bin to PATH...${NC}"

    # Add to .bashrc if it exists
    if [[ -f "$HOME/.bashrc" ]]; then
        echo '' >> "$HOME/.bashrc"
        echo '# AEM URL Converter - Add ~/.local/bin to PATH' >> "$HOME/.bashrc"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
        echo -e "${GREEN}Added to ~/.bashrc${NC}"
    fi

    # Add to .zshrc if it exists
    if [[ -f "$HOME/.zshrc" ]]; then
        echo '' >> "$HOME/.zshrc"
        echo '# AEM URL Converter - Add ~/.local/bin to PATH' >> "$HOME/.zshrc"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
        echo -e "${GREEN}Added to ~/.zshrc${NC}"
    fi

    # Export for current session
    export PATH="$HOME/.local/bin:$PATH"
    echo -e "${GREEN}PATH updated for current session${NC}"
fi

echo ""
echo -e "${GREEN}✅ Global Docker installation complete!${NC}"
echo ""
echo -e "${BLUE}Usage:${NC}"
echo "  $GLOBAL_COMMAND_NAME                # Run on solid branch"
echo "  $GLOBAL_COMMAND_NAME main           # Run on main branch"
echo "  $GLOBAL_COMMAND_NAME -c             # Use Docker Compose"
echo "  $GLOBAL_COMMAND_NAME --port 8502    # Custom port"
echo "  $GLOBAL_COMMAND_NAME --help         # Show all options"
echo ""
echo -e "${BLUE}You can now run from anywhere:${NC}"
echo "  cd /any/directory"
echo "  $GLOBAL_COMMAND_NAME"
echo ""
echo -e "${YELLOW}Note: You may need to restart your terminal or run:${NC}"
echo "  source ~/.bashrc"
echo -e "${YELLOW}for the command to be available in new terminals.${NC}"
echo ""
echo -e "${BLUE}🐳 Benefits of Docker approach:${NC}"
echo "  ✅ No local Python/venv setup needed"
echo "  ✅ Consistent environment across machines"
echo "  ✅ Complete isolation from host system"
echo "  ✅ Easy cleanup (just remove container)"
echo "  ✅ Production-ready deployment"