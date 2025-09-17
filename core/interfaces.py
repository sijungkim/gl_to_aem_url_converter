"""
core/interfaces.py - 추상 인터페이스 및 프로토콜 정의
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