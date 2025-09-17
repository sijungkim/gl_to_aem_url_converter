# 🚀 AEM URL Converter - Deployment Guide

## 🎯 Docker-Only Deployment Strategy

This application has been optimized for **Docker-only deployment** for maximum portability, consistency, and ease of use.

## 📦 What's Included

### **Core Files:**
- `Dockerfile` - Optimized production container
- `docker-compose.yml` - Multi-container orchestration
- `docker-run.sh` - Smart Docker runner script
- `install-docker-global.sh` - Global command installer
- `requirements.txt` - Minimal production dependencies (streamlit + pandas only)

### **Application Files:**
- `main.py` - Application entry point
- `app.py` - Streamlit application layer
- `di_container.py` - Dependency injection container
- `core/` - Business logic & domain models
- `services/` - Service implementations
- `presentation/` - UI/presentation layer

### **Documentation:**
- `README.md` - Docker-focused usage guide
- `DOCKER_TROUBLESHOOTING.md` - Connection issue solutions
- `MULTI_ZIP_FEATURE.md` - Feature documentation

## 🐳 Quick Deployment

### **Option 1: Global Command (Recommended)**
```bash
# One-time setup
cd gl_to_aem_url_converter
./install-docker-global.sh
source ~/.bashrc

# Use from anywhere
cd /any/directory
aem-docker                    # Latest features (solid branch)
aem-docker main              # Stable (main branch)
```

### **Option 2: Direct Docker**
```bash
# From project directory
./docker-run.sh              # Smart runner
docker-compose up --build    # Using compose
docker run -p 8501:8501 gl_to_aem_url:latest  # Manual
```

## 🌐 Access URLs

- **Windows Browser**: `http://localhost:8501` ⭐
- **WSL Browser**: `http://127.0.0.1:8501`
- **Alternative**: `http://[WSL-IP]:8501`

## 🔧 Removed Alternative Methods

The following methods have been **removed** to keep the project clean and focused:

- ❌ `run.sh` / `run.bat` - Shell scripts for local Python
- ❌ `Makefile` - Make-based workflow
- ❌ `setup-alias.sh` - Shell alias setup
- ❌ `install-global.sh` - Non-Docker global installer
- ❌ `USAGE_GUIDE.md` - Multi-method usage guide
- ❌ Development dependencies in requirements.txt

## ✅ Benefits of Docker-Only Approach

### **🌍 Universal Compatibility**
- Works on any system with Docker
- No Python version conflicts
- No virtual environment setup
- No dependency management

### **🚀 Performance**
- Optimized container (~240KB build context)
- Layer caching for fast rebuilds
- Minimal dependencies (only streamlit + pandas)
- Health monitoring built-in

### **🔒 Reliability**
- Complete isolation from host system
- Consistent environment across machines
- No host system pollution
- Easy cleanup and reset

### **🎯 Developer Experience**
- Run from anywhere in WSL
- Automatic branch management
- Volume mounting for development
- Production-ready deployment

## 📋 Environment Variables

```bash
# Optional customization
export AEM_HOST="https://your-aem-host.com"
export SOURCE_LANG="en"
export TEMPLATE_FILE="custom_template.html"
```

## 🐛 Troubleshooting

See [DOCKER_TROUBLESHOOTING.md](DOCKER_TROUBLESHOOTING.md) for:
- Connection refused solutions
- WSL2 networking tips
- Alternative access methods
- Port configuration
- Container debugging

## 🎉 Success Criteria

✅ **Container builds successfully**
✅ **Global command works from anywhere**
✅ **Application accessible via browser**
✅ **Multi-ZIP processing functional**
✅ **Clean, minimal codebase**
✅ **Production-ready deployment**

## 🔄 Development Workflow

```bash
# Daily development
aem-docker                    # Run latest features

# Feature development
git checkout -b feature/new-feature
aem-docker feature/new-feature

# Testing different branches
aem-docker solid             # Latest features
aem-docker main              # Stable version

# Production deployment
docker-compose up -d --build  # Background mode
```

This deployment strategy provides a **clean, modern, and maintainable** approach to running the AEM URL Converter application with minimal overhead and maximum portability.