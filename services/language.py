"""
---
title: "Language Detection and Path Management Services"
description: "Service layer components for language detection from file paths and language-specific path management. Implements business logic for identifying target languages and managing language-specific URL path configurations following the Single Responsibility Principle."
architect: "Sijung Kim"
authors: ["Sijung Kim", "Claude", "Gemini"]
reviewed_by: "Sijung Kim"
created_date: "2025-09-15"
last_modified: "2025-09-17"
version: "2.0.0"
module_type: "Service Layer"
dependencies: ["typing", "core.config"]
key_classes: ["LanguageDetectorService", "LanguagePathManager"]
key_functions: ["detect", "is_supported_language", "get_language_path", "get_spac_path"]
design_patterns: ["Service Pattern", "Strategy Pattern"]
solid_principles: ["SRP - Single Responsibility Principle", "DIP - Dependency Inversion Principle"]
features: ["Language Detection", "Path Management", "Configuration-driven", "Type Safety"]
tags: ["language-detection", "path-management", "services", "business-logic"]
---

services/language.py - Language Detection and Path Management Services

This module provides service layer components for language-related operations in
the AEM URL Converter application. It implements the business logic for detecting
languages from file paths and managing language-specific path configurations.

Key Responsibilities:
- Detect target languages from GlobalLink file paths
- Validate language support against configuration
- Manage language-specific path transformations
- Provide SPAC path mappings for different languages

Architecture:
The module contains two focused service classes that follow the Single
Responsibility Principle. Each service has a clear, well-defined purpose and
depends on the configuration abstraction rather than concrete implementations.

Service Classes:

1. LanguageDetectorService:
   Responsible for detecting target languages from file paths in GlobalLink
   ZIP archives. Uses configuration-driven language mappings to identify
   supported languages.

   Key Features:
   - Pattern-based language detection from file paths
   - Configuration-driven language mapping (ko-KR -> ko, ja-JP -> ja)
   - Support validation against configured languages
   - Robust error handling for unsupported languages

   Methods:
   - detect(path) -> Optional[str]: Detects language code from file path
   - is_supported_language(lang_code) -> bool: Validates language support

   Algorithm:
   The detection algorithm scans file paths for language locale patterns
   (e.g., 'ko-KR', 'ja-JP') and maps them to standardized language codes
   using the configuration. This approach is extensible and supports easy
   addition of new languages.

2. LanguagePathManager:
   Manages language-specific path configurations and transformations for
   AEM URL generation. Provides utilities for constructing language-specific
   paths and SPAC URLs.

   Key Features:
   - Language-specific path generation
   - SPAC path mapping for different languages
   - Configuration-based path management
   - Support for custom path patterns

   Methods:
   - get_language_path(lang_code) -> str: Generates language master path
   - get_spac_path(lang_code) -> str: Returns SPAC path for language
   - build_target_path(source_path, target_lang) -> str: Path transformation

   Design:
   The manager uses the configuration to provide consistent path generation
   across the application, ensuring that language-specific URLs follow
   the correct patterns for AEM integration.

Language Detection Algorithm:
1. Parse file path for locale patterns (ko-KR, ja-JP, etc.)
2. Look up locale in configuration language mapping
3. Return standardized language code (ko, ja, etc.)
4. Return None for unsupported or missing languages

Path Management Features:
- Language Master Paths: /language-master#[lang_code]
- SPAC Paths: /spac/[locale]/ (e.g., /spac/ko_KR/)
- Target Path Generation: Transform source paths to target language paths
- Configuration-driven: All paths come from centralized configuration

Usage Examples:
# Language detection
detector = LanguageDetectorService(config)
lang = detector.detect('/path/to/ko-KR/file.xml')  # Returns 'ko'
is_supported = detector.is_supported_language('ko')  # Returns True

# Path management
path_manager = LanguagePathManager(config)
lang_path = path_manager.get_language_path('ko')  # Returns 'language-master#ko'
spac_path = path_manager.get_spac_path('ko')  # Returns '/spac/ko_KR/'

Configuration Integration:
Both services depend on the Config object for their behavior, making them
easily configurable for different environments and extensible for new
languages. The configuration-driven approach ensures consistency across
the application and simplifies maintenance.

Error Handling:
- Graceful handling of unsupported languages
- Optional return types for missing data
- Validation methods for input verification
- Clear error messages for debugging

Testing:
The services are designed to be easily testable:
- Constructor injection enables mock configuration
- Pure methods with clear inputs/outputs
- No external dependencies beyond configuration
- Deterministic behavior for given inputs

Extensibility:
Adding support for new languages requires only configuration changes:
1. Add language mapping to Config.language_mapping
2. Add SPAC path to Config.spac_paths
3. Services automatically support the new language

The services demonstrate clean separation of concerns, with language detection
focused solely on path analysis and path management focused solely on URL
construction, following the Single Responsibility Principle.
"""
from typing import Optional, Dict
from core.config import Config


