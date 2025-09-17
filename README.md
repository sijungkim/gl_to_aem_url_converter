---
title: "AEM URL Converter"
description: "A Streamlit-based tool for processing GlobalLink translated ZIP files and generating AEM editor URLs for MSM (Multi-Site Manager) content review and updates across English, target languages, and SPAC target languages"
architect: "Sijung Kim"
authors: ["Sijung Kim", "Claude", "Gemini"]
reviewed_by: "Sijung Kim"
created_date: "2025-09-15"
last_modified: "2025-09-17"
version: "2.0.0"
license: "MIT"
tags: ["AEM", "GlobalLink", "Translation", "SOLID", "Clean Architecture", "Streamlit"]
---

# AEM URL Converter

A Streamlit-based tool for processing GlobalLink translated ZIP files and generating AEM editor URLs for MSM (Multi-Site Manager) content review and updates. The application analyzes downloaded GlobalLink translation packages and provides direct AEM editor links for English language master, target language content, and SPAC target language pages, streamlining the multilingual content management workflow.

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
│   ├── AEM URL Converter - 프로젝트 구조.md
│   ├── AEM URL 변환기 컴포넌트 다이어그램.md
│   ├── AEM URL 변환기 시퀀스 다이어그램.md
│   └── AEM URL 변환기 순서도.md
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

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/aem-url-converter.git
cd aem-url-converter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Run with Streamlit
streamlit run main.py

# Or run directly
python -m streamlit run main.py
```

### Environment Variables (Optional)

```bash
export AEM_HOST="https://your-aem-host.com"
export SOURCE_LANG="en"
export TEMPLATE_FILE="custom_template.html"
```

## 📦 Project Structure

### Core Package (`core/`) - Domain Layer
- **`config.py`**: Application configuration management
  - `Config` dataclass with environment variable support
  - Language mappings and SPAC path configurations
  - Type-safe configuration properties

- **`models.py`**: Domain models and business entities
  - `AEMLink`: Represents an AEM editor link with path utilities
  - `LinkCollection`: Language-specific link collections
  - `ProcessingResult`: Encapsulates processing outcomes with error handling

- **`interfaces.py`**: Abstract interfaces and protocols
  - `URLGenerator`: Abstract base for URL generation strategies
  - `FileProcessor`: Protocol for file processing implementations
  - `TemplateRenderer`: Interface for different rendering engines
  - `LanguageDetector`: Protocol for language detection services

### Services Package (`services/`) - Business Logic Layer
- **`language.py`**: Language detection and path management
  - `LanguageDetectorService`: Detects languages from file paths
  - `LanguagePathManager`: Manages language-specific path configurations

- **`url_generator.py`**: AEM URL generation and validation
  - `AEMURLGenerator`: Generates AEM editor URLs following URL conventions
  - `URLValidator`: Validates generated URLs for correctness

- **`file_processor.py`**: ZIP file processing services
  - `ZipFileProcessor`: Main ZIP file processing logic
  - `FileFilter`: Filters relevant files from ZIP archives
  - `BatchProcessor`: Handles batch processing operations

### Presentation Package (`presentation/`) - Presentation Layer
- **`df_builder.py`**: DataFrame construction utilities
  - `HierarchicalDataFrameBuilder`: Creates hierarchical table structures
  - `SummaryDataFrameBuilder`: Builds summary information tables

- **`html_renderer.py`**: HTML report generation
  - `HTMLTableRenderer`: Renders HTML tables with advanced features
  - `QuickLinksGenerator`: Generates quick access links (lm-en, lm-ko/ja, spac)

- **`template_loader.py`**: Template management system
  - `TemplateLoader`: Basic template loading functionality
  - `AdvancedTemplateLoader`: Advanced template management with directory support

### Documentation (`docs/`)
- **Project Structure**: Detailed architecture documentation
- **Component Diagram**: Mermaid class diagrams showing relationships
- **Sequence Diagram**: Processing flow visualization
- **Flowchart**: Step-by-step process documentation

### Application Layer
- **`di_container.py`**: Dependency injection container
  - `DIContainer`: Main dependency injection container with singleton pattern
  - `TestDIContainer`: Testing-specific container with mock injection support

- **`app.py`**: Streamlit application interface
  - `AEMConverterApp`: Main application class handling UI interactions
  - Clean separation between business logic and presentation

- **`main.py`**: Application entry point
  - Configuration loading from environment variables
  - Dependency injection setup
  - Application initialization and execution

## 🧪 Testing

The refactored architecture supports comprehensive testing:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test modules
pytest tests/test_language.py
pytest tests/test_url_generator.py
pytest tests/test_file_processor.py

# Test with different environments
AEM_HOST=https://test.example.com pytest
```

