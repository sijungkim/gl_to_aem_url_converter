"""
---
title: "Abstract Interfaces and Protocols"
description: "Core interface definitions implementing the Interface Segregation and Dependency Inversion principles. Provides abstract base classes and protocols that define contracts for services without coupling to implementations, enabling extensibility and testability."
architect: "Sijung Kim"
authors: ["Sijung Kim", "Claude", "Gemini"]
reviewed_by: "Sijung Kim"
created_date: "2025-09-15"
last_modified: "2025-09-17"
version: "2.0.0"
module_type: "Core Domain Layer"
dependencies: ["abc", "typing", "core.models"]
key_classes: ["URLGenerator", "TemplateRenderer"]
key_protocols: ["FileProcessor", "LanguageDetector", "DataFrameBuilder"]
key_functions: ["generate", "render", "process", "detect", "build"]
design_patterns: ["Abstract Factory Pattern", "Strategy Pattern", "Protocol Pattern"]
solid_principles: ["ISP - Interface Segregation Principle", "DIP - Dependency Inversion Principle", "OCP - Open/Closed Principle"]
features: ["Duck Typing", "Protocol-based Design", "Extensibility", "Type Safety"]
tags: ["interfaces", "protocols", "abstractions", "core", "contracts"]
---

core/interfaces.py - Abstract Interfaces and Protocols

This module defines the core abstractions that enable the application to follow
SOLID principles, particularly the Interface Segregation Principle (ISP) and
Dependency Inversion Principle (DIP). It provides contracts that implementations
must follow without dictating how they should be implemented.

Key Responsibilities:
- Define abstract interfaces for core services
- Establish protocols for duck-typed services
- Enable dependency inversion throughout the application
- Support extensibility and plugin architecture
- Facilitate testing through mockable interfaces

Architecture:
The module uses a combination of Abstract Base Classes (ABC) and Protocols to
define contracts. ABCs are used for core services that require explicit inheritance,
while Protocols enable duck typing for more flexible implementations.

Interface Design Principles:
- Interface Segregation: Each interface is focused and contains only related methods
- Dependency Inversion: High-level modules depend on these abstractions
- Open/Closed: New implementations can be added without modifying existing code
- Liskov Substitution: All implementations are interchangeable

Abstract Interfaces:

1. URLGenerator (ABC):
   Defines the contract for URL generation services. Implementations must provide
   the ability to generate AEM editor URLs from file names and target languages.

   Methods:
   - generate(file_name, target_lang) -> Optional[Tuple[str, str]]
     Generates a URL and path tuple for the given file and language

   Design: Uses ABC to enforce explicit inheritance and ensure all implementations
   provide the required generate method.

2. TemplateRenderer (ABC):
   Defines the contract for template rendering services. Implementations can
   support different template engines or rendering strategies.

   Methods:
   - render(links, **kwargs) -> str
     Renders links into formatted output (HTML, etc.)

   Design: Abstract enough to support multiple rendering backends while ensuring
   consistent interface for client code.

Protocols:

1. FileProcessor (Protocol):
   Defines the contract for file processing services using duck typing. Any class
   that implements the process method can be used as a FileProcessor.

   Methods:
   - process(file_path) -> Optional[AEMLink]
     Processes a file and returns an AEMLink if successful

   Design: Uses Protocol to enable duck typing and flexible implementations
   without requiring explicit inheritance.

2. LanguageDetector (Protocol):
   Defines the contract for language detection services. Enables different
   language detection strategies without coupling to specific implementations.

   Methods:
   - detect(path) -> Optional[str]
     Detects language code from a file path

   Design: Simple, focused interface that can be implemented by various
   language detection algorithms.

3. DataFrameBuilder (Protocol):
   Defines the contract for DataFrame construction services. Allows different
   data presentation strategies while maintaining consistent interface.

   Methods:
   - build(links) -> DataFrame
     Builds a pandas DataFrame from a list of links

   Design: Generic enough to support different DataFrame structures while
   ensuring type safety.

Benefits of Protocol-based Design:
- Duck Typing: Implementations don't need explicit inheritance
- Flexibility: Easy to create lightweight implementations
- Testing: Simple to create mock objects that satisfy protocols
- Interoperability: Different libraries can implement protocols naturally

Usage Examples:
# Abstract Base Class implementation
class AEMURLGenerator(URLGenerator):
    def generate(self, file_name: str, target_lang: str) -> Optional[Tuple[str, str]]:
        # Implementation here
        pass

# Protocol implementation (duck typing)
class MyFileProcessor:
    def process(self, file_path: str) -> Optional[AEMLink]:
        # Implementation here - no inheritance needed
        pass

# Usage with type hints
def process_files(processor: FileProcessor, files: List[str]) -> List[AEMLink]:
    return [processor.process(f) for f in files if processor.process(f)]

Extensibility:
The interface design enables easy extension of the application:
- New URL generators can implement URLGenerator
- Different template engines can implement TemplateRenderer
- Custom file processors can satisfy the FileProcessor protocol
- Alternative language detection can implement LanguageDetector

Testing Support:
All interfaces and protocols are designed to be easily mockable:
- Simple method signatures reduce mock complexity
- Optional return types handle edge cases gracefully
- Protocol-based design enables lightweight test doubles

The interfaces form the foundation for the application's plugin architecture,
enabling new functionality to be added without modifying existing code,
demonstrating the Open/Closed Principle in action.
"""
from abc import ABC, abstractmethod
from typing import Protocol, Optional, Tuple, List, Dict
from .models import AEMLink, LinkCollection


