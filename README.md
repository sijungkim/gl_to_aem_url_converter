# AEM URL Converter

A Streamlit-based tool for converting GlobalLink translation files to AEM editor URLs, following SOLID principles and clean architecture.

## 🏗️ Architecture

This project demonstrates clean architecture and SOLID principles:

```
aem_url_converter/
├── core/               # Business logic & domain models
├── services/          # Service implementations
├── presentation/      # UI/presentation layer
├── di_container.py    # Dependency injection
├── app.py            # Streamlit application
└── main.py           # Entry point
```

### SOLID Principles Applied

1. **SRP (Single Responsibility)**: Each class has one reason to change
2. **OCP (Open/Closed)**: Open for extension, closed for modification
3. **LSP (Liskov Substitution)**: Implementations are interchangeable
4. **ISP (Interface Segregation)**: Clients depend only on what they need
5. **DIP (Dependency Inversion)**: Depend on abstractions, not concretions

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

### Core Package (`core/`)
- `config.py`: Application configuration
- `models.py`: Domain models (AEMLink, LinkCollection)
- `interfaces.py`: Abstract interfaces and protocols

### Services Package (`services/`)
- `language.py`: Language detection and path management
- `url_generator.py`: AEM URL generation logic
- `file_processor.py`: ZIP file processing

### Presentation Package (`presentation/`)
- `df_builder.py`: DataFrame construction
- `html_renderer.py`: HTML report generation
- `template_loader.py`: Template management

### Dependency Injection
- `di_container.py`: Centralized dependency management

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_language.py
```

## 📚 Usage

1. **Upload ZIP File**: Upload the GlobalLink translation ZIP file
2. **Optional Metadata**: Enter Job ID and Submission Name
3. **View Results**: See extracted URLs in hierarchical tables
4. **Download Report**: Export HTML report for reference

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

1. Update `Config.language_mapping`:
```python
language_mapping = {
    'ko-KR': 'ko',
    'ja-JP': 'ja',
    'zh-CN': 'zh'  # New language
}
```

2. Add SPAC path:
```python
spac_paths = {
    'ko': '/spac/ko_KR/',
    'ja': '/spac/ja_JP/',
    'zh': '/spac/zh_CN/'  # New path
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Sijung Kim - Initial work

## 🙏 Acknowledgments

- Streamlit for the web framework
- pandas for data manipulation
- GlobalLink for translation management