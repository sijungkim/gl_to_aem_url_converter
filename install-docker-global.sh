#!/bin/bash
# Install aem-docker global command

set -e

COMMAND="aem-docker"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"

# Create bin directory
mkdir -p "$BIN_DIR"

# Create global command
cat > "$BIN_DIR/$COMMAND" << EOF
#!/bin/bash
exec "$PROJECT_DIR/docker-run.sh" "\$@"
EOF

chmod +x "$BIN_DIR/$COMMAND"

# Add to PATH if needed
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "export PATH=\"$BIN_DIR:\$PATH\"" >> ~/.bashrc
    export PATH="$BIN_DIR:$PATH"
fi

echo "✅ Installed '$COMMAND' command"
echo "Usage: $COMMAND [branch]"
echo "Example: $COMMAND main"