class URLGenerator(ABC):
    """URL 생성 인터페이스
    
    URL 생성 로직의 추상 인터페이스.
    새로운 URL 생성 방식은 이 인터페이스를 구현해야 함.
    """
    
    @abstractmethod
    def generate(self, file_name: str, target_lang: str) -> Optional[Tuple[str, str]]:
        """URL 생성 추상 메서드
        
        Args:
            file_name: 원본 파일명
            target_lang: 대상 언어 코드
            
        Returns:
            (URL, 경로) 튜플 또는 None
        """
        pass


class FileProcessor(Protocol):
    """파일 처리 프로토콜
    
    파일 처리기가 구현해야 할 프로토콜.
    덕 타이핑을 통한 유연한 인터페이스 제공.
    """
    
    def process(self, file_path: str) -> Optional[AEMLink]:
        """파일 처리 메서드
        
        Args:
            file_path: 처리할 파일 경로
            
        Returns:
            AEMLink 객체 또는 None
        """
        ...


class TemplateRenderer(ABC):
    """템플릿 렌더링 인터페이스
    
    HTML 템플릿 렌더링의 추상 인터페이스.
    다양한 렌더링 방식을 지원하기 위한 기반 클래스.
    """
    
    @abstractmethod
    def render(self, links: List[Dict[str, str]], **kwargs) -> str:
        """템플릿 렌더링 추상 메서드
        
        Args:
            links: 렌더링할 링크 리스트
            **kwargs: 추가 렌더링 옵션
            
        Returns:
            렌더링된 HTML 문자열
        """
        pass


class LanguageDetector(Protocol):
    """언어 감지 프로토콜
    
    파일 경로에서 언어를 감지하는 프로토콜.
    """
    
    def detect(self, path: str) -> Optional[str]:
        """언어 감지 메서드
        
        Args:
            path: 파일 경로
            
        Returns:
            언어 코드 또는 None
        """
        ...


class DataFrameBuilder(Protocol):
    """DataFrame 빌더 프로토콜
    
    링크를 DataFrame으로 변환하는 프로토콜.
    """
    
    def build(self, links: List[Dict[str, str]]) -> any:
        """DataFrame 생성 메서드
        
        Args:
            links: 링크 리스트
            
        Returns:
            pandas DataFrame 객체
        """
        ...