### Testing Architecture

```python
# Example: Testing with dependency injection
from di_container import TestDIContainer
from unittest.mock import Mock

def test_zip_processing():
    # Create test container
    container = TestDIContainer()

    # Inject mock dependencies
    mock_url_generator = Mock()
    container.inject_mock('url_generator', mock_url_generator)

    # Test with injected mocks
    processor = container.zip_processor
    # ... test implementation
```

### Testable Components
- **Unit Tests**: Each service can be tested independently
- **Integration Tests**: Test service interactions through DI container
- **Mock Injection**: `TestDIContainer` supports easy mock object injection
- **Configuration Testing**: Different configurations can be tested easily

## 📚 Usage

### Basic Usage
1. **Launch Application**: Run `streamlit run main.py` or `python main.py`
2. **Upload GlobalLink ZIP**: Upload the downloaded GlobalLink translation ZIP file
3. **Optional Metadata**: Enter Job ID and Submission Name for tracking
4. **View MSM Review Links**:
   - **Summary Tab**: Overview with statistics and translation coverage
   - **Japanese Tab**: AEM editor links for Japanese content review
   - **Korean Tab**: AEM editor links for Korean content review
5. **Download MSM Reports**: Export HTML reports with:
   - Interactive checkboxes for content selection
   - Quick Links for MSM workflow:
     - **Language Master (English)**: Source content links
     - **Target Language**: Translated content for review
     - **SPAC Target Language**: SPAC-specific content links
   - Hierarchical table structure for easy navigation

### MSM Workflow Features
- **Multi-Site Manager Integration**: Direct links to AEM MSM content structure
- **Language Master Access**: Quick access to English source content
- **Target Language Review**: Direct editing links for translated content
- **SPAC Integration**: Specialized links for SPAC target language content
- **Content Hierarchy**: Organized view matching AEM content structure
- **Translation Tracking**: Job ID and submission tracking for workflow management

### GlobalLink to AEM Processing Flow
1. **Download ZIP from GlobalLink** → **Upload to Application** → **Content Analysis**
2. **Language Detection** → **MSM Structure Mapping** → **AEM URL Generation**
3. **Review Link Generation** → **Report Creation** → **MSM Workflow Support**

## 🔧 Customization

### Custom Templates

Create a `template.html` file in the project root:

```html
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <!-- Your custom styles -->
</head>
<body>
    <h1>{title}</h1>
    <div class="source-info">{source_info}</div>
    <table>
        <thead><tr>{headers}</tr></thead>
        <tbody>{table_rows}</tbody>
    </table>
</body>
</html>
```

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

### Benefits of the Refactored Architecture
- **Type Safety**: Strong typing prevents runtime errors
- **Dependency Injection**: Easy testing and mock object injection
- **Separation of Concerns**: Clear boundaries between layers
- **Extensibility**: Easy to add new features without modifying existing code
- **Maintainability**: Changes in one layer don't affect others

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔍 Architecture Benefits

### 🚀 Performance
- **Lazy Loading**: Services are instantiated only when needed
- **Singleton Pattern**: Prevents duplicate service creation
- **Efficient Processing**: Optimized file processing with minimal memory usage

### 🛡️ Reliability
- **Type Safety**: Comprehensive type hints prevent runtime errors
- **Error Handling**: Structured error reporting with `ProcessingResult`
- **Validation**: URL and file validation at multiple layers

### 🔧 Maintainability
- **Clean Architecture**: Clear separation of concerns across layers
- **SOLID Principles**: Makes code easy to understand and modify
- **Dependency Injection**: Facilitates testing and reduces coupling

### 📈 Extensibility
- **Plugin Architecture**: Easy to add new URL generators or renderers
- **Language Support**: Simple configuration-based language addition
- **Template System**: Flexible HTML template customization

## 👥 Authors

- Sijung Kim - Initial work and SOLID refactoring

## 🙏 Acknowledgments

- **Streamlit**: Modern web framework for Python applications
- **pandas**: Powerful data manipulation and analysis library
- **GlobalLink**: Translation management system integration
- **SOLID Principles**: Robert C. Martin's software design principles
- **Clean Architecture**: Architectural pattern for maintainable software