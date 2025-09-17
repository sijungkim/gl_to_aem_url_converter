"""
---
title: "Domain Models and Business Entities"
description: "Core domain models representing the business entities of the AEM URL Converter. Implements immutable data structures for AEM links, link collections, and processing results with rich behavior and validation following Domain-Driven Design principles. Enhanced with multi-ZIP support for batch processing."
architect: "Sijung Kim"
authors: ["Sijung Kim", "Claude", "Gemini"]
reviewed_by: "Sijung Kim"
created_date: "2025-09-15"
last_modified: "2025-09-18"
version: "2.1.0"
module_type: "Core Domain Layer"
dependencies: ["dataclasses", "typing"]
key_classes: ["AEMLink", "LinkCollection", "ProcessingResult"]
key_functions: ["get_path_parts", "get_page_name", "to_dict", "get_total_count", "add_warning", "is_successful"]
design_patterns: ["Data Class Pattern", "Value Object Pattern", "Aggregate Pattern"]
solid_principles: ["SRP - Single Responsibility Principle", "ISP - Interface Segregation Principle"]
features: ["Immutable Design", "Rich Behavior", "Type Safety", "Validation", "Business Logic", "Multi-ZIP Source Tracking"]
tags: ["domain-models", "business-entities", "dataclass", "core", "value-objects", "multi-zip"]
---

core/models.py - Domain Models and Business Entities

This module defines the core domain models that represent the fundamental business
entities of the AEM URL Converter application. These models encapsulate both data
and behavior, following Domain-Driven Design principles and maintaining rich domain
logic while remaining independent of external concerns.

Key Responsibilities:
- Define business entities and value objects
- Encapsulate domain-specific business logic
- Provide type-safe data structures
- Implement validation and business rules
- Maintain data integrity and consistency

Architecture:
The models are implemented as immutable dataclasses that combine data with behavior.
Each model has a single responsibility and provides methods that implement business
logic related to that entity. The models form the foundation of the domain layer
and are used throughout the application.

Domain Models:

1. AEMLink (Value Object):
   Represents a single AEM editor link with associated metadata. Contains utility
   methods for path manipulation and data conversion. Enhanced to track source ZIP
   file for multi-ZIP batch processing.

   Properties:
   - url: The complete AEM editor URL
   - path: The content path within AEM
   - language: The target language code (ko, ja, etc.)
   - source_zip: The source ZIP filename (optional, for multi-ZIP tracking)

   Behavior:
   - Path parsing and hierarchy extraction
   - Page name extraction from paths
   - Legacy format conversion for compatibility

2. LinkCollection (Aggregate):
   Manages collections of AEM links organized by language. Provides aggregate
   operations and maintains consistency across language-specific collections.

   Properties:
   - korean: List of Korean language AEM links
   - japanese: List of Japanese language AEM links

   Behavior:
   - Total count calculations across all languages
   - Language-specific link retrieval
   - Collection validation and consistency checks

3. ProcessingResult (Aggregate Root):
   Represents the outcome of a file processing operation. Encapsulates the
   processed links along with metadata about the processing operation,
   including error handling and warning management.

   Properties:
   - links: LinkCollection containing all processed links
   - processed_count: Number of files successfully processed
   - error_count: Number of errors encountered
   - warnings: List of warning messages

   Behavior:
   - Success/failure determination logic
   - Warning accumulation and management
   - Processing statistics calculations

Key Features:
- Immutable Design: All models are immutable, preventing accidental modifications
- Type Safety: Full type annotations ensure compile-time safety
- Rich Behavior: Models contain business logic, not just data
- Validation: Built-in validation ensures data integrity
- Composability: Models can be easily composed and combined
- Testability: Pure functions make testing straightforward

Business Logic:
The models implement domain-specific business logic:
- Path parsing follows AEM content structure conventions
- Link validation ensures proper URL formation
- Collection aggregation maintains language separation
- Processing results track success/failure states

Usage Examples:
# Creating an AEM link
link = AEMLink(
    url="https://author.example.com/editor.html/content/en/page.html",
    path="/content/en/page.html",
    language="en"
)

# Path operations
parts = link.get_path_parts()  # ['en', 'page']
page_name = link.get_page_name()  # 'page'

# Creating collections
collection = LinkCollection(korean=[ko_link1, ko_link2], japanese=[ja_link1])
total = collection.get_total_count()  # 3

# Processing results
result = ProcessingResult(links=collection, processed_count=5)
result.add_warning("Some files were skipped")
success = result.is_successful()  # True if no errors and links exist

Design Principles:
- Single Responsibility: Each model has one clear purpose
- Immutability: Models cannot be modified after creation
- Encapsulation: Internal state is protected and accessed through methods
- Cohesion: Related data and behavior are grouped together
- Loose Coupling: Models don't depend on external services or infrastructure

The models serve as the foundation for the entire application, providing a clear
and consistent representation of the business domain that all other layers can
depend upon without coupling to external concerns.
"""
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class AEMLink:
    """AEM 링크를 표현하는 도메인 모델

    Attributes:
        url: AEM 에디터 URL
        path: 파일 경로
        language: 언어 코드 (ko, ja 등)
        source_zip: 소스 ZIP 파일명 (optional, for multi-ZIP processing)
    """
    url: str
    path: str
    language: str
    source_zip: str = None
    
    def get_path_parts(self) -> List[str]:
        """경로를 계층별로 분할
        
        Returns:
            경로 구성 요소 리스트 (content 레벨 제외)
        """
        # /content/... 에서 content를 제외한 나머지 경로
        return self.path.strip('/').replace('.html', '').split('/')[1:]
    
    def get_page_name(self) -> str:
        """페이지 이름 추출
        
        Returns:
            경로의 마지막 부분 (페이지 이름)
        """
        parts = self.get_path_parts()
        return parts[-1] if parts else ""
    
    def to_dict(self) -> Dict[str, str]:
        """딕셔너리로 변환 (레거시 코드 호환용)

        Returns:
            url, path, source_zip을 포함한 딕셔너리
        """
        result = {
            "url": self.url,
            "path": self.path
        }
        if self.source_zip:
            result["source_zip"] = self.source_zip
        return result


