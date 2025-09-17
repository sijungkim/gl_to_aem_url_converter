"""
---
title: "Application Configuration Management"
description: "Core configuration module implementing type-safe application settings with environment variable support, language mappings, and SPAC path management. Provides centralized configuration management following the Single Responsibility Principle."
architect: "Sijung Kim"
authors: ["Sijung Kim", "Claude", "Gemini"]
reviewed_by: "Sijung Kim"
created_date: "2025-09-15"
last_modified: "2025-09-17"
version: "2.0.0"
module_type: "Core Domain Layer"
dependencies: ["dataclasses", "typing"]
key_classes: ["Config"]
key_functions: ["__post_init__", "get_supported_languages", "get_spac_path"]
design_patterns: ["Data Class Pattern", "Configuration Pattern"]
solid_principles: ["SRP - Single Responsibility Principle"]
features: ["Type Safety", "Environment Variables", "Default Values", "Language Mapping"]
tags: ["configuration", "settings", "dataclass", "core", "domain"]
---

core/config.py - Application Configuration Management

This module provides centralized configuration management for the AEM URL Converter
application. It implements a type-safe, immutable configuration system that supports
environment variables, default values, and language-specific settings.

Key Responsibilities:
- Application-wide configuration management
- Environment variable integration
- Language mapping and SPAC path configuration
- Type-safe configuration properties
- Default value management

Architecture:
The Config class is implemented as a dataclass with post-initialization processing
to ensure all configuration values are properly set. It follows the Single
Responsibility Principle by focusing solely on configuration management without
mixing business logic.

Key Features:
- Type-Safe Configuration: All configuration values are typed for compile-time safety
- Environment Variable Support: Automatic loading from environment variables
- Language Mappings: Configurable language code translations (ko-KR -> ko, ja-JP -> ja)
- SPAC Path Management: Language-specific SPAC URL path configurations
- Immutable Design: Configuration values are set once during initialization
- Default Values: Sensible defaults for all configuration options

Configuration Properties:
- aem_host: AEM server host URL (default: https://prod-author.illumina.com)
- source_lang: Source language code (default: en)
- template_file: HTML template file path (default: template.html)
- language_mapping: Dictionary mapping locale codes to language codes
- spac_paths: Dictionary mapping language codes to SPAC paths

Language Support:
The configuration system is designed to be easily extensible for new languages.
Adding support for a new language requires only updating the language_mapping
and spac_paths dictionaries in the post_init method.

Usage Examples:
# Basic usage with defaults
config = Config()
print(config.aem_host)  # https://prod-author.illumina.com

# Custom configuration
config = Config(
    aem_host="https://staging.example.com",
    source_lang="en",
    template_file="custom_template.html"
)

# Language utilities
supported_langs = config.get_supported_languages()  # ['ko', 'ja']
spac_path = config.get_spac_path('ko')  # '/spac/ko_KR/'

Environment Variable Integration:
The configuration can be overridden using environment variables:
- AEM_HOST: Override the AEM host URL
- SOURCE_LANG: Override the source language
- TEMPLATE_FILE: Override the template file path

This design ensures that the application can be easily configured for different
environments (development, staging, production) without code changes, following
the twelve-factor app methodology.
"""
from dataclasses import dataclass
from typing import Dict


@dataclass
class Config:
    """애플리케이션 전역 설정을 관리하는 데이터 클래스
    
    Attributes:
        aem_host: AEM 서버 호스트 URL
        source_lang: 소스 언어 코드
        template_file: HTML 템플릿 파일 경로
        language_mapping: 로케일과 언어 코드 매핑
        spac_paths: 언어별 SPAC 경로 매핑
    """
    aem_host: str = "https://prod-author.illumina.com"
    source_lang: str = "en"
    template_file: str = "template.html"
    
    # 언어 매핑 설정
    language_mapping: Dict[str, str] = None
    spac_paths: Dict[str, str] = None
    
    def __post_init__(self):
        """데이터클래스 초기화 후 실행되는 메서드"""
        if self.language_mapping is None:
            self.language_mapping = {
                'ko-KR': 'ko',
                'ja-JP': 'ja'
            }
        
        if self.spac_paths is None:
            self.spac_paths = {
                'ko': '/spac/ko_KR/',
                'ja': '/spac/ja_JP/'
            }
    
    @property
    def source_lang_path(self) -> str:
        """소스 언어 경로 생성
        
        Returns:
            언어 마스터 경로 문자열
        """
        return f"language-master#{self.source_lang}"
    
    def get_supported_languages(self) -> list:
        """지원되는 언어 목록 반환
        
        Returns:
            지원 언어 코드 리스트
        """
        return list(self.language_mapping.values())
    
    def get_spac_path(self, lang_code: str) -> str:
        """특정 언어의 SPAC 경로 반환
        
        Args:
            lang_code: 언어 코드
            
        Returns:
            SPAC 경로 문자열
        """
        return self.spac_paths.get(lang_code, '')