---
title: "AEM URL Converter"
description: "A Docker-based tool for processing GlobalLink translated ZIP files and generating AEM editor URLs for MSM (Multi-Site Manager) content review and updates across English, target languages, and SPAC target languages. Features multi-ZIP batch processing with intelligent deduplication and source tracking."
architect: "Sijung Kim"
authors: ["Sijung Kim", "Claude", "Gemini"]
reviewed_by: "Sijung Kim"
created_date: "2025-09-15"
last_modified: "2025-09-18"
version: "2.1.0"
license: "MIT"
tags: ["AEM", "GlobalLink", "Translation", "SOLID", "Clean Architecture", "Docker", "Multi-ZIP", "Batch Processing"]
---

# 🐳 AEM URL Converter

A Docker-based tool for processing GlobalLink translated ZIP files and generating AEM editor URLs for MSM (Multi-Site Manager) content review and updates. The application analyzes downloaded GlobalLink translation packages and provides direct AEM editor links for English language master, target language content, and SPAC target language pages, streamlining the multilingual content management workflow.

## 🚀 **Multi-ZIP Batch Processing**

✨ **Version 2.1.0** introduces powerful multi-ZIP batch processing capabilities:
- **Batch Upload**: Select and process multiple ZIP files simultaneously
- **Smart Deduplication**: Automatically removes duplicate URLs with "latest file wins" strategy
- **Source Tracking**: Each URL tracks its originating ZIP file for complete transparency
- **Consolidated Reporting**: Single comprehensive report combining all processed files
- **Backward Compatible**: Single file processing works exactly as before

## 🏗️ Architecture

This project demonstrates clean architecture and SOLID principles with a modular design:

```
gl_to_aem_url_converter/
├── core/                    # Business logic & domain models
│   ├── config.py           # Application configuration
│   ├── models.py           # Domain models (AEMLink, LinkCollection, ProcessingResult)
│   └── interfaces.py       # Abstract interfaces and protocols
├── services/               # Service implementations
│   ├── language.py         # Language detection and path management
│   ├── url_generator.py    # AEM URL generation logic
│   └── file_processor.py   # ZIP file processing
├── presentation/           # UI/presentation layer
│   ├── df_builder.py       # DataFrame construction
│   ├── html_renderer.py    # HTML report generation
│   └── template_loader.py  # Template management
├── docs/                   # Project documentation
├── Dockerfile              # Docker container configuration
├── docker-compose.yml     # Docker Compose setup
├── docker-run.sh          # Smart Docker runner script
├── di_container.py         # Dependency injection container
├── app.py                  # Streamlit application layer
├── main.py                 # Application entry point
└── requirements.txt        # Python dependencies
```

### SOLID Principles Applied

1. **SRP (Single Responsibility)**: Each class has one reason to change
   - `Config`: Only manages application settings
   - `AEMLink`: Only handles link data
   - `LanguageDetectorService`: Only detects languages
   - `AEMURLGenerator`: Only generates URLs

2. **OCP (Open/Closed)**: Open for extension, closed for modification
   - `URLGenerator` interface allows new URL generation strategies
   - `TemplateRenderer` interface supports different rendering engines
   - `FileProcessor` protocol enables new file processing methods

3. **LSP (Liskov Substitution)**: Implementations are interchangeable
   - All `URLGenerator` implementations work identically
   - Different `TemplateRenderer` implementations are substitutable

4. **ISP (Interface Segregation)**: Clients depend only on what they need
   - `LanguageDetector`, `DataFrameBuilder` protocols are focused
   - No client depends on unused interface methods

5. **DIP (Dependency Inversion)**: Depend on abstractions, not concretions
   - `DIContainer` manages all dependencies centrally
   - High-level modules don't depend on low-level modules
   - All dependencies flow through abstract interfaces

## 🚀 Quick Start

### Prerequisites

- **Docker**: Install Docker Desktop for your platform
- **WSL2** (Windows users): Ensure WSL2 is enabled

### Installation & Setup

```bash
# Clone the repository
git clone <repository-url>
cd gl_to_aem_url_converter

# One-time setup: Install global Docker command
./install-docker-global.sh

# Restart terminal or reload shell
source ~/.bashrc
```

### Running the Application

#### **🎯 Recommended Method (Global Command):**
```bash
# From anywhere in your system:
cd /any/directory
aem-docker                    # Run on solid branch (latest features)
aem-docker main              # Run on main branch (stable)
aem-docker feature/my-branch # Run on any branch
```

