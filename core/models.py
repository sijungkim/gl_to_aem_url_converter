"""
core/models.py - 도메인 모델 정의
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
    """
    url: str
    path: str
    language: str
    
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
            url과 path를 포함한 딕셔너리
        """
        return {
            "url": self.url,
            "path": self.path
        }


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