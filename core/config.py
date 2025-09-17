"""
core/config.py - 애플리케이션 설정 관리
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