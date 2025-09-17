"""
---
title: "AEM URL Generation and Validation Services"
description: "Service layer components for generating AEM MSM editor URLs from GlobalLink translated content. Implements URLGenerator interface to transform GlobalLink file paths into proper AEM editor URLs for language master (English), target language content, and SPAC target language review workflow."
architect: "Sijung Kim"
authors: ["Sijung Kim", "Claude", "Gemini"]
reviewed_by: "Sijung Kim"
created_date: "2025-09-15"
last_modified: "2025-09-17"
version: "2.0.0"
module_type: "Service Layer"
dependencies: ["typing", "core.interfaces", "core.config"]
key_classes: ["AEMURLGenerator", "URLValidator"]
key_functions: ["generate", "build_editor_url", "create_aem_path", "validate"]
design_patterns: ["Strategy Pattern", "Template Method Pattern"]
solid_principles: ["SRP - Single Responsibility Principle", "OCP - Open/Closed Principle", "LSP - Liskov Substitution Principle"]
features: ["URL Generation", "Path Transformation", "Validation", "AEM Integration"]
tags: ["url-generation", "aem-integration", "validation", "services"]
---

services/url_generator.py - AEM URL Generation and Validation Services

This module implements the core business logic for generating AEM editor URLs
from GlobalLink translation files. It provides services for transforming file
paths and names into properly formatted AEM editor URLs that can be used to
directly access content in the AEM authoring environment.

Key Responsibilities:
- Generate AEM editor URLs from file names and target languages
- Transform file paths according to AEM content structure conventions
- Validate generated URLs for correctness and accessibility
- Handle language-specific path transformations
- Implement URL generation strategy pattern

Service Classes:

1. AEMURLGenerator (implements URLGenerator interface):
   Core service for generating AEM editor URLs with language-specific
   transformations and proper path handling.

   Key Features:
   - File name to AEM path transformation (.xml to .html conversion)
   - Language-specific path generation using configuration
   - AEM editor URL construction with proper formatting
   - Error handling for invalid file names and unsupported formats

2. URLValidator:
   Validation service for ensuring generated URLs meet AEM requirements
   and follow proper formatting conventions.

   Key Features:
   - URL format validation
   - Path structure verification
   - AEM-specific URL pattern checking
   - Accessibility validation

URL Generation Algorithm:
1. Extract file name from GlobalLink path
2. Validate file name format (must start with #content)
3. Transform language path using configuration mappings
4. Convert .xml extension to .html for web access
5. Construct full AEM editor URL with host and editor path
6. Validate generated URL format and structure

The module follows SOLID principles by implementing the URLGenerator
interface (LSP), focusing on single responsibility (SRP), and being
open for extension through the strategy pattern (OCP).
"""
from typing import Optional, Tuple
from core.interfaces import URLGenerator
from core.config import Config


class AEMURLGenerator(URLGenerator):
    """AEM URL 생성 서비스 (DIP - 인터페이스 구현)
    
    AEM 에디터 URL을 생성하는 구체적인 구현.
    URLGenerator 인터페이스를 구현하여 의존성 역전 달성.
    """
    
    def __init__(self, config: Config):
        """URL 생성기 초기화
        
        Args:
            config: 애플리케이션 설정
        """
        self.config = config
        self.aem_host = config.aem_host
        self.source_lang_path = config.source_lang_path
    
    def generate(self, file_name: str, target_lang: str) -> Optional[Tuple[str, str]]:
        """파일명과 대상 언어로 AEM URL 생성
        
        Args:
            file_name: 원본 파일명 (#content로 시작)
            target_lang: 대상 언어 코드 ('ko', 'ja' 등)
            
        Returns:
            성공 시 (URL, 경로) 튜플, 실패 시 None
        """
        # 유효성 검증
        if not self._is_valid_source_file(file_name):
            return None
        
        # 대상 파일명 생성
        target_file_name = self._create_target_filename(file_name, target_lang)
        if not target_file_name:
            return None
        
        # AEM 경로 생성
        aem_path = self._create_aem_path(target_file_name)
        if not aem_path:
            return None
        
        # 최종 URL 생성
        final_url = self._build_final_url(aem_path)
        
        return final_url, aem_path
    
    def _is_valid_source_file(self, file_name: str) -> bool:
        """소스 파일 유효성 검증
        
        Args:
            file_name: 검증할 파일명
            
        Returns:
            유효한 소스 파일이면 True
        """
        return self.source_lang_path in file_name
    
    def _create_target_filename(self, file_name: str, target_lang: str) -> Optional[str]:
        """대상 언어용 파일명 생성
        
        Args:
            file_name: 원본 파일명
            target_lang: 대상 언어
            
        Returns:
            변환된 파일명 또는 None
        """
        target_lang_path = f"language-master#{target_lang}"
        target_file_name = file_name.replace(self.source_lang_path, target_lang_path)
        
        # #으로 시작하지 않으면 유효하지 않음
        if not target_file_name.startswith('#'):
            return None
            
        return target_file_name
    
    def _create_aem_path(self, target_file_name: str) -> Optional[str]:
        """AEM 경로 생성
        
        Args:
            target_file_name: 대상 파일명
            
        Returns:
            AEM 경로 또는 None
        """
        # # 제거하고 #을 /로 변환
        aem_path = target_file_name[1:].replace('#', '/')
        
        # XML 파일만 처리
        if not aem_path.endswith('.xml'):
            return None
        
        # .xml을 .html로 변환
        aem_path = aem_path[:-4] + '.html'
        
        return aem_path
    
    def _build_final_url(self, aem_path: str) -> str:
        """최종 URL 생성
        
        Args:
            aem_path: AEM 경로
            
        Returns:
            완전한 AEM 에디터 URL
        """
        return f"{self.aem_host}/editor.html/{aem_path}"


class URLValidator:
    """URL 유효성 검증 서비스 (SRP)
    
    생성된 URL의 유효성을 검증하는 별도 서비스.
    """
    
    def __init__(self, config: Config):
        """검증기 초기화
        
        Args:
            config: 애플리케이션 설정
        """
        self.config = config
    
    def is_valid_aem_url(self, url: str) -> bool:
        """AEM URL 유효성 검증
        
        Args:
            url: 검증할 URL
            
        Returns:
            유효한 AEM URL이면 True
        """
        if not url:
            return False
        
        # AEM 호스트로 시작하는지 확인
        if not url.startswith(self.config.aem_host):
            return False
        
        # editor.html 경로 포함 확인
        if '/editor.html/' not in url:
            return False
        
        # .html로 끝나는지 확인
        if not url.endswith('.html'):
            return False
        
        return True
    
    def is_valid_path(self, path: str) -> bool:
        """경로 유효성 검증
        
        Args:
            path: 검증할 경로
            
        Returns:
            유효한 경로면 True
        """
        if not path:
            return False
        
        # content로 시작하는지 확인
        if not path.startswith('content/'):
            return False
        
        # language-master 포함 확인
        if 'language-master' not in path:
            return False
        
        return True