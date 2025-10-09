#!/bin/bash
# Bash Setup Script for Memory Forensics Framework
# Linux/macOS-specific setup and configuration

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_header() {
    echo -e "${CYAN}$1${NC}"
}

# Function to run command and check result
run_command() {
    local cmd="$1"
    local description="$2"
    
    echo -e "${YELLOW}🔧 $description...${NC}"
    
    if eval "$cmd"; then
        print_status "$description completed successfully"
        return 0
    else
        print_error "$description failed"
        return 1
    fi
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect package manager
detect_package_manager() {
    if command_exists apt-get; then
        echo "apt"
    elif command_exists yum; then
        echo "yum"
    elif command_exists dnf; then
        echo "dnf"
    elif command_exists pacman; then
        echo "pacman"
    elif command_exists brew; then
        echo "brew"
    else
        echo "unknown"
    fi
}

# Function to install system dependencies
install_system_dependencies() {
    local pkg_manager=$(detect_package_manager)
    
    print_header "Installing system dependencies..."
    
    case $pkg_manager in
        "apt")
            run_command "sudo apt-get update" "Updating package list"
            run_command "sudo apt-get install -y python3 python3-pip python3-venv git build-essential" "Installing Python and build tools"
            ;;
        "yum")
            run_command "sudo yum update -y" "Updating package list"
            run_command "sudo yum install -y python3 python3-pip git gcc gcc-c++ make" "Installing Python and build tools"
            ;;
        "dnf")
            run_command "sudo dnf update -y" "Updating package list"
            run_command "sudo dnf install -y python3 python3-pip git gcc gcc-c++ make" "Installing Python and build tools"
            ;;
        "pacman")
            run_command "sudo pacman -Sy" "Updating package list"
            run_command "sudo pacman -S --noconfirm python python-pip git base-devel" "Installing Python and build tools"
            ;;
        "brew")
            run_command "brew update" "Updating Homebrew"
            run_command "brew install python3 git" "Installing Python and Git"
            ;;
        *)
            print_warning "Unknown package manager. Please install Python 3.9+, pip, and git manually."
            ;;
    esac
}

# Function to check Python version
check_python_version() {
    print_header "Checking Python installation..."
    
    if command_exists python3; then
        local python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
        local major_version=$(echo $python_version | cut -d'.' -f1)
        local minor_version=$(echo $python_version | cut -d'.' -f2)
        
        if [ "$major_version" -eq 3 ] && [ "$minor_version" -ge 9 ]; then
            print_status "Python $python_version detected (compatible)"
            return 0
        else
            print_error "Python 3.9+ is required. Found: $python_version"
            return 1
        fi
    else
        print_error "Python 3 not found. Please install Python 3.9+"
        return 1
    fi
}

# Function to install Python requirements
install_python_requirements() {
    print_header "Installing Python requirements..."
    
    # Check if requirements.txt exists
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found"
        return 1
    fi
    
    # Install requirements
    run_command "python3 -m pip install --user -r requirements.txt" "Installing Python requirements"
    
    # Install memory forensics tools specifically
    local tools=("volatility3" "rekall" "psutil" "yara-python")
    
    for tool in "${tools[@]}"; do
        print_info "Installing $tool..."
        run_command "python3 -m pip install --user $tool" "Installing $tool"
    done
}

# Function to create project directories
create_project_directories() {
    print_header "Creating project directories..."
    
    local directories=(
        "src/framework"
        "src/utils"
        "src/tests"
        "docs/reports"
        "docs/guides"
        "docs/presentations"
        "data/dumps"
        "data/results"
        "logs"
        "week1" "week2" "week3" "week4" "week5" "week6" "week7"
    )
    
    for dir in "${directories[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            print_status "Created directory: $dir"
        else
            print_info "Directory already exists: $dir"
        fi
    done
}

# Function to create .gitignore
create_gitignore() {
    print_header "Creating .gitignore..."
    
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Memory dumps and sensitive data
data/dumps/*.dmp
data/dumps/*.raw
data/dumps/*.vmem
data/results/*.json
*.log

# OS specific
.DS_Store
Thumbs.db

# Project specific
logs/
temp/
cache/
EOF
    
    print_status ".gitignore created"
}

# Function to setup Git repository
setup_git() {
    print_header "Setting up Git repository..."
    
    if [ ! -d ".git" ]; then
        run_command "git init" "Initializing Git repository"
        run_command "git add ." "Adding files to Git"
        run_command 'git commit -m "Initial commit: Framework setup"' "Creating initial commit"
        print_status "Git repository initialized"
    else
        print_info "Git repository already initialized"
    fi
}

# Function to verify installation
verify_installation() {
    print_header "Verifying installation..."
    
    local test_imports=("volatility3" "rekall" "psutil" "yara")
    
    for module in "${test_imports[@]}"; do
        if python3 -c "import $module; print('$module import successful')" 2>/dev/null; then
            print_status "$module import successful"
        else
            print_error "$module import failed"
            return 1
        fi
    done
    
    return 0
}

# Function to run tests
run_tests() {
    print_header "Running basic tests..."
    
    if [ -d "src/tests" ]; then
        run_command "python3 -m pytest src/tests/ -v" "Running tests"
    else
        print_warning "No tests found. Skipping test execution."
    fi
}

# Main setup function
main() {
    print_header "🚀 Memory Forensics Framework Setup (Linux/macOS)"
    echo "=================================================="
    
    # Check if running as root (not recommended)
    if [ "$EUID" -eq 0 ]; then
        print_warning "Running as root is not recommended. Consider using a regular user account."
    fi
    
    # Install system dependencies
    install_system_dependencies
    
    # Check Python version
    check_python_version
    
    # Create project directories
    create_project_directories
    
    # Create .gitignore
    create_gitignore
    
    # Install Python requirements
    install_python_requirements
    
    # Setup Git repository
    setup_git
    
    # Verify installation
    verify_installation
    
    # Run tests
    run_tests
    
    echo "=================================================="
    print_status "🎉 Setup completed successfully!"
    echo ""
    print_info "Next steps:"
    echo "1. Run tests: pytest src/tests/ -v"
    echo "2. Start with Week 1: python3 scripts/week1/setup.py"
    echo "3. Read documentation: docs/guides/user_guide.md"
    echo ""
    print_info "For additional system dependencies, you may need to install:"
    echo "- libyara-dev (for YARA support)"
    echo "- libcapstone-dev (for Capstone support)"
    echo "- libkeystone-dev (for Keystone support)"
}

# Run main function
main "$@"
