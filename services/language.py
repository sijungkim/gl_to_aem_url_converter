"""
services/language.py - 언어 감지 및 처리 서비스
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