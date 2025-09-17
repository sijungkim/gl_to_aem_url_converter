"""
__init__.py 파일들 - 패키지 초기화
"""

# ========================================
# core/__init__.py
# ========================================
"""
Core 패키지 - 핵심 비즈니스 로직과 도메인 모델
"""
from .config import Config
from .models import AEMLink, LinkCollection, ProcessingResult
from .interfaces import (
    URLGenerator,
    FileProcessor,
    TemplateRenderer,
    LanguageDetector,
    DataFrameBuilder
)

__all__ = [
    # Config
    'Config',
    
    # Models
    'AEMLink',
    'LinkCollection',
    'ProcessingResult',
    
    # Interfaces
    'URLGenerator',
    'FileProcessor',
    'TemplateRenderer',
    'LanguageDetector',
    'DataFrameBuilder'
]

# ========================================
# services/__init__.py
# ========================================
"""
Services 패키지 - 비즈니스 로직 구현
"""
from .language import LanguageDetectorService, LanguagePathManager
from .url_generator import AEMURLGenerator, URLValidator
from .file_processor import ZipFileProcessor, FileFilter, BatchProcessor

__all__ = [
    # Language services
    'LanguageDetectorService',
    'LanguagePathManager',
    
    # URL services
    'AEMURLGenerator',
    'URLValidator',
    
    # File processing services
    'ZipFileProcessor',
    'FileFilter',
    'BatchProcessor'
]

# ========================================
# presentation/__init__.py
# ========================================
"""
Presentation 패키지 - 표현 계층 (UI/출력 관련)
"""
from .df_builder import HierarchicalDataFrameBuilder, SummaryDataFrameBuilder
from .html_renderer import QuickLinksGenerator, HTMLTableRenderer
from .template_loader import TemplateLoader, AdvancedTemplateLoader

__all__ = [
    # DataFrame builders
    'HierarchicalDataFrameBuilder',
    'SummaryDataFrameBuilder',
    
    # HTML rendering
    'QuickLinksGenerator',
    'HTMLTableRenderer',
    
    # Template loading
    'TemplateLoader',
    'AdvancedTemplateLoader'
]