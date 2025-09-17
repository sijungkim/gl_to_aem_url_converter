# 🐳 AEM URL Converter

Docker-based tool for processing GlobalLink translated ZIP files and generating AEM editor URLs.

## Features
- Multi-ZIP batch processing with smart deduplication
- AEM editor URL generation for Korean/Japanese content
- HTML report generation with source tracking
- Clean architecture following SOLID principles

## 🚀 Quick Start

### Prerequisites
- Docker (native Docker in WSL/Linux)

### Installation
```bash
git clone <repository-url>
cd gl_to_aem_url_converter
./install-docker-global.sh
source ~/.bashrc
```

### Usage
```bash
# Run from anywhere
aem-docker                # Use main branch
aem-docker solid         # Use solid branch

# Alternative methods
./docker-run.sh          # From project directory
docker-compose up --build
```

### Access
Application runs at: `http://localhost:8501`

If connection fails, try:
- `http://127.0.0.1:8501` (WSL)
- Different port: `PORT=8502 aem-docker`

## 📚 Usage

1. **Launch**: Run `aem-docker`
2. **Upload**: Select one or multiple ZIP files
3. **Process**: View results in Summary/Japanese/Korean tabs
4. **Download**: Export HTML reports with AEM editor links

### Multi-ZIP Features
- **Smart Deduplication**: Removes duplicate URLs (latest file wins)
- **Source Tracking**: Shows which ZIP each URL originated from
- **Batch Processing**: Process multiple files simultaneously

## 🔧 Customization

### Environment Variables
```bash
export AEM_HOST="https://your-aem-host.com"
export SOURCE_LANG="en"
export TEMPLATE_FILE="custom_template.html"
```

### Adding Languages
Update `core/config.py`:
```python
self.language_mapping = {
    'ko-KR': 'ko',
    'ja-JP': 'ja',
    'zh-CN': 'zh'  # New language
}
```

## 🐛 Troubleshooting

### Connection Issues
```bash
# Check container status
docker ps

# Test connection
curl http://localhost:8501

# View logs
docker logs aem-converter

# Rebuild if needed
aem-docker --rebuild
```

## 📁 Architecture

```
gl_to_aem_url_converter/
├── core/           # Domain models & config
├── services/       # Business logic
├── presentation/   # UI components
├── main.py         # Application entry point
└── Dockerfile      # Container config
```

Built with SOLID principles for maintainability and extensibility.