#### **🔧 Alternative Methods:**
```bash
# From project directory:
./docker-run.sh              # Run on solid branch
./docker-run.sh main         # Run on main branch

# Using Docker Compose:
docker-compose up --build

# Manual Docker run:
docker run -p 8501:8501 gl_to_aem_url:latest
```

#### **🌐 Accessing the Application:**

The application will be available at:
- **Windows Browser**: `http://localhost:8501` ⭐ (Most common)
- **WSL Browser**: `http://127.0.0.1:8501`
- **Alternative**: `http://[WSL-IP]:8501` (shown in output)

> **💡 Tip**: If you get "ERR_CONNECTION_REFUSED", try the different URLs above. See [DOCKER_TROUBLESHOOTING.md](DOCKER_TROUBLESHOOTING.md) for solutions.

### Environment Variables (Optional)

```bash
# Customize AEM host
export AEM_HOST="https://your-aem-host.com"
export SOURCE_LANG="en"
export TEMPLATE_FILE="custom_template.html"

# Then run normally
aem-docker
```

## 📚 Usage

### Basic Usage

#### Single File Processing (Original Workflow)
1. **Launch Application**: Run `aem-docker`
2. **Upload GlobalLink ZIP**: Upload a single downloaded GlobalLink translation ZIP file
3. **Optional Metadata**: Enter Job ID and Submission Name for tracking
4. **View MSM Review Links**: Browse results in organized tabs
5. **Download Report**: Export HTML report for the single file

#### 🆕 Multi-ZIP Batch Processing (New Feature)
1. **Launch Application**: Run `aem-docker`
2. **Upload Multiple ZIPs**:
   - Use Ctrl+Click (Windows/Linux) or Cmd+Click (Mac) to select multiple ZIP files
   - Upload all selected files at once
3. **Batch Processing**:
   - Application processes all files automatically
   - Smart deduplication removes duplicate URLs
   - "Latest file wins" for conflicts
4. **View Consolidated Results**:
   - **Summary Tab**: Combined statistics across all files
   - **Japanese Tab**: Merged Japanese content with source tracking
   - **Korean Tab**: Merged Korean content with source tracking
   - **Source Column**: Shows which ZIP file each URL originated from
5. **Download Comprehensive Report**:
   - Single HTML report combining all files
   - Source file information included
   - Complete audit trail of processed files

### MSM Review Interface
- **Summary Tab**: Overview with statistics and translation coverage
- **Japanese Tab**: AEM editor links for Japanese content review
- **Korean Tab**: AEM editor links for Korean content review
- **Source Tracking**: When multiple files are processed, see which ZIP each URL came from

### Download Options
Export HTML reports with:
- Interactive checkboxes for content selection
- Quick Links for MSM workflow:
  - **Language Master (English)**: Source content links
  - **Target Language**: Translated content for review
  - **SPAC Target Language**: SPAC-specific content links
- Hierarchical table structure for easy navigation
- **Source Information**: ZIP file tracking when processing multiple files

### MSM Workflow Features
- **Multi-Site Manager Integration**: Direct links to AEM MSM content structure
- **Language Master Access**: Quick access to English source content
- **Target Language Review**: Direct editing links for translated content
- **SPAC Integration**: Specialized links for SPAC target language content
- **Content Hierarchy**: Organized view matching AEM content structure
- **Translation Tracking**: Job ID and submission tracking for workflow management

## 📦 Multi-ZIP Feature Details

### Smart Deduplication
- **Path-Based Detection**: URLs with identical paths are considered duplicates
- **Latest File Priority**: When conflicts occur, the version from the later-processed file is kept
- **Transparent Reporting**: Deduplication statistics shown in application warnings
- **Source Preservation**: Winning URLs retain their source ZIP information

### Source File Tracking
- **Granular Attribution**: Each URL knows which ZIP file it originated from
- **Visual Indicators**: Source column automatically appears for multi-file processing
- **Report Integration**: HTML reports include source file information
- **Audit Trail**: Complete visibility into which files contributed which content

### Batch Processing Benefits
- **Time Efficiency**: Process multiple translation deliveries simultaneously
- **Consistency**: Single consolidated view of all translated content
- **Quality Assurance**: Automatic duplicate detection prevents review redundancy
- **Workflow Integration**: Streamlined handoff to MSM review process

