---
title: "AEM URL Converter (Main Branch)"
description: "A Streamlit-based tool for processing GlobalLink translated ZIP files and generating AEM editor URLs for MSM (Multi-Site Manager) content review and updates across English, target languages, and SPAC target languages. Monolithic implementation."
architect: "Sijung Kim"
authors: ["Sijung Kim", "Claude", "Gemini"]
reviewed_by: "Sijung Kim"
created_date: "2025-09-15"
last_modified: "2025-09-17"
version: "1.0.0"
license: "MIT"
branch: "main"
architecture: "Monolithic"
tags: ["AEM", "GlobalLink", "Translation", "MSM", "Streamlit", "Production"]
---

# AEM URL Converter

A Streamlit-based tool for processing GlobalLink translated ZIP files and generating AEM editor URLs for MSM (Multi-Site Manager) content review and updates. This main branch contains the production-ready monolithic implementation.

## 🏗️ Architecture

This main branch uses a **monolithic architecture** with all functionality contained in a single file:

```
gl_to_aem_url_converter/ (main branch)
├── aem_url_converter.py         # Main monolithic application
├── html_template_file.html      # HTML template
├── docs/                        # Documentation files
│   ├── AEM URL 변환기 컴포넌트 다이어그램.md
│   ├── AEM URL 변환기 시퀀스 다이어그램.md
│   └── AEM URL 변환기 순서도.md
└── .gitignore                   # Git exclusion rules
```

### Monolithic Design Benefits
- **Simplicity**: Single file deployment and execution
- **Easy Debugging**: All code in one place for troubleshooting
- **Quick Deployment**: No complex dependency management
- **Production Stability**: Battle-tested monolithic approach

> **Note**: For a refactored SOLID-principles implementation, see the `solid` branch.

## 🚀 Quick Start

### Installation
```bash
# Clone and switch to main branch
git clone https://github.com/sijungkim/gl_to_aem_url_converter.git
cd gl_to_aem_url_converter
git checkout main

# Install dependencies
pip install streamlit pandas

# Run the application
streamlit run aem_url_converter.py
```

### Environment Variables (Optional)
```bash
export AEM_HOST="https://your-aem-host.com"  # Default: https://prod-author.illumina.com
```

## 📦 Core Functions

The monolithic `aem_url_converter.py` contains all essential functions:

### **Configuration Section**
```python
AEM_HOST = "https://prod-author.illumina.com"
SOURCE_LANG_PATH = "language-master#en"
TEMPLATE_FILE = "template.html"
```

### **Core Functions**
- **`load_template()`**: Loads HTML template or provides default
- **`generate_aem_url(file_name, target_lang)`**: Generates AEM editor URLs
- **`process_zip_file(uploaded_file)`**: Processes GlobalLink ZIP archives
- **`build_hierarchical_df(links)`**: Creates hierarchical DataFrames
- **`generate_html_table(...)`**: Generates downloadable HTML reports

### **Streamlit UI Section**
- File upload interface
- Real-time processing with progress indicators
- Split-view results (Korean/Japanese)
- HTML report generation and download

## 📚 Usage

### Basic Workflow
1. **Launch Application**: `streamlit run aem_url_converter.py`
2. **Upload GlobalLink ZIP**: Upload the downloaded GlobalLink translation ZIP file
3. **Optional Metadata**: Enter Job ID and Submission Name for tracking
4. **View MSM Review Links**:
   - **Japanese Section**: AEM editor links for Japanese content review
   - **Korean Section**: AEM editor links for Korean content review
5. **Download MSM Reports**: Export HTML reports with:
   - Interactive checkboxes for content selection
   - Quick Links for MSM workflow:
     - **lm-en**: English language master links
     - **lm-ko/ja**: Target language content links
     - **spac-ko/ja**: SPAC target language links
   - Hierarchical table structure for easy navigation

### MSM Integration Features
- **Multi-Site Manager Support**: Direct links to AEM MSM content structure
- **Language Master Access**: Quick access to English source content
- **Target Language Review**: Direct editing links for translated content
- **SPAC Integration**: Specialized links for SPAC target language content
- **Content Hierarchy**: Organized view matching AEM content structure

### GlobalLink Processing Algorithm
1. **ZIP Analysis**: Extract and analyze GlobalLink translation package
2. **Language Detection**: Identify ko-KR and ja-JP language files
3. **Content Filtering**: Process only files starting with "#content"
4. **URL Generation**: Transform paths to AEM editor URLs
5. **MSM Link Creation**: Generate language master, target, and SPAC links
6. **Report Generation**: Create downloadable HTML reports

## 🔧 Customization

### Custom HTML Templates
Create a `template.html` file in the project root for custom styling:

```html
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>/* Custom styles */</style>
</head>
<body>
    <h1>{title}</h1>
    <div>{source_info}</div>
    <table>
        <thead><tr>{headers}</tr></thead>
        <tbody>{table_rows}</tbody>
    </table>
</body>
</html>
```

### Configuration Modifications
Edit the configuration section in `aem_url_converter.py`:
```python
# Modify these constants for your environment
AEM_HOST = "https://your-aem-host.com"
SOURCE_LANG_PATH = "language-master#en"
TEMPLATE_FILE = "template.html"  # Note: actual file is html_template_file.html
```

## 🔍 Function Details

### Language Processing
- **Supported Languages**: Korean (ko-KR → ko), Japanese (ja-JP → ja)
- **Path Detection**: Automatic language detection from file paths
- **Content Filtering**: Processes only "#content" prefixed files

### URL Generation Logic
1. **Source Path Analysis**: `language-master#en` → `language-master#ko/ja`
2. **Path Transformation**: Remove `#`, convert `.xml` to `.html`
3. **Editor URL Construction**: `{AEM_HOST}/editor.html/{aem_path}`
4. **Quick Links Generation**:
   - English: `/language-master/en/`
   - Target: `/language-master/{lang}/`
   - SPAC: `/spac/{lang}_*/`

## 🏭 Production Features

### Stability & Performance
- **Battle-tested**: Production-ready monolithic implementation
- **Error Handling**: Comprehensive error handling throughout
- **Memory Efficient**: Processes ZIP files in memory without extraction
- **Fast Processing**: Optimized for large GlobalLink packages

### User Experience
- **Progress Indicators**: Real-time processing feedback
- **Split View**: Side-by-side Korean/Japanese results
- **Interactive Tables**: Clickable links and hierarchical organization
- **Download Reports**: Professional HTML reports with MSM navigation

### Enterprise Ready
- **AEM Integration**: Direct integration with Adobe Experience Manager
- **MSM Workflow**: Supports Multi-Site Manager content workflows
- **Translation Management**: GlobalLink TMS integration
- **SPAC Support**: Specialized SPAC content handling

## 🔗 Branch Information

- **Current Branch**: `main`
- **Architecture**: Monolithic (single file)
- **Stability**: Production-ready
- **Alternative**: `solid` branch (refactored SOLID principles)

This main branch represents the stable, production-ready monolithic implementation optimized for simplicity and reliability in enterprise environments.