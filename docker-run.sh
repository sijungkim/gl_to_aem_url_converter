#!/bin/bash

# AEM URL Converter - Smart Docker Runner
# Run from anywhere - automatically detects project directory and builds/runs

set -e

# Configuration
CONTAINER_NAME="gl-to-aem-url"
IMAGE_NAME="gl_to_aem_url:latest"
PORT="8501"
DEFAULT_BRANCH="solid"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Function to find project directory
find_project_dir() {
    local current_dir="$(pwd)"
    local search_dir="$current_dir"

    # First check if we're already in the project directory
    if [[ -f "main.py" && -f "requirements.txt" && -f "Dockerfile" ]]; then
        echo "$current_dir"
        return 0
    fi

    # Search common locations
    local possible_dirs=(
        "/mnt/d/Cloud-Synced/illumina_projects/gl_to_aem_url_converter"
        "/home/cjkim/illumina_project/gl_to_aem_url_converter"
        "$HOME/gl_to_aem_url_converter"
        "$HOME/projects/gl_to_aem_url_converter"
    )

    for dir in "${possible_dirs[@]}"; do
        if [[ -f "$dir/main.py" && -f "$dir/requirements.txt" && -f "$dir/Dockerfile" ]]; then
            echo "$dir"
            return 0
        fi
    done

    print_error "Could not find AEM URL Converter project directory!"
    print_error "Please run this script from the project directory or update the search paths."
    exit 1
}

# Function to check if we're on the desired branch
check_and_switch_branch() {
    local target_branch=${1:-$DEFAULT_BRANCH}
    local current_branch=$(git branch --show-current 2>/dev/null || echo "unknown")

    if [[ "$current_branch" != "$target_branch" ]]; then
        print_warning "Currently on branch '$current_branch', switching to '$target_branch'"

        # Check for uncommitted changes
        if ! git diff-index --quiet HEAD -- 2>/dev/null; then
            print_error "You have uncommitted changes. Please commit or stash them first."
            git status --porcelain
            exit 1
        fi

        # Switch to target branch
        if git checkout "$target_branch" 2>/dev/null; then
            print_success "Switched to branch '$target_branch'"
        else
            print_error "Failed to switch to branch '$target_branch'"
            exit 1
        fi
    else
        print_success "Already on correct branch: '$target_branch'"
    fi
}

# Function to stop existing container
stop_existing_container() {
    if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
        print_status "Stopping existing container..."
        docker stop "$CONTAINER_NAME" > /dev/null 2>&1
        docker rm "$CONTAINER_NAME" > /dev/null 2>&1
        print_success "Existing container stopped"
    fi
}

# Function to build Docker image
build_image() {
    print_status "Building Docker image..."
    if docker build -t "$IMAGE_NAME" . > /dev/null 2>&1; then
        print_success "Docker image built successfully"
    else
        print_error "Failed to build Docker image"
        exit 1
    fi
}

# Function to run container
run_container() {
    local project_dir="$1"

    print_status "Starting AEM URL Converter in Docker..."
    print_status "🌐 Application URLs:"
    print_status "   Windows Browser: http://localhost:$PORT"
    print_status "   WSL Browser:     http://127.0.0.1:$PORT"
    print_status "   Alternative:     http://$(hostname -I | awk '{print $1}'):$PORT"
    print_status "📁 Using project directory: $project_dir"
    print_status "🔄 Press Ctrl+C to stop the application"
    print_status ""
    print_status "💡 If connection refused, try the alternative URL above"
    echo ""

    # Run container with volume mount for development
    docker run -it --rm \
        --name "$CONTAINER_NAME" \
        -p "$PORT:8501" \
        -v "$project_dir:/app" \
        -e AEM_HOST="${AEM_HOST:-https://prod-author.illumina.com}" \
        -e SOURCE_LANG="${SOURCE_LANG:-en}" \
        -e TEMPLATE_FILE="${TEMPLATE_FILE:-template.html}" \
        "$IMAGE_NAME"
}

# Function to run with Docker Compose (if available)
run_with_compose() {
    local project_dir="$1"

    if [[ -f "$project_dir/docker-compose.yml" ]]; then
        print_status "Using Docker Compose..."
        cd "$project_dir"

        # Stop any existing compose services
        docker-compose down > /dev/null 2>&1 || true

        # Start with compose
        print_success "🚀 Starting with Docker Compose..."
        docker-compose up --build
    else
        print_warning "docker-compose.yml not found, using direct Docker run"
        run_container "$project_dir"
    fi
}

# Help function
show_help() {
    echo "AEM URL Converter - Smart Docker Runner"
    echo ""
    echo "Usage: $0 [OPTIONS] [branch]"
    echo ""
    echo "Arguments:"
    echo "  branch    Git branch to use (default: $DEFAULT_BRANCH)"
    echo ""
    echo "Options:"
    echo "  -c, --compose    Use Docker Compose (if available)"
    echo "  -p, --port PORT  Use custom port (default: $PORT)"
    echo "  --rebuild        Force rebuild of Docker image"
    echo "  -h, --help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                    # Run on $DEFAULT_BRANCH branch"
    echo "  $0 main              # Run on main branch"
    echo "  $0 -c                # Use Docker Compose"
    echo "  $0 --port 8502       # Use port 8502"
    echo "  $0 --rebuild solid   # Force rebuild and run on solid"
    echo ""
    echo "Environment Variables:"
    echo "  AEM_HOST      AEM host URL (default: https://prod-author.illumina.com)"
    echo "  SOURCE_LANG   Source language (default: en)"
    echo "  TEMPLATE_FILE Template file name (default: template.html)"
    echo ""
    echo "Features:"
    echo "  ✅ Automatic project directory detection"
    echo "  ✅ Branch switching with safety checks"
    echo "  ✅ Docker image building and management"
    echo "  ✅ Container lifecycle management"
    echo "  ✅ Development volume mounting"
    echo "  ✅ Environment variable support"
}

# Main execution
main() {
    local target_branch="$DEFAULT_BRANCH"
    local use_compose=false
    local force_rebuild=false
    local custom_port=""

    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -c|--compose)
                use_compose=true
                shift
                ;;
            -p|--port)
                custom_port="$2"
                PORT="$custom_port"
                shift 2
                ;;
            --rebuild)
                force_rebuild=true
                shift
                ;;
            *)
                target_branch="$1"
                shift
                ;;
        esac
    done

    echo "================================================================"
    echo "🐳 AEM URL Converter - Smart Docker Runner"
    echo "================================================================"

    # Find and navigate to project directory
    local project_dir=$(find_project_dir)
    print_success "Found project directory: $project_dir"
    cd "$project_dir"

    # Check Docker availability
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed or not in PATH"
        exit 1
    fi

    # Check and switch branch
    check_and_switch_branch "$target_branch"

    # Stop existing container
    stop_existing_container

    # Build image (force rebuild if requested)
    if [[ "$force_rebuild" == true ]] || ! docker images -q "$IMAGE_NAME" | grep -q .; then
        build_image
    else
        print_success "Using existing Docker image"
    fi

    echo ""
    echo "================================================================"
    print_success "🎉 Setup complete! Starting application..."
    echo "================================================================"
    echo ""

    # Run container
    if [[ "$use_compose" == true ]]; then
        run_with_compose "$project_dir"
    else
        run_container "$project_dir"
    fi
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi

# Run main function with all arguments
main "$@"