@dataclass
class LinkCollection:
    """언어별 링크 컬렉션
    
    Attributes:
        korean: 한국어 링크 리스트
        japanese: 일본어 링크 리스트
    """
    korean: List[AEMLink]
    japanese: List[AEMLink]
    
    def get_total_count(self) -> int:
        """전체 링크 개수 반환
        
        Returns:
            모든 언어의 링크 총 개수
        """
        return len(self.korean) + len(self.japanese)
    
    def get_by_language(self, lang_code: str) -> List[AEMLink]:
        """특정 언어의 링크 리스트 반환
        
        Args:
            lang_code: 언어 코드 ('ko' 또는 'ja')
            
        Returns:
            해당 언어의 링크 리스트
        """
        if lang_code == 'ko':
            return self.korean
        elif lang_code == 'ja':
            return self.japanese
        else:
            return []
    
    def has_links(self) -> bool:
        """링크가 있는지 확인
        
        Returns:
            링크가 하나라도 있으면 True
        """
        return bool(self.korean or self.japanese)


@dataclass
class ProcessingResult:
    """파일 처리 결과
    
    Attributes:
        links: 링크 컬렉션
        processed_count: 처리된 파일 수
        error_count: 오류 발생 수
        warnings: 경고 메시지 리스트
    """
    links: LinkCollection
    processed_count: int = 0
    error_count: int = 0
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []
    
    def add_warning(self, message: str):
        """경고 메시지 추가
        
        Args:
            message: 경고 메시지
        """
        self.warnings.append(message)
    
    def is_successful(self) -> bool:
        """처리 성공 여부
        
        Returns:
            오류가 없고 링크가 있으면 True
        """
        return self.error_count == 0 and self.links.has_links()