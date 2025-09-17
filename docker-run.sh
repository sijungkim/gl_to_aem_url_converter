#!/bin/bash
# AEM URL Converter - Simple Docker Runner

set -e

# Config
NAME="aem-converter"
PORT="${PORT:-8501}"
BRANCH="${1:-main}"

# Find project directory
if [[ -f "main.py" ]]; then
    PROJECT_DIR="$(pwd)"
elif [[ -f "/mnt/d/Cloud-Synced/illumina_projects/gl_to_aem_url_converter/main.py" ]]; then
    PROJECT_DIR="/mnt/d/Cloud-Synced/illumina_projects/gl_to_aem_url_converter"
elif [[ -f "/home/cjkim/illumina_project/gl_to_aem_url_converter/main.py" ]]; then
    PROJECT_DIR="/home/cjkim/illumina_project/gl_to_aem_url_converter"
else
    echo "❌ Project directory not found"
    exit 1
fi

cd "$PROJECT_DIR"

# Check git status
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "❌ You have uncommitted changes. Please commit or stash them first."
    exit 1
fi

# Switch branch if needed
CURRENT=$(git branch --show-current 2>/dev/null || echo "unknown")
if [[ "$CURRENT" != "$BRANCH" ]]; then
    echo "🔄 Switching to branch '$BRANCH'"
    git checkout "$BRANCH" || exit 1
fi

# Stop existing container
docker stop "$NAME" 2>/dev/null || true
docker rm "$NAME" 2>/dev/null || true

# Build and run
echo "🐳 Building and starting AEM URL Converter..."
docker build -t "$NAME" . || exit 1

echo "🌐 Starting at http://localhost:$PORT"
docker run -it --rm --name "$NAME" -p "$PORT:8501" "$NAME"