### Technical Implementation
- **Memory Efficient**: Files processed sequentially, not loaded simultaneously
- **Error Isolation**: Problems in one ZIP don't affect others
- **Progress Feedback**: Real-time updates during batch processing
- **Backward Compatible**: Zero impact on existing single-file workflows

## 🐳 Docker Benefits

### **🌍 True Portability**
- ✅ **Run from anywhere**: Works from any directory in WSL/Linux
- ✅ **No local setup**: No Python, virtual environments, or dependencies needed
- ✅ **Consistent environment**: Same behavior across all machines
- ✅ **Clean isolation**: No conflicts with other Python projects

### **🚀 Performance & Reliability**
- ✅ **Fast startup**: Optimized Docker image with minimal dependencies
- ✅ **Layer caching**: Subsequent builds are extremely fast
- ✅ **Health checks**: Built-in container monitoring
- ✅ **Automatic cleanup**: Easy to reset and restart

### **🔧 Development Experience**
- ✅ **Branch management**: Automatic git branch switching
- ✅ **Volume mounting**: Live development with file changes
- ✅ **Multiple environments**: Easy testing across different branches
- ✅ **Production ready**: Same container can deploy anywhere

## 🔧 Customization

### Adding New Languages

The refactored architecture makes adding new languages straightforward:

1. **Update language configuration in `core/config.py`**:
```python
# In Config.__post_init__ method
self.language_mapping = {
    'ko-KR': 'ko',
    'ja-JP': 'ja',
    'zh-CN': 'zh',  # New language
    'fr-FR': 'fr'   # Another new language
}

self.spac_paths = {
    'ko': '/spac/ko_KR/',
    'ja': '/spac/ja_JP/',
    'zh': '/spac/zh_CN/',  # New SPAC path
    'fr': '/spac/fr_FR/'   # Another new SPAC path
}
```

2. **Language detection is automatic** - `LanguageDetectorService` will automatically detect the new languages based on the configuration

3. **URL generation will work automatically** - `AEMURLGenerator` uses the configuration dynamically

4. **UI updates are handled automatically** - The application will create new tabs and sections for the new languages

## 🐛 Troubleshooting

### Connection Issues
If you encounter "ERR_CONNECTION_REFUSED":

1. **Try different URLs**:
   - `http://localhost:8501` (Windows browser)
   - `http://127.0.0.1:8501` (WSL browser)
   - `http://[WSL-IP]:8501` (alternative)

2. **Check container status**:
   ```bash
   docker ps  # Should show container as "Up" and "(healthy)"
   ```

3. **Test connection**:
   ```bash
   curl http://localhost:8501  # Should return HTML
   ```

4. **Use alternative port**:
   ```bash
   aem-docker --port 8502
   ```

See [DOCKER_TROUBLESHOOTING.md](DOCKER_TROUBLESHOOTING.md) for comprehensive troubleshooting guide.

### Docker Issues
```bash
# Rebuild image if needed
aem-docker --rebuild

# Check Docker status
docker info

# View container logs
docker logs gl-to-aem-url
```

## 🔍 Architecture Benefits

### 🚀 Performance
- **Docker Optimization**: Minimal image size with only essential dependencies
- **Layer Caching**: Fast subsequent builds and deployments
- **Memory Efficiency**: Optimized file processing with minimal memory usage

### 🛡️ Reliability
- **Container Isolation**: No host system conflicts or dependencies
- **Health Monitoring**: Built-in container health checks
- **Error Handling**: Structured error reporting with `ProcessingResult`

### 🔧 Maintainability
- **Clean Architecture**: Clear separation of concerns across layers
- **SOLID Principles**: Makes code easy to understand and modify
- **Dependency Injection**: Facilitates testing and reduces coupling

### 📈 Extensibility
- **Plugin Architecture**: Easy to add new URL generators or renderers
- **Language Support**: Simple configuration-based language addition
- **Template System**: Flexible HTML template customization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Sijung Kim - Initial work and SOLID refactoring

## 🙏 Acknowledgments

- **Docker**: Modern containerization platform
- **Streamlit**: Modern web framework for Python applications
- **pandas**: Powerful data manipulation and analysis library
- **GlobalLink**: Translation management system integration
- **SOLID Principles**: Robert C. Martin's software design principles
- **Clean Architecture**: Architectural pattern for maintainable software