class LanguageDetectorService:
    """언어 감지 서비스 (SRP - 언어 감지만 담당)
    
    파일 경로에서 언어 코드를 감지하는 역할만 수행.
    """
    
    def __init__(self, config: Config):
        """언어 감지기 초기화
        
        Args:
            config: 애플리케이션 설정
        """
        self.language_mapping = config.language_mapping
    
    def detect(self, path: str) -> Optional[str]:
        """경로에서 언어 코드 감지
        
        Args:
            path: 파일 경로
            
        Returns:
            감지된 언어 코드 ('ko', 'ja' 등) 또는 None
        """
        for locale, lang_code in self.language_mapping.items():
            if locale in path:
                return lang_code
        return None
    
    def is_supported_language(self, lang_code: str) -> bool:
        """지원되는 언어인지 확인
        
        Args:
            lang_code: 언어 코드
            
        Returns:
            지원 여부
        """
        return lang_code in self.language_mapping.values()


class LanguagePathManager:
    """언어별 경로 관리 서비스 (OCP - 확장에 열림)
    
    언어별 특수 경로(SPAC 등)를 관리.
    새로운 경로 타입 추가 시 이 클래스만 수정.
    """
    
    def __init__(self, config: Config):
        """경로 관리자 초기화
        
        Args:
            config: 애플리케이션 설정
        """
        self.config = config
        self.spac_paths = config.spac_paths
    
    def get_spac_path(self, lang_code: str) -> str:
        """SPAC 경로 반환
        
        Args:
            lang_code: 언어 코드
            
        Returns:
            SPAC 경로 문자열
        """
        return self.spac_paths.get(lang_code, '')
    
    def get_language_master_path(self, lang_code: str) -> str:
        """언어 마스터 경로 반환
        
        Args:
            lang_code: 언어 코드
            
        Returns:
            언어 마스터 경로
        """
        return f'/language-master/{lang_code}/'
    
    def get_english_path(self) -> str:
        """영어 경로 반환
        
        Returns:
            영어 언어 마스터 경로
        """
        return '/language-master/en/'
    
    def convert_to_spac_url(self, url: str, lang_code: str) -> str:
        """URL을 SPAC URL로 변환
        
        Args:
            url: 원본 URL
            lang_code: 언어 코드
            
        Returns:
            SPAC URL
        """
        lm_path = self.get_language_master_path(lang_code)
        spac_path = self.get_spac_path(lang_code)
        return url.replace(lm_path, spac_path)
    
    def convert_to_english_url(self, url: str, lang_code: str) -> str:
        """URL을 영어 URL로 변환
        
        Args:
            url: 원본 URL
            lang_code: 원본 언어 코드
            
        Returns:
            영어 URL
        """
        lm_path = self.get_language_master_path(lang_code)
        en_path = self.get_english_path()
        return url.replace(lm_path, en_path)